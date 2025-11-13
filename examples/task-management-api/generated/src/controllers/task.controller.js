/**
 * Task Controller
 * Handles task-related business logic
 */

const { Task, Project, User, Comment } = require('../models');
const { ApiError } = require('../utils/ApiError');
const { searchService } = require('../services/search.service');
const { notificationService } = require('../services/notification.service');
const logger = require('../utils/logger');

class TaskController {
  /**
   * Get all tasks with filtering and pagination
   */
  async getTasks(req, res, next) {
    try {
      const {
        projectId,
        status,
        priority,
        assigneeId,
        search,
        page = 1,
        limit = 20,
        sortBy = 'createdAt',
        order = 'DESC'
      } = req.query;

      const where = {};

      // Apply filters
      if (projectId) where.projectId = projectId;
      if (status) where.status = status;
      if (priority) where.priority = priority;
      if (assigneeId) where.assigneeId = assigneeId;

      // Build query options
      const options = {
        where,
        include: [
          {
            model: User,
            as: 'assignee',
            attributes: ['id', 'name', 'email', 'avatarUrl']
          },
          {
            model: User,
            as: 'creator',
            attributes: ['id', 'name', 'email']
          },
          {
            model: Project,
            as: 'project',
            attributes: ['id', 'name']
          }
        ],
        order: [[sortBy, order]],
        limit: parseInt(limit),
        offset: (parseInt(page) - 1) * parseInt(limit)
      };

      // Handle search
      let tasks;
      let total;

      if (search) {
        const searchResults = await searchService.searchTasks(search, where);
        tasks = searchResults.results;
        total = searchResults.total;
      } else {
        const result = await Task.findAndCountAll(options);
        tasks = result.rows;
        total = result.count;
      }

      res.json({
        data: tasks,
        pagination: {
          page: parseInt(page),
          limit: parseInt(limit),
          total,
          pages: Math.ceil(total / parseInt(limit))
        }
      });
    } catch (error) {
      logger.error('Error getting tasks:', error);
      next(error);
    }
  }

  /**
   * Get single task by ID
   */
  async getTask(req, res, next) {
    try {
      const { id } = req.params;

      const task = await Task.findByPk(id, {
        include: [
          {
            model: User,
            as: 'assignee',
            attributes: ['id', 'name', 'email', 'avatarUrl']
          },
          {
            model: User,
            as: 'creator',
            attributes: ['id', 'name', 'email']
          },
          {
            model: Project,
            as: 'project',
            attributes: ['id', 'name', 'visibility']
          },
          {
            model: Comment,
            as: 'comments',
            include: [
              {
                model: User,
                as: 'user',
                attributes: ['id', 'name', 'email', 'avatarUrl']
              }
            ],
            order: [['createdAt', 'ASC']]
          }
        ]
      });

      if (!task) {
        throw new ApiError(404, 'Task not found');
      }

      // Check permissions
      await this._checkTaskAccess(req.user, task);

      res.json({ data: task });
    } catch (error) {
      logger.error('Error getting task:', error);
      next(error);
    }
  }

  /**
   * Create new task
   */
  async createTask(req, res, next) {
    try {
      const {
        projectId,
        title,
        description,
        priority,
        assigneeId,
        dueDate,
        tags
      } = req.body;

      // Check if project exists and user has access
      const project = await Project.findByPk(projectId);
      if (!project) {
        throw new ApiError(404, 'Project not found');
      }

      await this._checkProjectAccess(req.user, project);

      // Create task
      const task = await Task.create({
        projectId,
        title,
        description,
        priority: priority || 'medium',
        assigneeId,
        dueDate,
        tags: tags || [],
        createdById: req.user.id,
        status: 'todo'
      });

      // Load associations
      await task.reload({
        include: [
          { model: User, as: 'assignee', attributes: ['id', 'name', 'email'] },
          { model: User, as: 'creator', attributes: ['id', 'name', 'email'] },
          { model: Project, as: 'project', attributes: ['id', 'name'] }
        ]
      });

      // Send notifications
      if (assigneeId && assigneeId !== req.user.id) {
        await notificationService.notifyTaskAssignment(task, req.user);
      }

      // Emit WebSocket event
      req.io.to(`project:${projectId}`).emit('task:created', { task });

      logger.info(`Task created: ${task.id} by user ${req.user.id}`);

      res.status(201).json({ data: task });
    } catch (error) {
      logger.error('Error creating task:', error);
      next(error);
    }
  }

  /**
   * Update task
   */
  async updateTask(req, res, next) {
    try {
      const { id } = req.params;
      const updates = req.body;

      const task = await Task.findByPk(id, {
        include: [{ model: Project, as: 'project' }]
      });

      if (!task) {
        throw new ApiError(404, 'Task not found');
      }

      await this._checkTaskAccess(req.user, task);

      // Track changes for notifications
      const statusChanged = updates.status && updates.status !== task.status;
      const assigneeChanged = updates.assigneeId && updates.assigneeId !== task.assigneeId;

      // Update task
      await task.update(updates);

      // Reload with associations
      await task.reload({
        include: [
          { model: User, as: 'assignee', attributes: ['id', 'name', 'email'] },
          { model: User, as: 'creator', attributes: ['id', 'name', 'email'] },
          { model: Project, as: 'project', attributes: ['id', 'name'] }
        ]
      });

      // Send notifications
      if (statusChanged) {
        await notificationService.notifyTaskStatusChange(task, req.user);
      }

      if (assigneeChanged && task.assigneeId !== req.user.id) {
        await notificationService.notifyTaskAssignment(task, req.user);
      }

      // Emit WebSocket event
      req.io.to(`project:${task.projectId}`).emit('task:updated', { task });

      logger.info(`Task updated: ${task.id} by user ${req.user.id}`);

      res.json({ data: task });
    } catch (error) {
      logger.error('Error updating task:', error);
      next(error);
    }
  }

  /**
   * Delete task
   */
  async deleteTask(req, res, next) {
    try {
      const { id } = req.params;

      const task = await Task.findByPk(id, {
        include: [{ model: Project, as: 'project' }]
      });

      if (!task) {
        throw new ApiError(404, 'Task not found');
      }

      await this._checkTaskAccess(req.user, task);

      const projectId = task.projectId;

      await task.destroy();

      // Emit WebSocket event
      req.io.to(`project:${projectId}`).emit('task:deleted', { taskId: id });

      logger.info(`Task deleted: ${id} by user ${req.user.id}`);

      res.status(204).send();
    } catch (error) {
      logger.error('Error deleting task:', error);
      next(error);
    }
  }

  /**
   * Check if user has access to task
   */
  async _checkTaskAccess(user, task) {
    const project = task.project || await task.getProject();
    await this._checkProjectAccess(user, project);
  }

  /**
   * Check if user has access to project
   */
  async _checkProjectAccess(user, project) {
    if (project.visibility === 'public') {
      return true;
    }

    const member = await project.hasMember(user.id);
    if (!member && project.ownerId !== user.id) {
      throw new ApiError(403, 'You do not have access to this project');
    }
  }
}

module.exports = new TaskController();

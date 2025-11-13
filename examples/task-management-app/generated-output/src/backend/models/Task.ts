import { prisma } from '../config/database';
import { TaskStatus, TaskPriority } from '@prisma/client';

/**
 * Task Model
 *
 * Handles all database operations for tasks.
 * Generated based on the data model in PROJECT_BRIEF.md
 */

export interface CreateTaskDTO {
  title: string;
  description?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  projectId: string;
  assigneeId?: string;
  creatorId: string;
  dueDate?: Date;
  estimatedHours?: number;
}

export interface UpdateTaskDTO {
  title?: string;
  description?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  assigneeId?: string;
  dueDate?: Date;
  estimatedHours?: number;
}

export class TaskModel {
  /**
   * Create a new task
   */
  async create(data: CreateTaskDTO) {
    return prisma.task.create({
      data: {
        title: data.title,
        description: data.description,
        status: data.status || 'TODO',
        priority: data.priority || 'MEDIUM',
        projectId: data.projectId,
        assigneeId: data.assigneeId,
        creatorId: data.creatorId,
        dueDate: data.dueDate,
        estimatedHours: data.estimatedHours,
      },
      include: {
        assignee: true,
        creator: true,
        project: true,
      },
    });
  }

  /**
   * Find task by ID
   */
  async findById(id: string) {
    return prisma.task.findUnique({
      where: { id },
      include: {
        assignee: true,
        creator: true,
        project: true,
        comments: {
          include: {
            user: true,
          },
          orderBy: {
            createdAt: 'desc',
          },
        },
      },
    });
  }

  /**
   * Find all tasks for a project
   */
  async findByProject(projectId: string) {
    return prisma.task.findMany({
      where: { projectId },
      include: {
        assignee: true,
        creator: true,
      },
      orderBy: [
        { priority: 'desc' },
        { createdAt: 'desc' },
      ],
    });
  }

  /**
   * Update task
   */
  async update(id: string, data: UpdateTaskDTO) {
    return prisma.task.update({
      where: { id },
      data,
      include: {
        assignee: true,
        creator: true,
        project: true,
      },
    });
  }

  /**
   * Delete task
   */
  async delete(id: string) {
    return prisma.task.delete({
      where: { id },
    });
  }

  /**
   * Get tasks assigned to a user
   */
  async findByAssignee(assigneeId: string, filters?: {
    status?: TaskStatus;
    priority?: TaskPriority;
  }) {
    return prisma.task.findMany({
      where: {
        assigneeId,
        ...(filters?.status && { status: filters.status }),
        ...(filters?.priority && { priority: filters.priority }),
      },
      include: {
        project: true,
        creator: true,
      },
      orderBy: [
        { dueDate: 'asc' },
        { priority: 'desc' },
      ],
    });
  }
}

export default new TaskModel();

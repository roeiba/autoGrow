/**
 * Task API Tests
 * Integration tests for task endpoints
 */

const request = require('supertest');
const { app } = require('../src/server');
const { Task, User, Project } = require('../src/models');
const { generateToken } = require('../src/utils/jwt');

describe('Task API', () => {
  let authToken;
  let testUser;
  let testProject;

  beforeAll(async () => {
    // Create test user
    testUser = await User.create({
      email: 'test@example.com',
      password: 'hashedpassword',
      name: 'Test User',
      emailVerified: true
    });

    // Generate auth token
    authToken = generateToken({ id: testUser.id, email: testUser.email });

    // Create test project
    testProject = await Project.create({
      name: 'Test Project',
      description: 'Test project for task tests',
      ownerId: testUser.id,
      visibility: 'private'
    });
  });

  afterAll(async () => {
    // Clean up
    await Task.destroy({ where: {} });
    await Project.destroy({ where: {} });
    await User.destroy({ where: {} });
  });

  describe('POST /api/v1/tasks', () => {
    it('should create a new task', async () => {
      const taskData = {
        projectId: testProject.id,
        title: 'Test Task',
        description: 'This is a test task',
        priority: 'high',
        dueDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000) // 7 days from now
      };

      const response = await request(app)
        .post('/api/v1/tasks')
        .set('Authorization', `Bearer ${authToken}`)
        .send(taskData)
        .expect(201);

      expect(response.body.data).toMatchObject({
        title: taskData.title,
        description: taskData.description,
        priority: taskData.priority,
        status: 'todo',
        projectId: testProject.id,
        createdById: testUser.id
      });

      expect(response.body.data.id).toBeDefined();
    });

    it('should fail without authentication', async () => {
      const taskData = {
        projectId: testProject.id,
        title: 'Unauthorized Task'
      };

      await request(app)
        .post('/api/v1/tasks')
        .send(taskData)
        .expect(401);
    });

    it('should fail with invalid project ID', async () => {
      const taskData = {
        projectId: '00000000-0000-0000-0000-000000000000',
        title: 'Invalid Project Task'
      };

      await request(app)
        .post('/api/v1/tasks')
        .set('Authorization', `Bearer ${authToken}`)
        .send(taskData)
        .expect(404);
    });

    it('should validate required fields', async () => {
      const response = await request(app)
        .post('/api/v1/tasks')
        .set('Authorization', `Bearer ${authToken}`)
        .send({ projectId: testProject.id })
        .expect(400);

      expect(response.body.error).toBeDefined();
    });
  });

  describe('GET /api/v1/tasks', () => {
    beforeEach(async () => {
      // Create test tasks
      await Task.bulkCreate([
        {
          projectId: testProject.id,
          title: 'Task 1',
          status: 'todo',
          priority: 'high',
          createdById: testUser.id
        },
        {
          projectId: testProject.id,
          title: 'Task 2',
          status: 'in_progress',
          priority: 'medium',
          createdById: testUser.id,
          assigneeId: testUser.id
        },
        {
          projectId: testProject.id,
          title: 'Task 3',
          status: 'done',
          priority: 'low',
          createdById: testUser.id
        }
      ]);
    });

    afterEach(async () => {
      await Task.destroy({ where: {} });
    });

    it('should get all tasks', async () => {
      const response = await request(app)
        .get('/api/v1/tasks')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.data).toHaveLength(3);
      expect(response.body.pagination).toBeDefined();
      expect(response.body.pagination.total).toBe(3);
    });

    it('should filter tasks by status', async () => {
      const response = await request(app)
        .get('/api/v1/tasks?status=todo')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.data).toHaveLength(1);
      expect(response.body.data[0].status).toBe('todo');
    });

    it('should filter tasks by priority', async () => {
      const response = await request(app)
        .get('/api/v1/tasks?priority=high')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.data).toHaveLength(1);
      expect(response.body.data[0].priority).toBe('high');
    });

    it('should filter tasks by assignee', async () => {
      const response = await request(app)
        .get(`/api/v1/tasks?assigneeId=${testUser.id}`)
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.data).toHaveLength(1);
      expect(response.body.data[0].assigneeId).toBe(testUser.id);
    });

    it('should paginate results', async () => {
      const response = await request(app)
        .get('/api/v1/tasks?page=1&limit=2')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.data).toHaveLength(2);
      expect(response.body.pagination.page).toBe(1);
      expect(response.body.pagination.limit).toBe(2);
      expect(response.body.pagination.pages).toBe(2);
    });
  });

  describe('GET /api/v1/tasks/:id', () => {
    let testTask;

    beforeEach(async () => {
      testTask = await Task.create({
        projectId: testProject.id,
        title: 'Single Task Test',
        description: 'Task for get by ID test',
        createdById: testUser.id
      });
    });

    afterEach(async () => {
      await Task.destroy({ where: {} });
    });

    it('should get task by ID', async () => {
      const response = await request(app)
        .get(`/api/v1/tasks/${testTask.id}`)
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.data).toMatchObject({
        id: testTask.id,
        title: testTask.title,
        description: testTask.description
      });
    });

    it('should return 404 for non-existent task', async () => {
      await request(app)
        .get('/api/v1/tasks/00000000-0000-0000-0000-000000000000')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(404);
    });
  });

  describe('PUT /api/v1/tasks/:id', () => {
    let testTask;

    beforeEach(async () => {
      testTask = await Task.create({
        projectId: testProject.id,
        title: 'Task to Update',
        status: 'todo',
        createdById: testUser.id
      });
    });

    afterEach(async () => {
      await Task.destroy({ where: {} });
    });

    it('should update task', async () => {
      const updates = {
        title: 'Updated Task Title',
        status: 'in_progress',
        priority: 'urgent'
      };

      const response = await request(app)
        .put(`/api/v1/tasks/${testTask.id}`)
        .set('Authorization', `Bearer ${authToken}`)
        .send(updates)
        .expect(200);

      expect(response.body.data).toMatchObject(updates);
    });

    it('should set completedAt when status changes to done', async () => {
      const response = await request(app)
        .put(`/api/v1/tasks/${testTask.id}`)
        .set('Authorization', `Bearer ${authToken}`)
        .send({ status: 'done' })
        .expect(200);

      expect(response.body.data.completedAt).toBeDefined();
      expect(response.body.data.status).toBe('done');
    });
  });

  describe('DELETE /api/v1/tasks/:id', () => {
    let testTask;

    beforeEach(async () => {
      testTask = await Task.create({
        projectId: testProject.id,
        title: 'Task to Delete',
        createdById: testUser.id
      });
    });

    it('should delete task', async () => {
      await request(app)
        .delete(`/api/v1/tasks/${testTask.id}`)
        .set('Authorization', `Bearer ${authToken}`)
        .expect(204);

      const deletedTask = await Task.findByPk(testTask.id);
      expect(deletedTask).toBeNull();
    });

    it('should return 404 for non-existent task', async () => {
      await request(app)
        .delete('/api/v1/tasks/00000000-0000-0000-0000-000000000000')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(404);
    });
  });
});

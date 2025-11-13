# Task Management API Documentation

## Overview

This is a RESTful API for managing tasks and projects with team collaboration features. The API provides endpoints for user authentication, project management, task tracking, and team collaboration.

**Base URL**: `http://localhost:3000/api/v1`

**API Version**: v1

## Authentication

All endpoints (except authentication endpoints) require a valid JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### POST /auth/register

Register a new user account.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "name": "John Doe"
}
```

**Response** (201 Created):
```json
{
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "emailVerified": false
  },
  "message": "Registration successful. Please check your email to verify your account."
}
```

### POST /auth/login

Login with email and password.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response** (200 OK):
```json
{
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "name": "John Doe"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": "24h"
  }
}
```

## Tasks

### GET /tasks

Get all tasks with optional filtering.

**Query Parameters**:
- `projectId` (optional): Filter by project ID
- `status` (optional): Filter by status (todo, in_progress, review, done)
- `priority` (optional): Filter by priority (low, medium, high, urgent)
- `assigneeId` (optional): Filter by assignee ID
- `search` (optional): Full-text search
- `page` (optional, default: 1): Page number
- `limit` (optional, default: 20): Items per page
- `sortBy` (optional, default: createdAt): Sort field
- `order` (optional, default: DESC): Sort order (ASC or DESC)

**Response** (200 OK):
```json
{
  "data": [
    {
      "id": "uuid",
      "projectId": "uuid",
      "title": "Implement authentication",
      "description": "Add JWT authentication to the API",
      "status": "in_progress",
      "priority": "high",
      "assigneeId": "uuid",
      "createdById": "uuid",
      "dueDate": "2024-12-31T23:59:59.000Z",
      "completedAt": null,
      "tags": ["backend", "security"],
      "createdAt": "2024-01-01T00:00:00.000Z",
      "updatedAt": "2024-01-02T10:30:00.000Z",
      "assignee": {
        "id": "uuid",
        "name": "John Doe",
        "email": "john@example.com",
        "avatarUrl": "https://..."
      },
      "creator": {
        "id": "uuid",
        "name": "Jane Smith",
        "email": "jane@example.com"
      },
      "project": {
        "id": "uuid",
        "name": "API Development"
      }
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "pages": 3
  }
}
```

### POST /tasks

Create a new task.

**Request Body**:
```json
{
  "projectId": "uuid",
  "title": "Implement user profile",
  "description": "Add user profile management endpoints",
  "priority": "medium",
  "assigneeId": "uuid",
  "dueDate": "2024-12-31T23:59:59.000Z",
  "tags": ["backend", "user-management"]
}
```

**Response** (201 Created):
```json
{
  "data": {
    "id": "uuid",
    "projectId": "uuid",
    "title": "Implement user profile",
    "description": "Add user profile management endpoints",
    "status": "todo",
    "priority": "medium",
    "assigneeId": "uuid",
    "createdById": "uuid",
    "dueDate": "2024-12-31T23:59:59.000Z",
    "tags": ["backend", "user-management"],
    "createdAt": "2024-01-15T10:00:00.000Z",
    "updatedAt": "2024-01-15T10:00:00.000Z"
  }
}
```

### GET /tasks/:id

Get a specific task by ID.

**Response** (200 OK):
```json
{
  "data": {
    "id": "uuid",
    "projectId": "uuid",
    "title": "Implement authentication",
    "description": "Add JWT authentication to the API",
    "status": "in_progress",
    "priority": "high",
    "assigneeId": "uuid",
    "createdById": "uuid",
    "dueDate": "2024-12-31T23:59:59.000Z",
    "completedAt": null,
    "tags": ["backend", "security"],
    "createdAt": "2024-01-01T00:00:00.000Z",
    "updatedAt": "2024-01-02T10:30:00.000Z",
    "assignee": { ... },
    "creator": { ... },
    "project": { ... },
    "comments": [
      {
        "id": "uuid",
        "content": "Working on this now",
        "userId": "uuid",
        "createdAt": "2024-01-02T09:00:00.000Z",
        "user": {
          "id": "uuid",
          "name": "John Doe",
          "email": "john@example.com"
        }
      }
    ]
  }
}
```

### PUT /tasks/:id

Update a task.

**Request Body** (all fields optional):
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "status": "review",
  "priority": "urgent",
  "assigneeId": "uuid",
  "dueDate": "2024-12-31T23:59:59.000Z",
  "tags": ["backend", "security", "priority"]
}
```

**Response** (200 OK):
```json
{
  "data": {
    "id": "uuid",
    "title": "Updated title",
    "status": "review",
    // ... updated task data
  }
}
```

### DELETE /tasks/:id

Delete a task.

**Response** (204 No Content)

## Projects

### GET /projects

Get all projects accessible by the current user.

**Query Parameters**:
- `page` (optional, default: 1)
- `limit` (optional, default: 20)

**Response** (200 OK):
```json
{
  "data": [
    {
      "id": "uuid",
      "name": "API Development",
      "description": "Backend API for task management",
      "visibility": "private",
      "status": "active",
      "ownerId": "uuid",
      "createdAt": "2024-01-01T00:00:00.000Z",
      "updatedAt": "2024-01-01T00:00:00.000Z"
    }
  ],
  "pagination": { ... }
}
```

### POST /projects

Create a new project.

**Request Body**:
```json
{
  "name": "New Project",
  "description": "Project description",
  "visibility": "private"
}
```

**Response** (201 Created)

## Comments

### GET /tasks/:taskId/comments

Get all comments for a task.

**Response** (200 OK):
```json
{
  "data": [
    {
      "id": "uuid",
      "taskId": "uuid",
      "content": "This is a comment with @mention",
      "mentions": ["uuid"],
      "userId": "uuid",
      "createdAt": "2024-01-15T10:00:00.000Z",
      "user": {
        "id": "uuid",
        "name": "John Doe",
        "email": "john@example.com"
      }
    }
  ]
}
```

### POST /tasks/:taskId/comments

Create a comment on a task.

**Request Body**:
```json
{
  "content": "This is a comment mentioning @username"
}
```

**Response** (201 Created)

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error Type",
  "message": "Detailed error message",
  "timestamp": "2024-01-15T10:00:00.000Z",
  "path": "/api/v1/tasks/invalid-id"
}
```

### Common Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Request successful, no content to return
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required or failed
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

## Rate Limiting

The API implements rate limiting:
- **Authentication endpoints**: 5 requests per 15 minutes per IP
- **Other endpoints**: 100 requests per minute per user

When rate limited, you'll receive a `429 Too Many Requests` response.

## WebSocket Events

The API supports real-time updates via WebSocket (Socket.io).

**Connection**:
```javascript
const socket = io('http://localhost:3000', {
  auth: {
    token: 'your-jwt-token'
  }
});
```

**Events**:
- `task:created` - New task created in a project
- `task:updated` - Task updated
- `task:deleted` - Task deleted
- `comment:created` - New comment on a task

**Subscribe to project updates**:
```javascript
socket.emit('join:project', { projectId: 'uuid' });
```

## Examples

### Complete Task Workflow

1. **Create a project**:
```bash
curl -X POST http://localhost:3000/api/v1/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"My Project","visibility":"private"}'
```

2. **Create a task**:
```bash
curl -X POST http://localhost:3000/api/v1/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"projectId":"uuid","title":"New Task","priority":"high"}'
```

3. **Update task status**:
```bash
curl -X PUT http://localhost:3000/api/v1/tasks/uuid \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"in_progress"}'
```

4. **Add a comment**:
```bash
curl -X POST http://localhost:3000/api/v1/tasks/uuid/comments \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"Started working on this"}'
```

5. **Complete the task**:
```bash
curl -X PUT http://localhost:3000/api/v1/tasks/uuid \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"done"}'
```

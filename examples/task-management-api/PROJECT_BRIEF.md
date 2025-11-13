# Project Brief - Task Management API

> **This is a demo PROJECT_BRIEF.md showcasing how to use the AI-Optimized Project Template.**
> This example demonstrates how AI agents generate a complete, production-ready API from requirements.

---

## 🎯 Project Overview

**Project Name**: Task Management API

**Brief Description**:
A RESTful API for managing tasks and projects with user authentication, team collaboration, and real-time notifications. Users can create, assign, track, and complete tasks within projects, with support for priorities, due dates, labels, and comments.

**Problem Statement**:
Teams need a simple yet powerful way to track work items, assign responsibilities, and monitor progress. Existing solutions are either too complex (enterprise project management tools) or too simple (basic to-do lists). This API provides a middle ground - flexible task management with team collaboration features.

**Target Users**:
- Development teams tracking sprint work
- Small businesses managing projects
- Freelancers organizing client work
- Students collaborating on group projects
- API consumers building custom task management UIs

---

## 📋 Core Requirements

### Functional Requirements

1. **User Management**
   - User registration with email verification
   - Secure authentication using JWT tokens
   - User profile management (name, avatar, preferences)
   - Password reset functionality
   - Role-based access control (Admin, Manager, Member)

2. **Project Management**
   - Create, read, update, delete projects
   - Project visibility settings (public, private, team)
   - Project members with role assignments
   - Project templates for quick setup
   - Archive completed projects

3. **Task Management**
   - Create tasks with title, description, assignee, due date
   - Task status workflow (Todo, In Progress, Review, Done)
   - Priority levels (Low, Medium, High, Urgent)
   - Task labels/tags for organization
   - Task dependencies (blocked by/blocking)
   - File attachments on tasks
   - Bulk task operations

4. **Collaboration Features**
   - Comments on tasks with mentions (@user)
   - Activity feed showing project updates
   - Task assignment notifications
   - Due date reminders
   - Real-time updates via WebSocket

5. **Search & Filtering**
   - Full-text search across tasks and projects
   - Filter by status, assignee, priority, labels
   - Sort by various fields
   - Saved filters for quick access

6. **Analytics & Reporting**
   - Task completion metrics
   - Team productivity statistics
   - Burndown charts for projects
   - Export data to CSV/JSON

### Non-Functional Requirements

- **Performance**: API responses under 200ms, support 1000+ concurrent users
- **Security**: OWASP Top 10 compliance, encrypted data at rest and in transit
- **Scalability**: Horizontal scaling capability, database replication
- **Reliability**: 99.9% uptime, automated backups, disaster recovery
- **Usability**: Clear API documentation, comprehensive error messages
- **Maintainability**: Clean code, comprehensive tests, logging and monitoring

---

## 🏗️ Technical Preferences

### Technology Stack

**Backend Framework**:
- [x] Node.js with Express.js
- Technology: Node.js 20.x LTS
- Reason: Fast development, rich ecosystem, excellent async support

**Database**:
- [x] PostgreSQL 16
- Reason: ACID compliance, JSON support, robust relational data model
- [x] Redis for caching and session storage
- Reason: Fast in-memory caching, pub/sub for real-time features

**API Design**:
- [x] RESTful API with JSON responses
- [x] OpenAPI 3.0 specification
- [x] API versioning (v1, v2, etc.)

**Authentication**:
- [x] JWT (JSON Web Tokens)
- [x] Bcrypt for password hashing
- [x] OAuth2 for third-party integration (future)

**Real-time Communication**:
- [x] Socket.io for WebSocket connections

**Testing**:
- [x] Jest for unit and integration tests
- [x] Supertest for API testing
- [x] 80%+ code coverage target

**DevOps**:
- [x] Docker for containerization
- [x] Docker Compose for local development
- [x] GitHub Actions for CI/CD
- [x] Kubernetes deployment manifests

**Monitoring & Logging**:
- [x] Winston for structured logging
- [x] Prometheus metrics
- [x] Health check endpoints

---

## 👥 User Roles & Permissions

| Role | Description | Key Permissions |
|------|-------------|-----------------|
| Admin | System administrator | Full access, user management, system configuration |
| Manager | Project manager | Create projects, manage team members, view all tasks |
| Member | Regular team member | Create/update assigned tasks, comment, view team projects |
| Guest | Read-only access | View public projects and tasks |

---

## 🔄 Key User Flows

### Flow 1: User Registration & Authentication
1. User submits registration form with email and password
2. API validates input and creates user account
3. System sends verification email
4. User clicks verification link
5. User logs in and receives JWT token
6. Token is used for all subsequent authenticated requests

### Flow 2: Creating and Managing a Project
1. Manager creates new project with name and description
2. Manager invites team members by email
3. System sends invitation notifications
4. Team members accept invitations
5. Manager creates initial tasks and assigns to team
6. Team members receive task assignment notifications

### Flow 3: Task Lifecycle
1. Member creates task with details (title, description, due date)
2. Task starts in "Todo" status
3. Member updates status to "In Progress" when starting work
4. Member adds comments documenting progress
5. Member marks task as "Review" when complete
6. Manager reviews and marks as "Done" or requests changes
7. Activity is logged in project feed

### Flow 4: Team Collaboration
1. Member encounters blocker and comments on task
2. Comment mentions another team member (@username)
3. Mentioned user receives real-time notification
4. Users have conversation in task comments
5. Task is unblocked and work continues
6. All activity is visible in project timeline

---

## 🗄️ Data Model (High-Level)

### User
- id: UUID, primary key
- email: string, unique, indexed
- password_hash: string, bcrypt hash
- name: string
- avatar_url: string, optional
- role: enum (admin, manager, member, guest)
- email_verified: boolean
- created_at, updated_at: timestamps

### Project
- id: UUID, primary key
- name: string, max 100 chars
- description: text, optional
- visibility: enum (public, private, team)
- status: enum (active, archived)
- owner_id: UUID, foreign key to User
- created_at, updated_at: timestamps

### Task
- id: UUID, primary key
- project_id: UUID, foreign key to Project
- title: string, max 200 chars
- description: text, optional
- status: enum (todo, in_progress, review, done)
- priority: enum (low, medium, high, urgent)
- assignee_id: UUID, foreign key to User, optional
- created_by_id: UUID, foreign key to User
- due_date: timestamp, optional
- completed_at: timestamp, optional
- created_at, updated_at: timestamps

### Comment
- id: UUID, primary key
- task_id: UUID, foreign key to Task
- user_id: UUID, foreign key to User
- content: text
- mentions: array of user IDs
- created_at, updated_at: timestamps

### ProjectMember
- project_id: UUID, foreign key to Project
- user_id: UUID, foreign key to User
- role: enum (manager, member)
- joined_at: timestamp
- Primary key: (project_id, user_id)

---

## 🔌 External Integrations

- [x] SMTP server for email notifications (SendGrid/Mailgun)
- [x] File storage for attachments (AWS S3 or local storage)
- [x] WebSocket server for real-time updates
- [ ] Slack integration for notifications (future)
- [ ] GitHub integration for linking commits to tasks (future)
- [ ] Calendar integration (Google/Outlook) (future)

---

## 📅 Timeline & Priorities

**Target Launch Date**: 4 weeks from project start

**Phase 1 - Core API (Weeks 1-2)** - Must Have:
1. User authentication and authorization
2. Project CRUD operations
3. Task CRUD operations
4. Basic API documentation

**Phase 2 - Collaboration (Week 3)** - Must Have:
5. Comments system
6. Activity feed
7. Email notifications
8. Search and filtering

**Phase 3 - Production Ready (Week 4)** - Must Have:
9. WebSocket real-time updates
10. Comprehensive tests (80%+ coverage)
11. Docker deployment setup
12. Monitoring and logging

**Future Enhancements**:
- Task templates and recurring tasks
- Time tracking on tasks
- Custom fields and workflows
- Advanced reporting and analytics
- Mobile app support
- Third-party integrations

---

## 🔒 Security Requirements

**Authentication & Authorization**:
- Secure password hashing (bcrypt, minimum 10 rounds)
- JWT tokens with expiration (24 hours access, 7 days refresh)
- Role-based access control on all endpoints
- Rate limiting on authentication endpoints

**Data Protection**:
- Input validation and sanitization
- SQL injection prevention (parameterized queries)
- XSS prevention (output encoding)
- CSRF protection for state-changing operations
- Encrypted connections (HTTPS/TLS)

**API Security**:
- API rate limiting (100 requests/minute per user)
- Request size limits
- CORS configuration
- Security headers (helmet.js)

---

## 📊 API Endpoints Overview

### Authentication
- POST /api/v1/auth/register - Register new user
- POST /api/v1/auth/login - Login user
- POST /api/v1/auth/logout - Logout user
- POST /api/v1/auth/refresh - Refresh JWT token
- POST /api/v1/auth/forgot-password - Request password reset
- POST /api/v1/auth/reset-password - Reset password

### Users
- GET /api/v1/users/me - Get current user profile
- PUT /api/v1/users/me - Update current user profile
- GET /api/v1/users/:id - Get user by ID

### Projects
- GET /api/v1/projects - List projects
- POST /api/v1/projects - Create project
- GET /api/v1/projects/:id - Get project details
- PUT /api/v1/projects/:id - Update project
- DELETE /api/v1/projects/:id - Delete project
- POST /api/v1/projects/:id/members - Add project member
- DELETE /api/v1/projects/:id/members/:userId - Remove member

### Tasks
- GET /api/v1/tasks - List tasks (with filtering)
- POST /api/v1/tasks - Create task
- GET /api/v1/tasks/:id - Get task details
- PUT /api/v1/tasks/:id - Update task
- DELETE /api/v1/tasks/:id - Delete task
- GET /api/v1/projects/:projectId/tasks - Get project tasks

### Comments
- GET /api/v1/tasks/:taskId/comments - List task comments
- POST /api/v1/tasks/:taskId/comments - Create comment
- PUT /api/v1/comments/:id - Update comment
- DELETE /api/v1/comments/:id - Delete comment

### Analytics
- GET /api/v1/projects/:id/analytics - Get project statistics
- GET /api/v1/users/:id/analytics - Get user statistics

---

## 💰 Budget & Resources

**Budget**: Open source / startup project (minimal budget)

**Team Size**: 1 developer + AI coding assistant

**Development Time**: 4 weeks full-time

**Resources Needed**:
- Development environment (local Docker)
- PostgreSQL database
- Redis instance
- Email service (free tier: SendGrid/Mailgun)
- Cloud hosting for production (AWS/GCP/Digital Ocean)

---

## 📝 Additional Context

**Design Philosophy**:
This API follows REST principles and clean architecture patterns. The focus is on:
- **Simplicity**: Easy to understand and use
- **Flexibility**: Extensible for various use cases
- **Developer Experience**: Clear documentation, helpful errors
- **Performance**: Optimized queries, caching, efficient data structures

**Success Metrics**:
- API response time < 200ms for 95th percentile
- Zero critical security vulnerabilities
- 80%+ code coverage
- Clear documentation for all endpoints
- Successful deployment with monitoring

**Known Constraints**:
- Initial version is single-tenant (one database for all users)
- File attachments limited to 10MB per file
- WebSocket connections limited to 1000 concurrent per server
- Email notifications may have slight delays (async queue)

---

## ✅ Completion Checklist

- [x] All required sections completed
- [x] Technical stack selected
- [x] API endpoints defined
- [x] Data model specified
- [x] Security requirements documented
- [x] Ready for AI agent implementation

---

**Next Step**: Provide this PROJECT_BRIEF.md to your AI coding assistant and request project generation following the template guidelines.

**Example Prompt**:
```
I've created a PROJECT_BRIEF.md for a Task Management API. Please generate the complete
project structure following the ai-project-template guidelines:

1. Read the PROJECT_BRIEF.md carefully
2. Follow the guidelines in .agents/project-rules.md
3. Generate the complete backend application in src/backend/
4. Include comprehensive tests
5. Create API documentation
6. Set up Docker and CI/CD configurations
7. Add monitoring and logging

Generate a production-ready application following best practices.
```

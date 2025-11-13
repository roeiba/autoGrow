# Project Brief - Task Management Application

> **This is the ONLY file you need to edit as a human user.**
> Fill in your project requirements below, then let AI agents generate everything else.

---

## 🎯 Project Overview

**Project Name**: TaskFlow

**Brief Description**:
A modern, collaborative task management application that helps teams organize work, track progress, and improve productivity. Features real-time collaboration, smart task prioritization, and seamless integration with popular development tools.

**Problem Statement**:
Teams struggle with fragmented task management across multiple tools, lack of visibility into project progress, and inefficient collaboration workflows. Existing solutions are either too complex or too simplistic, lacking the balance between ease of use and powerful features that growing teams need.

**Target Users**:
- Software development teams (5-50 members)
- Project managers coordinating multiple projects
- Remote and distributed teams needing real-time collaboration
- Startups and scale-ups requiring flexible task management

---

## 📋 Core Requirements

### Functional Requirements

1. **Task Management**
   - Create, read, update, delete tasks
   - Task priorities (low, medium, high, urgent)
   - Task statuses (backlog, todo, in progress, review, done)
   - Due dates and time estimates
   - Task assignments and reassignments
   - Subtasks and task dependencies
   - Task tags and labels

2. **User & Team Management**
   - User authentication (email/password, OAuth)
   - User profiles with avatars
   - Team creation and management
   - Role-based access control (admin, member, viewer)
   - Team invitations via email

3. **Real-Time Collaboration**
   - Live task updates across all users
   - Real-time notifications
   - Task comments and discussions
   - @mentions in comments
   - Activity feed showing team actions

4. **Project Organization**
   - Multiple projects per team
   - Kanban board view
   - List view with filters and sorting
   - Calendar view for due dates
   - Custom project templates

5. **Integrations**
   - GitHub integration (link tasks to PRs/issues)
   - Slack notifications
   - REST API for external integrations
   - Webhook support

### Non-Functional Requirements

- **Performance**: Page load < 2 seconds, API response < 200ms
- **Scalability**: Support 10,000+ concurrent users
- **Security**: HTTPS, encrypted data at rest, OWASP top 10 compliance
- **Availability**: 99.9% uptime SLA
- **Usability**: Intuitive UI, keyboard shortcuts, mobile responsive
- **Accessibility**: WCAG 2.1 AA compliance

---

## 🏗️ Technical Preferences

### Technology Stack

**Backend**:
- [x] Node.js with TypeScript
- [x] Express.js framework
- [x] PostgreSQL database
- [x] Redis for caching and sessions
- [x] Socket.io for real-time features
- [x] JWT authentication
- [x] Prisma ORM

**Frontend**:
- [x] React 18 with TypeScript
- [x] Next.js 14 (App Router)
- [x] Tailwind CSS for styling
- [x] React Query for data fetching
- [x] Zustand for state management
- [x] Socket.io client for real-time updates

**Infrastructure**:
- [x] Docker containers
- [x] Docker Compose for local development
- [x] Kubernetes for production
- [x] GitHub Actions for CI/CD
- [x] PostgreSQL (managed service)
- [x] Redis (managed service)

**Testing**:
- [x] Jest for unit tests
- [x] Supertest for API testing
- [x] React Testing Library for component tests
- [x] Playwright for E2E tests
- [x] 80%+ code coverage target

---

## 👥 User Roles & Permissions

| Role | Description | Key Permissions |
|------|-------------|-----------------|
| Admin | Team administrator | Full access: manage team, projects, users, billing |
| Project Manager | Project lead | Create/delete projects, assign tasks, manage project members |
| Developer | Team member | Create/edit tasks, comment, update own assignments |
| Viewer | Read-only access | View tasks and comments, no editing rights |

---

## 🔄 Key User Flows

### Flow 1: New User Onboarding
1. User signs up with email or OAuth (Google/GitHub)
2. User creates or joins a team via invitation link
3. System shows welcome tour highlighting key features
4. User creates their first project or is added to existing one
5. User creates their first task and explores board views

### Flow 2: Daily Task Management
1. User logs in and sees personalized dashboard
2. User views tasks assigned to them (filtered by priority)
3. User updates task status by dragging on Kanban board
4. User adds comments to task with progress updates
5. User receives real-time notifications when mentioned
6. User marks tasks complete and moves to done column

### Flow 3: Team Collaboration
1. Project manager creates new project with custom workflow
2. Manager invites team members and assigns roles
3. Manager creates tasks and assigns to team members
4. Team members receive notifications and start work
5. Members collaborate via task comments and @mentions
6. Manager tracks progress via dashboard and reports
7. Team conducts sprint review using completed tasks view

### Flow 4: Integration Workflow
1. Admin connects GitHub integration in team settings
2. Developer creates task linked to GitHub issue
3. Developer works on feature and opens pull request
4. Task automatically updates when PR is merged
5. Team receives Slack notification of task completion
6. Activity is logged in team activity feed

---

## 🗄️ Data Model (High-Level)

### User
- id: UUID
- email: string, unique
- name: string
- avatar_url: string, optional
- created_at: timestamp
- last_login: timestamp

### Team
- id: UUID
- name: string
- slug: string, unique
- created_at: timestamp
- owner_id: UUID (foreign key to User)

### Project
- id: UUID
- name: string
- description: text
- team_id: UUID (foreign key to Team)
- status: enum (active, archived)
- created_at: timestamp

### Task
- id: UUID
- title: string
- description: text
- status: enum (backlog, todo, in_progress, review, done)
- priority: enum (low, medium, high, urgent)
- project_id: UUID (foreign key to Project)
- assignee_id: UUID (foreign key to User), nullable
- creator_id: UUID (foreign key to User)
- due_date: timestamp, nullable
- estimated_hours: integer, nullable
- created_at: timestamp
- updated_at: timestamp

### Comment
- id: UUID
- content: text
- task_id: UUID (foreign key to Task)
- user_id: UUID (foreign key to User)
- created_at: timestamp

---

## 🔌 External Integrations

- [x] GitHub API: Link tasks to issues and pull requests
- [x] Slack API: Send notifications to channels
- [x] Google OAuth: Authentication
- [x] GitHub OAuth: Authentication
- [ ] Jira: Import/export tasks (future)
- [ ] Calendar sync: Google Calendar, Outlook (future)

---

## 📅 Timeline & Priorities

**Target Launch Date**: 3 months from project start

**Phase 1 (Month 1)** - MVP:
1. Core task CRUD operations
2. User authentication and basic teams
3. Kanban board view
4. Basic real-time updates
5. PostgreSQL database setup
6. Docker containerization

**Phase 2 (Month 2)** - Enhanced Features:
1. Comments and mentions
2. Task filters and search
3. Calendar and list views
4. Email notifications
5. GitHub integration
6. CI/CD pipeline

**Phase 3 (Month 3)** - Polish & Launch:
1. Slack integration
2. Advanced permissions
3. Performance optimization
4. E2E testing
5. Documentation
6. Production deployment

---

## 💰 Budget & Resources

**Budget**: $5,000 for infrastructure and services
- Managed PostgreSQL: $50/month
- Managed Redis: $30/month
- Kubernetes cluster: $150/month
- Domain and SSL: $20/year
- Monitoring services: $50/month
- OAuth application setup: Free

**Team Size**:
- 1 Full-stack developer (you!)
- AI agents for code generation
- Community beta testers

**Constraints**:
- 3-month timeline is fixed
- Must use TypeScript for type safety
- Must achieve 80% test coverage
- Must support 1000+ users at launch

---

## 📝 Additional Context

### Design Philosophy
- **Mobile-first**: Design for mobile, enhance for desktop
- **Keyboard-first**: Power users should rarely touch the mouse
- **Real-time by default**: All updates should propagate instantly
- **Offline-capable**: Progressive Web App with offline support
- **Accessible**: Screen reader friendly, keyboard navigable

### Success Metrics
- User onboarding completion rate > 80%
- Daily active users > 60% of total users
- Average session duration > 15 minutes
- Task completion rate > 70%
- API response time p95 < 200ms
- Zero downtime deployments

### Competitive Advantage
- **Simplicity**: Easy to learn, powerful when needed
- **Speed**: Fastest task management tool on the market
- **Integration**: Deep GitHub integration for dev teams
- **Real-time**: True real-time collaboration without page refreshes
- **Open architecture**: REST API and webhooks for customization

---

## ✅ Completion Checklist

- [x] All required sections completed
- [x] Technical preferences selected
- [x] User roles defined
- [x] Key flows documented
- [x] Data model outlined
- [x] Timeline established
- [x] Ready for AI agents to start implementation

---

**Next Step**: Provide this PROJECT_BRIEF.md to your AI coding assistant with the prompt:

```
I've filled out PROJECT_BRIEF.md for a task management application.
Please generate the complete project following the guidelines in
.agents/project-rules.md. Include:
- Complete backend API with TypeScript/Express
- Frontend with React/Next.js
- Database schema and migrations
- Docker configuration
- Tests and documentation
- CI/CD pipeline
```

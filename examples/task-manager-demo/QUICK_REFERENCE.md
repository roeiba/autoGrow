# Quick Reference - TaskFlow Demo

> **Fast lookup guide for the Task Manager demo project**

## File Structure Overview

```
task-manager-demo/
├── PROJECT_BRIEF.md          # ⭐ Requirements document (start here)
├── GUIDE.md                  # 📖 Step-by-step generation walkthrough
├── README.md                 # 📄 Project overview and setup
├── QUICK_REFERENCE.md        # 📌 This file
│
├── backend/                  # Node.js/Express API
│   ├── src/
│   │   ├── server.ts         # Main entry point
│   │   ├── models/           # Data models (User, Task, Project)
│   │   ├── services/         # Business logic (auth, tasks)
│   │   ├── controllers/      # Request handlers
│   │   ├── routes/           # API routes
│   │   ├── middleware/       # Auth, validation, error handling
│   │   └── config/           # Configuration
│   ├── tests/                # Unit & integration tests
│   ├── package.json
│   └── .env.example          # Environment variables template
│
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── hooks/            # Custom hooks (useAuth, useTasks)
│   │   ├── services/         # API clients
│   │   └── pages/            # Page components
│   ├── tests/                # Component & E2E tests
│   └── package.json
│
├── deployment/               # DevOps configs
│   ├── docker-compose.yml    # Local development
│   └── kubernetes/           # K8s manifests
│
└── docs/                     # Documentation
    ├── API.md                # API reference
    ├── ARCHITECTURE.md       # System design
    └── DEPLOYMENT.md         # Deployment guide
```

## Key Files to Explore

### 1. Requirements (Input)
- `PROJECT_BRIEF.md` - The complete requirements that AI used to generate everything

### 2. Generated Code (Output)
- `backend/src/server.ts` - Express server setup
- `backend/src/services/auth.service.ts` - Authentication logic
- `backend/src/models/User.ts` - User data model
- `frontend/src/hooks/useAuth.tsx` - Auth context and hooks
- `frontend/src/components/tasks/TaskCard.tsx` - Task UI component

### 3. Infrastructure
- `deployment/docker-compose.yml` - Run entire stack locally
- `backend/.env.example` - Required environment variables

### 4. Documentation
- `GUIDE.md` - Detailed walkthrough of AI generation process
- `README.md` - Setup and usage instructions

## Quick Commands

### Run with Docker (Easiest)
```bash
cd examples/task-manager-demo/
docker-compose -f deployment/docker-compose.yml up -d
```

### Backend Only
```bash
cd backend/
npm install
cp .env.example .env
# Edit .env with your database credentials
npm run migrate
npm run dev
```

### Frontend Only
```bash
cd frontend/
npm install
npm run dev
```

### Run Tests
```bash
# Backend tests
cd backend/
npm test

# Frontend tests
cd frontend/
npm test

# E2E tests
npm run test:e2e
```

## API Endpoints Reference

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Tasks
- `GET /api/tasks` - List tasks (with filters)
- `POST /api/tasks` - Create task
- `GET /api/tasks/:id` - Get task details
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task

### Projects
- `GET /api/projects` - List projects
- `POST /api/projects` - Create project
- `GET /api/projects/:id` - Get project details

### WebSocket Events
- `task:created` - New task created
- `task:updated` - Task modified
- `task:assigned` - Task assigned to user
- `comment:added` - New comment on task

## Tech Stack at a Glance

**Backend:**
- Node.js 18+ with TypeScript
- Express.js web framework
- PostgreSQL database
- Redis for caching
- Socket.io for real-time
- JWT authentication

**Frontend:**
- React 18+ with TypeScript
- Vite build tool
- TailwindCSS styling
- React Query for data
- Socket.io client

**DevOps:**
- Docker containerization
- Docker Compose orchestration
- Kubernetes configs
- GitHub Actions CI/CD

## Environment Variables

### Backend (.env)
```bash
NODE_ENV=development
PORT=8000
DATABASE_URL=postgres://user:pass@localhost:5432/taskflow
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## Common Use Cases

### Learning the Generation Process
1. Read `PROJECT_BRIEF.md` first
2. Follow `GUIDE.md` for step-by-step explanation
3. Examine generated code in `backend/src/` and `frontend/src/`
4. Run the application to see it work

### Using as Template for Your Project
1. Copy `PROJECT_BRIEF.md` structure
2. Replace content with your requirements
3. Give to AI assistant with generation prompt
4. Review and customize generated code

### Understanding Specific Features
- **Authentication**: See `backend/src/services/auth.service.ts`
- **Real-time**: See `backend/src/websocket.ts`
- **React Hooks**: See `frontend/src/hooks/useAuth.tsx`
- **Task Management**: See `frontend/src/components/tasks/`

### Testing Locally
1. Start with Docker: `docker-compose up -d`
2. Access frontend: http://localhost:3000
3. API docs: http://localhost:8000/api-docs
4. Register account and explore features

## Key Concepts Demonstrated

### AI Generation Patterns
- How detailed requirements lead to accurate code
- AI's approach to architecture decisions
- Pattern consistency throughout codebase
- Proper error handling and validation
- Test coverage strategies

### Best Practices
- Clean architecture with separation of concerns
- Type safety with TypeScript
- RESTful API design
- React hooks and composition
- Docker containerization
- Environment-based configuration
- Comprehensive testing

### Production Readiness
- Authentication and authorization
- Input validation
- Error handling
- Logging and monitoring
- Security middleware (helmet, CORS, rate limiting)
- Database migrations
- CI/CD pipelines

## Customization Points

### Change Tech Stack
Update in `PROJECT_BRIEF.md`:
```markdown
Backend: Python + Django
Frontend: Vue.js + Nuxt
Database: MongoDB
```

### Add Features
Add to functional requirements:
```markdown
5. Time Tracking
   - Track time spent on tasks
   - Generate time reports
   - Export to CSV/PDF
```

### Modify Data Model
Update data model section:
```markdown
TimeEntry:
- id, task_id, user_id, start_time, end_time, duration
```

### Adjust Architecture
Change non-functional requirements:
```markdown
- Microservices architecture
- Support 10,000+ concurrent users
- Multi-region deployment
```

## Troubleshooting

### Port Already in Use
```bash
# Change ports in docker-compose.yml or .env files
# Backend: PORT=8001
# Frontend: Change in vite.config.ts
```

### Database Connection Failed
```bash
# Ensure PostgreSQL is running
docker-compose ps

# Check DATABASE_URL in .env
# Format: postgres://user:password@host:port/database
```

### Build Errors
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Docker cache
docker-compose down -v
docker-compose build --no-cache
```

## Additional Resources

- **Main Template README**: [../../README.md](../../README.md)
- **Template Guidelines**: [../../.agents/project-rules.md](../../.agents/project-rules.md)
- **Contributing**: [../../CONTRIBUTING.md](../../CONTRIBUTING.md)

## Getting Help

- **Understand generation**: Read [GUIDE.md](GUIDE.md)
- **Setup issues**: Check [README.md](README.md)
- **API questions**: See `docs/API.md`
- **Architecture**: See `docs/ARCHITECTURE.md`
- **General questions**: [GitHub Discussions](https://github.com/roeiba/ai-project-template/discussions)

---

**Pro Tip**: This demo is fully functional! Deploy it, customize it, or use it as a learning resource. The code quality is production-ready, generated entirely by AI from the PROJECT_BRIEF.md requirements.

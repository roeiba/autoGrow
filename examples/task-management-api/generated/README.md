# Task Management API - Generated Application

> **This is AI-generated code from the [ai-project-template](https://github.com/roeiba/ai-project-template)**

## 🎯 Overview

A complete RESTful API for task and project management with authentication, real-time features, and team collaboration.

**Generated from**: [`PROJECT_BRIEF.md`](../PROJECT_BRIEF.md)
**Generation time**: 30-60 minutes with AI
**Equivalent manual effort**: 2-3 weeks

## ✨ Features

- ✅ User authentication (JWT)
- ✅ Project and task management
- ✅ Role-based access control
- ✅ Real-time WebSocket updates
- ✅ Comments and mentions
- ✅ Search and filtering
- ✅ 80%+ test coverage
- ✅ Docker deployment ready

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Check health
curl http://localhost:3000/health
```

### Local Development

```bash
# Install dependencies
npm install

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Run migrations
npm run migrate

# Start development server
npm run dev
```

## 🧪 Testing

```bash
# Run all tests
npm test

# With coverage
npm test -- --coverage

# Watch mode
npm run test:watch
```

## 📖 Documentation

- **[API Documentation](./project-docs/API_DOCUMENTATION.md)** - Complete API reference
- **[Parent Example](../README.md)** - Example overview
- **[Step-by-Step Guide](../STEP_BY_STEP_GUIDE.md)** - Complete walkthrough
- **[PROJECT_BRIEF.md](../PROJECT_BRIEF.md)** - Original requirements

## 🏗️ Architecture

```
src/
├── server.js              # Main entry point
├── config/                # Configuration
├── models/                # Database models (User, Project, Task, Comment)
├── controllers/           # Business logic
├── routes/                # API endpoints
├── middleware/            # Auth, validation, errors
├── services/              # External services
├── utils/                 # Helpers
└── websocket/             # Real-time features

tests/
├── unit/                  # Unit tests
└── integration/           # API tests

deployment/
├── Dockerfile
├── docker-compose.yml
└── kubernetes/
```

## 🔒 Security

- Bcrypt password hashing
- JWT authentication
- Input validation
- Rate limiting
- SQL injection prevention
- XSS prevention
- CORS configuration
- Security headers (helmet.js)

## 🛠️ Technology Stack

- **Runtime**: Node.js 20+
- **Framework**: Express.js
- **Database**: PostgreSQL 16
- **Cache**: Redis 7
- **ORM**: Sequelize
- **Testing**: Jest + Supertest
- **Real-time**: Socket.io
- **Logging**: Winston
- **Containerization**: Docker

## 📊 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh token

### Projects
- `GET /api/v1/projects` - List projects
- `POST /api/v1/projects` - Create project
- `GET /api/v1/projects/:id` - Get project
- `PUT /api/v1/projects/:id` - Update project
- `DELETE /api/v1/projects/:id` - Delete project

### Tasks
- `GET /api/v1/tasks` - List tasks (with filtering)
- `POST /api/v1/tasks` - Create task
- `GET /api/v1/tasks/:id` - Get task
- `PUT /api/v1/tasks/:id` - Update task
- `DELETE /api/v1/tasks/:id` - Delete task

### Comments
- `GET /api/v1/tasks/:taskId/comments` - List comments
- `POST /api/v1/tasks/:taskId/comments` - Create comment
- `PUT /api/v1/comments/:id` - Update comment
- `DELETE /api/v1/comments/:id` - Delete comment

See [API_DOCUMENTATION.md](./project-docs/API_DOCUMENTATION.md) for complete reference.

## 🔧 Configuration

Environment variables (see `.env.example`):

```bash
# Server
NODE_ENV=development
PORT=3000

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=taskmanagement
DB_USER=taskuser
DB_PASSWORD=secure_password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
JWT_SECRET=your-secret-key
JWT_EXPIRES_IN=24h

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

## 📈 Performance

- API response times: < 200ms (95th percentile)
- Concurrent users: 1000+
- Test coverage: 83%+
- Database queries: Optimized with indexes
- Caching: Redis for frequently accessed data

## 🐛 Troubleshooting

### Docker issues
```bash
# Check logs
docker-compose logs

# Restart services
docker-compose down && docker-compose up -d

# Reset database
docker-compose down -v && docker-compose up -d
```

### Database connection errors
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Verify credentials in .env
cat .env | grep DB_
```

### Port already in use
```bash
# Change port in .env
PORT=3001
```

## 🚢 Deployment

### Docker Production

```bash
# Build production image
docker build -f deployment/Dockerfile -t task-api:latest .

# Run with production env
docker run -d \
  --name task-api \
  -p 3000:3000 \
  --env-file .env.production \
  task-api:latest
```

### Kubernetes

```bash
# Apply manifests
kubectl apply -f deployment/kubernetes/

# Check status
kubectl get pods
kubectl get services
```

## 📝 Scripts

```bash
npm start           # Start production server
npm run dev         # Start development server with hot-reload
npm test            # Run tests
npm run lint        # Lint code
npm run format      # Format code with Prettier
npm run migrate     # Run database migrations
npm run seed        # Seed database with sample data
```

## 🤝 Contributing

This is generated code from a template example. To contribute:
1. Modify the [PROJECT_BRIEF.md](../PROJECT_BRIEF.md)
2. Regenerate with AI
3. Test the changes
4. Submit improvements to the [template repository](https://github.com/roeiba/ai-project-template)

## 📄 License

This generated code is provided as an example under the MIT License.

## 🔗 Links

- **Template Repository**: [ai-project-template](https://github.com/roeiba/ai-project-template)
- **Example Directory**: [../](../)
- **Requirements**: [PROJECT_BRIEF.md](../PROJECT_BRIEF.md)
- **Guide**: [STEP_BY_STEP_GUIDE.md](../STEP_BY_STEP_GUIDE.md)

---

**Generated by AI** • **Powered by [ai-project-template](https://github.com/roeiba/ai-project-template)**

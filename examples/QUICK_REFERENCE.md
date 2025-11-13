# Quick Reference: AI Project Generation

> **One-page guide to generating projects with the AI-Optimized Template**

---

## 🚀 3-Minute Quick Start

```bash
# 1. Clone template
git clone https://github.com/roeiba/ai-project-template.git my-project
cd my-project

# 2. Fill PROJECT_BRIEF.md (see template below)

# 3. Provide to AI
"I've filled out PROJECT_BRIEF.md. Generate the complete project following
.agents/project-rules.md guidelines. Create production-ready code with tests,
documentation, and deployment configurations."

# 4. Review and run
cd src/backend && npm install && npm test && docker-compose up
```

---

## 📝 PROJECT_BRIEF.md Template

### Minimum Required Sections

```markdown
# Project Brief

## 🎯 Project Overview
**Project Name**: [Your Project Name]
**Brief Description**: [What it does in 2-3 sentences]
**Problem Statement**: [What problem does it solve?]
**Target Users**: [Who will use it?]

## 📋 Core Requirements

### Functional Requirements
1. [Feature 1 with details]
2. [Feature 2 with details]
3. [Feature 3 with details]

### Non-Functional Requirements
- Performance: [Response times, concurrent users]
- Security: [Authentication, authorization, data protection]
- Scalability: [Growth expectations]

## 🏗️ Technical Preferences
**Backend**: [Node.js/Python/Go/Java]
**Database**: [PostgreSQL/MongoDB/MySQL]
**Authentication**: [JWT/OAuth/Sessions]
**Testing**: [Jest/Pytest/Go test]
**DevOps**: [Docker/Kubernetes/Cloud provider]

## 🗄️ Data Model (High-Level)
### Entity1
- field1: type, description
- field2: type, description
- Relationships: [what it relates to]

### Entity2
- field1: type, description
- field2: type, description

## 📊 API Endpoints Overview (if applicable)
- GET /api/v1/resource
- POST /api/v1/resource
- PUT /api/v1/resource/:id
- DELETE /api/v1/resource/:id

## ✅ Completion Checklist
- [ ] All required sections completed
- [ ] Technical preferences selected
- [ ] Ready for AI generation
```

---

## 🤖 AI Prompt Templates

### Basic Generation
```
I've filled out PROJECT_BRIEF.md. Please generate the complete project
following the guidelines in .agents/project-rules.md. Create:
1. Complete application code
2. Comprehensive tests (80%+ coverage)
3. API documentation
4. Docker deployment setup
5. CI/CD pipeline configuration

Follow best practices for security, performance, and maintainability.
```

### Specific Technology Stack
```
Generate a [Node.js/Python/Go] application based on PROJECT_BRIEF.md:
- Use [Express/FastAPI/Gin] framework
- [PostgreSQL/MongoDB] database
- [Jest/Pytest] for testing
- Docker containerization
- Production-ready with logging and monitoring

Follow .agents/project-rules.md guidelines.
```

### Add Feature to Existing Project
```
Add [feature name] to the existing project:
- Requirements: [specific requirements]
- Should integrate with: [existing components]
- Include tests and documentation
- Follow existing code patterns
```

### Fix or Refactor
```
[Fix/Refactor] [component name]:
- Issue: [describe the problem]
- Expected behavior: [what should happen]
- Maintain existing tests
- Update documentation if needed
```

---

## 📊 What Gets Generated

### Backend API
```
src/backend/
├── server.js              # Entry point
├── config/                # Configuration
├── models/                # Database models
├── controllers/           # Business logic
├── routes/                # API endpoints
├── middleware/            # Auth, validation, errors
├── services/              # External services
└── utils/                 # Helpers

tests/                     # Test suite
deployment/               # Docker, K8s
project-docs/             # Documentation
```

### Frontend App
```
src/frontend/
├── public/               # Static assets
├── src/
│   ├── components/       # React/Vue components
│   ├── pages/            # Route pages
│   ├── hooks/            # Custom hooks
│   ├── services/         # API clients
│   ├── store/            # State management
│   └── utils/            # Helpers
├── tests/                # Component tests
└── package.json
```

---

## ⚡ Common Commands

### Running Generated Projects

```bash
# Docker (recommended)
docker-compose up -d
docker-compose logs -f
docker-compose down

# Local development
npm install          # or pip install -r requirements.txt
npm run dev          # or python main.py
npm test             # or pytest
npm run lint         # or pylint

# Database
npm run migrate      # Run migrations
npm run seed         # Seed data
```

### Testing

```bash
npm test                    # Run all tests
npm test -- --coverage      # With coverage
npm test -- --watch         # Watch mode
npm test -- path/to/file    # Specific file
```

### Docker

```bash
docker-compose up -d        # Start all services
docker-compose ps           # Check status
docker-compose logs api     # View logs
docker-compose exec api sh  # Shell into container
docker-compose down -v      # Stop and remove volumes
```

---

## 🎯 Best Practices

### ✅ Do This

- **Be specific** in requirements
  - ❌ "Add authentication"
  - ✅ "Add JWT authentication with email verification, password reset, and 2FA"

- **Include context**
  - ❌ "Build a task manager"
  - ✅ "Build a task manager for development teams tracking sprint work, supporting priorities, assignments, and comments"

- **Specify constraints**
  - ✅ "Must support 1000 concurrent users"
  - ✅ "API responses under 200ms"
  - ✅ "Deploy to AWS"

- **Review generated code**
  - ✅ Check security-critical sections
  - ✅ Validate business logic
  - ✅ Run all tests

### ❌ Avoid This

- Vague requirements
- Missing technical preferences
- No success criteria
- Skipping code review
- Not testing before deployment

---

## 🔍 Code Review Checklist

When reviewing AI-generated code:

### Security
- [ ] Passwords are hashed (bcrypt/argon2)
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] Authentication required on protected routes
- [ ] Rate limiting implemented
- [ ] No secrets in code

### Code Quality
- [ ] Clear, descriptive naming
- [ ] Functions are small and focused
- [ ] No code duplication
- [ ] Error handling present
- [ ] Logging implemented
- [ ] Comments explain "why" not "what"

### Testing
- [ ] Unit tests for models/services
- [ ] Integration tests for APIs
- [ ] Edge cases covered
- [ ] 80%+ code coverage
- [ ] All tests passing

### Documentation
- [ ] README with setup instructions
- [ ] API documentation complete
- [ ] Code comments where needed
- [ ] Environment variables documented

---

## 🐛 Troubleshooting

### Generation Issues

**AI generates incomplete code**
→ Make PROJECT_BRIEF.md more detailed
→ Ask AI to "complete the implementation"

**AI misunderstands requirements**
→ Be more specific in PROJECT_BRIEF.md
→ Provide examples of expected behavior

**Generated code doesn't match tech stack**
→ Clearly specify technology preferences
→ Include specific framework/library names

### Runtime Issues

**Docker container won't start**
```bash
docker-compose logs [service-name]
docker-compose down -v && docker-compose up -d
```

**Tests failing**
```bash
# Check test output for specific errors
npm test -- --verbose

# Ensure test database is configured
cat .env.test
```

**API returns errors**
```bash
# Check logs
docker-compose logs api

# Verify environment variables
docker-compose exec api env | grep DB_

# Test database connection
docker-compose exec api npm run migrate
```

---

## 📚 Key Files Reference

| File | Purpose | When to Update |
|------|---------|----------------|
| `PROJECT_BRIEF.md` | Requirements document | Before generation, when requirements change |
| `.env` | Environment configuration | Local setup, deployment |
| `.agents/project-rules.md` | AI guidelines | When customizing AI behavior |
| `package.json` | Dependencies | When adding new libraries |
| `docker-compose.yml` | Local development | When adding services |
| `README.md` | Project documentation | After generation, keep updated |

---

## 🎓 Learning Path

### Beginner
1. Study [Task Management API example](./task-management-api/)
2. Read [STEP_BY_STEP_GUIDE.md](./task-management-api/STEP_BY_STEP_GUIDE.md)
3. Follow the example to generate your first project
4. Make small modifications and regenerate

### Intermediate
1. Write your own PROJECT_BRIEF.md from scratch
2. Generate a complete application
3. Add new features using AI
4. Deploy to production

### Advanced
1. Customize `.agents/project-rules.md` for your team
2. Create your own example projects
3. Contribute back to the template
4. Build internal tools using the template

---

## 💡 Pro Tips

1. **Start Simple**: Begin with core features, add complexity later
2. **Iterate Fast**: Generate → Review → Modify → Regenerate
3. **Use Examples**: Copy and adapt from existing examples
4. **Document Everything**: Keep PROJECT_BRIEF.md updated
5. **Test Early**: Run tests after every generation
6. **Version Control**: Commit after each successful generation
7. **Security First**: Always review auth and data handling code

---

## 🔗 Quick Links

- **Main Template**: [github.com/roeiba/ai-project-template](https://github.com/roeiba/ai-project-template)
- **Examples**: [./examples/](./examples/)
- **Issues**: [github.com/roeiba/ai-project-template/issues](https://github.com/roeiba/ai-project-template/issues)
- **Discussions**: [github.com/roeiba/ai-project-template/discussions](https://github.com/roeiba/ai-project-template/discussions)

---

## 📞 Getting Help

1. Check [examples/](./examples/) for similar projects
2. Review [STEP_BY_STEP_GUIDE.md](./task-management-api/STEP_BY_STEP_GUIDE.md)
3. Ask AI for clarification: "Explain the architecture of the generated code"
4. Open an issue on GitHub
5. Join discussions

---

<div align="center">

**Ready to build?**

Start with [Task Management API Example](./task-management-api/) →

*Generate production-ready code in minutes, not weeks*

</div>

# Examples Guide

> **How to use the example projects to learn and build your own AI-generated applications**

## Overview

The examples directory contains complete, working projects that demonstrate the full AI-driven project generation workflow. Each example shows:

1. **Requirements Definition** - A filled-out PROJECT_BRIEF.md
2. **Generated Code** - Complete application code created by AI
3. **Documentation** - Comprehensive guides and references
4. **Infrastructure** - Deployment configurations
5. **Tests** - Full test suite

## Available Examples

### Task Manager Demo
**Path**: `examples/task-manager-demo/`
**Stack**: Node.js + Express + React + PostgreSQL
**Complexity**: Medium
**What it demonstrates**: Full-stack web application with authentication, real-time features, and modern DevOps practices

## How to Use These Examples

### For Learning

#### 1. Understand the Input (PROJECT_BRIEF.md)
```bash
cd examples/task-manager-demo/
cat PROJECT_BRIEF.md
```

**Key things to notice:**
- How requirements are structured
- Level of detail provided
- Technology choices and justifications
- Data model definition
- User flows and use cases

#### 2. Study the Generation Process (GUIDE.md)
```bash
cat GUIDE.md
```

**What you'll learn:**
- How AI analyzes requirements
- Architecture decision-making process
- Code generation patterns
- Testing strategies
- DevOps automation

#### 3. Explore the Generated Code
```bash
# Backend structure
ls -R backend/src/

# Frontend structure
ls -R frontend/src/

# Infrastructure
cat deployment/docker-compose.yml
```

**Pay attention to:**
- Code organization and patterns
- Type safety implementation
- Error handling approach
- Testing structure
- Documentation quality

#### 4. Run the Application
```bash
docker-compose -f deployment/docker-compose.yml up -d
```

**Experience:**
- See the generated code in action
- Test features described in PROJECT_BRIEF.md
- Verify quality and completeness
- Understand real-world applicability

### For Your Own Projects

#### Step 1: Choose a Similar Example
Find an example that matches your:
- Technology preferences
- Application type
- Complexity level
- Domain (if applicable)

#### Step 2: Copy the PROJECT_BRIEF.md Template
```bash
cp examples/task-manager-demo/PROJECT_BRIEF.md my-project-brief.md
```

#### Step 3: Customize the Requirements

**Replace these sections:**
- Project Overview (name, description, problem)
- Core Requirements (your features)
- Data Model (your entities)
- User Flows (your workflows)
- Technology Stack (if different)

**Keep the structure:**
- Section organization
- Level of detail
- Format and clarity

#### Step 4: Generate Your Project

Provide to your AI assistant:
```
I've filled out PROJECT_BRIEF.md with requirements for [your project].
Please generate the complete project following the guidelines in
.agents/project-rules.md from the ai-project-template.

Generate:
1. Complete [backend/frontend/mobile] application
2. Database schema and migrations
3. Docker and deployment configurations
4. CI/CD pipeline setup
5. Comprehensive documentation
6. Test suite with >80% coverage
7. README with setup instructions
```

#### Step 5: Review and Refine

**Check generated code for:**
- Correctness and completeness
- Security best practices
- Performance considerations
- Test coverage
- Documentation quality

**Make adjustments:**
- Update environment variables
- Configure third-party services
- Customize business logic
- Add domain-specific validation

## Learning Paths

### Path 1: For Understanding AI Generation

**Goal**: Learn how AI generates production-ready code

1. Read task-manager-demo/PROJECT_BRIEF.md (30 min)
2. Read task-manager-demo/GUIDE.md (60 min)
3. Study backend/src/services/auth.service.ts (15 min)
4. Study frontend/src/hooks/useAuth.tsx (15 min)
5. Run the application locally (30 min)
6. Review tests in backend/tests/ (20 min)

**Total time**: ~2.5 hours

**Outcome**: Deep understanding of AI-driven development

### Path 2: For Quick Start

**Goal**: Get a working example running fast

1. Read task-manager-demo/README.md (10 min)
2. Read task-manager-demo/QUICK_REFERENCE.md (10 min)
3. Run with Docker Compose (5 min)
4. Test the application (15 min)
5. Explore code structure (20 min)

**Total time**: ~1 hour

**Outcome**: Working application and basic understanding

### Path 3: For Building Your Project

**Goal**: Create your own AI-generated project

1. Review task-manager-demo/PROJECT_BRIEF.md (20 min)
2. Draft your PROJECT_BRIEF.md (1-2 hours)
3. Generate with AI assistant (30-60 min)
4. Review and test generated code (2-3 hours)
5. Customize for your needs (varies)

**Total time**: ~4-6 hours for initial version

**Outcome**: Custom project tailored to your needs

## Example Deep Dives

### Authentication Implementation

**Files to study:**
- `backend/src/services/auth.service.ts` - Business logic
- `backend/src/middleware/auth.ts` - Request authentication
- `frontend/src/hooks/useAuth.tsx` - Client-side auth
- `backend/tests/services/auth.service.test.ts` - Tests

**Key concepts:**
- JWT token generation and verification
- Password hashing with bcrypt
- Context API for React state
- Token storage strategies
- Error handling

### Real-time Features

**Files to study:**
- `backend/src/websocket.ts` - WebSocket setup
- `frontend/src/hooks/useWebSocket.ts` - Client connection
- `backend/src/server.ts` - Socket.io integration

**Key concepts:**
- WebSocket authentication
- Event-driven architecture
- Real-time updates
- Connection management
- Error handling and reconnection

### Database Design

**Files to study:**
- `backend/database/migrations/` - Schema definitions
- `backend/src/models/` - Data models
- `backend/src/services/` - Data access

**Key concepts:**
- Relational schema design
- Foreign key relationships
- Indexes for performance
- Migration management
- Query optimization

### Testing Strategy

**Files to study:**
- `backend/tests/services/` - Unit tests
- `backend/tests/integration/` - Integration tests
- `frontend/tests/e2e/` - End-to-end tests

**Key concepts:**
- Testing pyramid
- Mocking and test isolation
- Test data management
- Coverage requirements
- CI/CD integration

## Common Questions

### Q: How much of this code is AI-generated?
**A**: 95%+. Only minor adjustments for environment-specific configurations and secrets were made by humans.

### Q: Is this production-ready?
**A**: Yes, with proper configuration. The code follows best practices and includes security, testing, and monitoring. You'll need to:
- Set up proper secrets management
- Configure production databases
- Set up monitoring and logging
- Perform security audits
- Load test for your scale

### Q: Can I use this code in my project?
**A**: Absolutely! It's MIT licensed. Use it as:
- A learning resource
- A starting point for your project
- A reference implementation
- A template to customize

### Q: What if I want different technologies?
**A**: Modify the PROJECT_BRIEF.md technology stack section. AI will generate code for your chosen stack following similar patterns.

### Q: How do I add features?
**A**: Either:
1. Update PROJECT_BRIEF.md and regenerate
2. Ask AI to add features to existing code
3. Manually add features following existing patterns

### Q: Are there examples for other stacks?
**A**: Currently one example. More coming:
- Python + Django + Vue.js
- Go + React
- Mobile app (React Native)
- Microservices architecture

Contributions welcome!

## Tips for Success

### Writing Good Requirements

**Do:**
- ✅ Be specific and detailed
- ✅ Include data models
- ✅ Define user flows
- ✅ Specify tech stack with versions
- ✅ Include non-functional requirements

**Don't:**
- ❌ Be vague ("make it fast", "user-friendly")
- ❌ Skip data relationships
- ❌ Ignore edge cases
- ❌ Forget about error handling
- ❌ Omit security requirements

### Working with AI

**Do:**
- ✅ Generate in phases (backend → frontend → tests)
- ✅ Review code as it's generated
- ✅ Ask for explanations when unclear
- ✅ Request changes if needed
- ✅ Test thoroughly

**Don't:**
- ❌ Accept all code blindly
- ❌ Skip code review
- ❌ Ignore security concerns
- ❌ Deploy without testing
- ❌ Forget to customize for your needs

### Customizing Generated Code

**Recommended approach:**
1. Run generated code first
2. Understand the architecture
3. Make small, incremental changes
4. Test after each change
5. Document your modifications

**Avoid:**
- Large rewrites before understanding
- Breaking established patterns
- Removing error handling
- Skipping tests for new code

## Contributing Examples

Want to add a new example? Great! Follow these guidelines:

### Requirements

1. **Complete PROJECT_BRIEF.md** - Well-defined requirements
2. **Working code** - Tested and functional
3. **Comprehensive GUIDE.md** - Step-by-step walkthrough
4. **Good README.md** - Setup and usage instructions
5. **Tests** - At least 70% coverage
6. **Documentation** - API docs, architecture, deployment

### Suggested Examples

**Most wanted:**
- Python/Django backend with Vue.js frontend
- Go microservices architecture
- Mobile app (React Native or Flutter)
- Machine learning integration
- Serverless architecture (AWS Lambda, etc.)
- E-commerce platform
- Social media application
- Content management system

**See**: [CONTRIBUTING.md](../CONTRIBUTING.md) for submission process

## Resources

### Within This Repository
- [Main README](../README.md) - Template overview
- [PROJECT_BRIEF.md](../PROJECT_BRIEF.md) - Blank template
- [.agents/project-rules.md](../.agents/project-rules.md) - AI guidelines
- [QUICKSTART.md](../QUICKSTART.md) - Getting started

### External Resources
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [The Twelve-Factor App](https://12factor.net/)
- [REST API Design](https://restfulapi.net/)
- [Testing Best Practices](https://testingjavascript.com/)

## Next Steps

1. **Explore** the task-manager-demo example
2. **Run** it locally to see it in action
3. **Study** the GUIDE.md to understand the process
4. **Draft** your own PROJECT_BRIEF.md
5. **Generate** your first AI-created project!

## Support

**Questions about examples?**
- Read the example's README.md
- Check QUICK_REFERENCE.md for fast answers
- Review GUIDE.md for detailed explanations
- Open a [Discussion](https://github.com/roeiba/ai-project-template/discussions)

**Found a bug in an example?**
- Open an [Issue](https://github.com/roeiba/ai-project-template/issues)
- Include: example name, steps to reproduce, expected vs actual behavior

**Want to contribute?**
- See [CONTRIBUTING.md](../CONTRIBUTING.md)
- All contributions welcome!

---

**Happy building!** The examples are here to help you understand and leverage AI-driven development. Start exploring and see how AI can accelerate your projects.

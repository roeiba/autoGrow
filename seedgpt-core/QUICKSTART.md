# Quick Start Guide

> Get from zero to a complete project in 3 steps

## For Humans 👤

### Step 1: Get the Template (30 seconds)

```bash
git clone <repository-url> my-awesome-project
cd my-awesome-project
```

### Step 2: Describe Your Project (10-30 minutes)

Open `PROJECT_BRIEF.md` and fill it out. This is the **ONLY** file you need to edit.

**What to include:**
- Project name and description
- What problem you're solving
- Key features you need
- Technology preferences (Node.js? Python? React? Vue?)
- User roles and permissions
- Timeline and priorities

**Example:**
```markdown
**Project Name**: TaskMaster Pro

**Brief Description**: 
A team task management system with real-time collaboration

**Problem Statement**:
Teams struggle to coordinate tasks across multiple projects

**Core Requirements**:
1. User authentication and authorization
2. Create, assign, and track tasks
3. Real-time updates when tasks change
4. Team collaboration features
5. Dashboard with analytics
```

### Step 3: Let AI Build It (Give this prompt to your AI assistant)

```
I've filled out PROJECT_BRIEF.md with my project requirements.
Please read it and generate the complete project following the
guidelines in .agents/project-rules.md.

Start by:
1. Reading PROJECT_BRIEF.md thoroughly
2. Creating a session log in .ai-prompts/sessions/
3. Determining which applications are needed (backend, frontend, mobile, etc.)
4. Generating the appropriate src/ structure with working code
5. Creating comprehensive documentation in project-docs/
6. Setting up CI/CD and deployment configurations
7. Creating initial tasks in tasks/active/

Follow all guidelines in .agents/project-rules.md and document
everything in your session log.
```

**That's it!** The AI will generate:
- ✅ Complete application code in `src/`
- ✅ Full documentation in `project-docs/`
- ✅ Tests and quality checks
- ✅ CI/CD pipelines
- ✅ Deployment configurations
- ✅ Initial task breakdown

---

## For AI Agents 🤖

### You've Been Given a PROJECT_BRIEF.md - Now What?

**Your Mission:** Generate a complete, production-ready project from the requirements.

### Generation Checklist

#### Phase 1: Understand (5 minutes)
- [ ] Read `PROJECT_BRIEF.md` completely
- [ ] Read `.agents/project-rules.md` for guidelines
- [ ] Create session log: `.ai-prompts/sessions/YYYY-MM-DD_initial-generation.md`
- [ ] Identify which apps are needed (backend? frontend? mobile?)
- [ ] Choose appropriate tech stack

#### Phase 2: Plan (10 minutes)
- [ ] Document tech stack decision in `project-docs/architecture/decisions/001-tech-stack.md`
- [ ] Plan folder structure for `src/`
- [ ] Identify external integrations needed
- [ ] Plan database schema
- [ ] Outline API endpoints

#### Phase 3: Generate Documentation (15 minutes)
- [ ] Create `project-docs/knowledge_base/requirements/functional.md`
- [ ] Create `project-docs/knowledge_base/requirements/non-functional.md`
- [ ] Create `project-docs/knowledge_base/domain/concepts.md`
- [ ] Create `project-docs/architecture/overview/system-context.md`
- [ ] Create `project-docs/architecture/overview/tech-stack.md`

#### Phase 4: Generate Code (30-60 minutes)
- [ ] Create backend application (if needed)
  - [ ] Project setup (package.json, dependencies)
  - [ ] Folder structure (api/, core/, services/, data/)
  - [ ] Authentication & authorization
  - [ ] Core business logic
  - [ ] Database models and migrations
  - [ ] API endpoints
  - [ ] .env.example with all required variables
- [ ] Create frontend application (if needed)
  - [ ] Project setup
  - [ ] Component structure
  - [ ] Pages and routing
  - [ ] State management
  - [ ] API integration
  - [ ] .env.example
- [ ] Create mobile application (if needed)
- [ ] Create shared libraries (if needed)

#### Phase 5: Generate Tests (20 minutes)
- [ ] Unit tests for business logic
- [ ] Integration tests for APIs
- [ ] E2E tests for critical flows
- [ ] Test configuration and scripts

#### Phase 6: Infrastructure (15 minutes)
- [ ] Docker configurations in `deployment/docker/`
- [ ] CI/CD pipeline in `deployment/ci-cd/`
- [ ] Kubernetes manifests (if needed)
- [ ] Monitoring setup

#### Phase 7: Tasks & Finalization (10 minutes)
- [ ] Create initial tasks in `tasks/active/`
- [ ] Update main README.md with project-specific info
- [ ] Complete session log with all work done
- [ ] Verify everything is documented

### Quality Checklist

Before you finish, verify:

**Code Quality**
- [ ] All code follows project guidelines
- [ ] No hardcoded secrets or credentials
- [ ] Error handling is comprehensive
- [ ] Code is well-commented
- [ ] Naming is clear and consistent

**Testing**
- [ ] >80% test coverage
- [ ] All tests pass
- [ ] Edge cases are covered

**Documentation**
- [ ] README.md is project-specific
- [ ] All APIs are documented
- [ ] Setup instructions are clear
- [ ] Architecture is documented

**Security**
- [ ] Authentication implemented correctly
- [ ] Input validation on all endpoints
- [ ] Secrets use environment variables
- [ ] Security headers configured

**Deployment**
- [ ] Docker builds successfully
- [ ] CI/CD pipeline is configured
- [ ] Environment variables documented
- [ ] Deployment instructions provided

### Example Output Structure

After generation, the project should look like:

```
my-awesome-project/
├── PROJECT_BRIEF.md              (original requirements)
├── README.md                     (updated with project info)
├── src/
│   ├── backend/                  (generated)
│   │   ├── src/
│   │   ├── tests/
│   │   ├── package.json
│   │   └── .env.example
│   ├── frontend/                 (generated)
│   │   ├── src/
│   │   ├── tests/
│   │   └── package.json
│   └── shared/                   (generated if needed)
├── project-docs/
│   ├── knowledge_base/           (populated)
│   ├── architecture/             (populated)
│   └── docs/                     (populated)
├── deployment/
│   ├── docker/                   (configured)
│   └── ci-cd/                    (configured)
├── tasks/
│   └── active/                   (initial tasks created)
└── .ai-prompts/
    └── sessions/
        └── 2025-11-04_initial-generation.md (your work log)
```

---

## Common Scenarios

### Scenario 1: Simple REST API
**PROJECT_BRIEF.md says:** "Build a REST API for managing blog posts"

**You generate:**
- `src/backend/` with Express/FastAPI/Gin
- Database models for posts, users
- CRUD endpoints
- Authentication
- Tests
- API documentation

### Scenario 2: Full-Stack Web App
**PROJECT_BRIEF.md says:** "Build a task management web application"

**You generate:**
- `src/backend/` for API
- `src/frontend/` with React/Vue/Angular
- `src/shared/` for TypeScript types
- Database schema
- Authentication flow
- Real-time updates (WebSocket)
- Tests for both frontend and backend

### Scenario 3: Microservices
**PROJECT_BRIEF.md says:** "Build an e-commerce platform with separate services"

**You generate:**
- `src/api-gateway/`
- `src/backend/user-service/`
- `src/backend/product-service/`
- `src/backend/order-service/`
- `src/backend/payment-service/`
- `src/frontend/`
- Service mesh configuration
- Inter-service communication

---

## Tips for Success

### For Humans
- **Be specific** in PROJECT_BRIEF.md - the more detail, the better
- **Include examples** of similar apps if helpful
- **Specify constraints** (budget, timeline, team size)
- **List must-haves vs nice-to-haves**

### For AI Agents
- **Read everything** before starting to code
- **Ask clarifying questions** if requirements are unclear
- **Document decisions** as you make them
- **Test as you go** - don't leave testing for the end
- **Keep session log updated** throughout the process
- **Follow patterns** in `.agents/` folders for each app type

---

## Need Help?

- **Humans**: Check `README.md` for detailed documentation
- **AI Agents**: Review `.agents/project-rules.md` for comprehensive guidelines
- **Both**: Look at `.ai-prompts/templates/` for common prompt patterns

---

**Ready to build something amazing? Start with PROJECT_BRIEF.md! 🚀**

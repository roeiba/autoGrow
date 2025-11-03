---
trigger: manual
project: AI-Optimized Project Template
version: 2.0.1
last_updated: 2025-11-11
---

# Project Guidelines for AI Agents

## Purpose

This document provides comprehensive guidelines for AI coding assistants working on this project. It defines the project structure, development workflows, quality standards, and best practices that ensure consistent, high-quality contributions.

## 🎯 Template vs Generated Project

**IMPORTANT**: This is a **template**, not a complete project.

### If PROJECT_BRIEF.md is filled out:
You are in **generation mode**. Your job is to:
1. Read `PROJECT_BRIEF.md` to understand requirements
2. Generate the complete project structure
3. Create all necessary code, documentation, and configuration
4. Follow the guidelines below while generating
5. Don't generate more than what is required. 
6. Do not create empty files or folders. Create only the files and folders that are required.

### If PROJECT_BRIEF.md is empty:
You are in **development mode** on an already-generated project. Your job is to:
1. Work on specific tasks in `tasks/active/`
2. Follow existing patterns and architecture
3. Maintain and extend the codebase
4. Follow the guidelines below while developing

### Starting Point: PROJECT_BRIEF.md

**For Initial Project Generation:**
- `PROJECT_BRIEF.md` is the **single source of truth** for requirements
- Human fills this out, AI generates everything else
- All code in `src/` should be generated based on this brief
- All documentation should derive from this brief
- This is the ONLY file humans need to edit to start a project

## Project Structure

### Architectural Philosophy

**Separation of Concerns**: Each component has a single, well-defined responsibility  
**Modularity**: Applications are independent and can be deployed separately  
**Context-Aware**: Every major folder includes `.agents/` with specific guidelines  
**Documentation-First**: Knowledge and decisions are captured before implementation

### Directory Overview

#### `src/` - Application Source Code
Contains all application code organized by platform or function:

- **Independent Apps**: `backend/`, `frontend/`, `mobile/`, `web/`, `portal/`, `marketing/`, `sales/`, `admin/`, `api-gateway/`
- **Shared Code**: `shared/` - Common libraries, types, and utilities
- **System Tests**: `blackboxtesting/` - End-to-end integration tests

**Key Principles**:
- Each app has its own `.agents/README.md` with app-specific guidelines
- Each app has its own `tests/` directory for unit and integration tests
- Apps are independently deployable with isolated dependencies
- Technology choices can differ between apps

#### `project-docs/` - Centralized Documentation
All project documentation in one location:

- **`docs/`** - Technical documentation, user guides, API specs, processes
- **`knowledge_base/`** - Business context, domain knowledge, requirements, research
- **`architecture/`** - System design, ADRs, diagrams, patterns, security

**When to Update**:
- `docs/` - When features, APIs, or processes change
- `knowledge_base/` - When requirements or business understanding evolves
- `architecture/` - When making architectural decisions or design changes

#### `tasks/` - Work Management
AI-optimized task tracking system:

- **`active/`** - Current sprint work (status: pending or in_progress)
- **`backlog/`** - Prioritized future work
- **`completed/`** - Archived finished tasks
- **`templates/`** - Reusable task templates

**Task Lifecycle**: `pending` → `in_progress` → `review` → `completed`

#### `deployment/` - DevOps & Infrastructure
Infrastructure as Code and deployment configurations:

- **`docker/`** - Container definitions
- **`kubernetes/`** - K8s manifests and Helm charts
- **`ci-cd/`** - Pipeline definitions for various CI/CD platforms
- **`terraform/`** - Infrastructure provisioning
- **`ansible/`** - Configuration management
- **`monitoring/`** - Observability configurations
- **`scripts/`** - Deployment automation

#### `scripts/` - Automation Scripts
Utility scripts for development and operations:

- **`dev/`** - Development environment setup and helpers
- **`data/`** - Data processing, migration, and seeding
- **`testing/`** - Test utilities and fixtures
- **`ci/`** - CI/CD helper scripts
- **`maintenance/`** - Cleanup, backup, and maintenance tasks

## Development Workflow

### 1. Initialize Context
**Before starting any work**, establish understanding:

```
1. Read this file (.agents/project-rules.md)
2. Review project-docs/knowledge_base/ for business context
3. Study project-docs/architecture/ for technical patterns
4. Check project-docs/docs/ for existing features
```

**Why This Matters**:
- Creates transparency in AI-assisted development
- Enables reproducibility of AI work
- Builds knowledge base of effective prompting patterns
- Helps debug issues by tracing back to original instructions
- Facilitates knowledge transfer to team members

### 2. Select Task
**Choose work strategically**:

```
1. Browse tasks/active/ for available work
2. Select task matching current context and skills
3. Update task status from 'pending' to 'in_progress'
4. Note any dependencies or blockers
5. Read linked documentation in knowledge_base/
```

### 3. Design Solution
**Plan before implementing**:

```
1. Review project-docs/architecture/patterns/ for existing patterns
2. Check if similar features exist in codebase
3. For significant decisions, create ADR in architecture/decisions/
4. Sketch solution approach in task file
5. Identify affected components and tests
```

### 4. Implement
**Write code following established patterns**:

```
1. Navigate to relevant src/<app>/ directory
2. Read src/<app>/.agents/README.md for app-specific rules
3. Follow existing code style and patterns
4. Write self-documenting code with clear naming
5. Add comments for complex logic
6. Keep functions small and focused
7. Handle errors appropriately
8. Avoid hardcoding values (use configuration)
```

### 5. Test
**Ensure quality through comprehensive testing**:

```
1. Write tests in src/<app>/tests/
2. Follow testing pyramid: many unit tests, fewer integration tests
3. Aim for >80% code coverage
4. Test edge cases and error conditions
5. If changes affect multiple apps, add tests to src/blackboxtesting/
6. Run all tests before committing
7. Fix any failing tests
```

### 6. Document
**Maintain living documentation**:

```
1. Update project-docs/docs/technical/ if APIs changed
2. Update project-docs/docs/user-guides/ if user-facing features changed
3. Add/update ADRs if architectural decisions were made
4. Update app-specific .agents/README.md if patterns changed
5. Add inline code documentation for complex logic
```

### 7. Complete
**Finalize work properly**:

```
1. Run full test suite
2. Check code quality (linting, formatting)
3. Finalize session log in .ai-prompts/sessions/ with:
   - All prompts received
   - Files created/modified
   - Outcomes (completed, partial, not completed)
   - Challenges encountered and lessons learned
4. Update task file with completion notes
5. Move task from tasks/active/ to tasks/completed/
6. Create clear commit message (conventional commits format)
7. Commit session log along with code changes
```

## Code Quality Standards

### General Principles

**SOLID Principles**
- Single Responsibility: Each class/function has one reason to change
- Open/Closed: Open for extension, closed for modification
- Liskov Substitution: Subtypes must be substitutable for base types
- Interface Segregation: Many specific interfaces better than one general
- Dependency Inversion: Depend on abstractions, not concretions

**Clean Code**
- Meaningful names: Variables, functions, classes should reveal intent
- Small functions: Functions should do one thing well
- DRY: Don't repeat yourself - extract common logic
- Comments: Explain why, not what (code should be self-documenting)
- Error handling: Don't ignore errors, handle them appropriately

### Language-Specific Standards

**JavaScript/TypeScript**
- Use ESLint and Prettier
- Prefer `const` over `let`, avoid `var`
- Use async/await over callbacks
- Type everything in TypeScript (avoid `any`)
- Use functional programming patterns where appropriate

**Python**
- Follow PEP 8 style guide
- Use type hints (PEP 484)
- Use Black for formatting
- Prefer list comprehensions for simple transformations
- Use context managers for resource management

**Go**
- Follow official Go style guide
- Use `gofmt` for formatting
- Handle all errors explicitly
- Use interfaces for abstraction
- Keep packages focused and small

### Testing Standards

**Unit Tests**
- Test one thing per test
- Use descriptive test names (should/when/then pattern)
- Arrange-Act-Assert structure
- Mock external dependencies
- Fast execution (<100ms per test)

**Integration Tests**
- Test component interactions
- Use test databases/services
- Clean up after tests
- Acceptable slower execution
- Test realistic scenarios

**System Tests** (in `src/blackboxtesting/`)
- Test end-to-end user journeys
- Test across multiple applications
- Use production-like environment
- Include performance and load tests
- Validate security requirements

### Documentation Standards

**Code Documentation**
- Public APIs: Comprehensive documentation with examples
- Complex algorithms: Explain approach and reasoning
- Configuration: Document all options and defaults
- Error messages: Clear, actionable, user-friendly

**Project Documentation**
- Technical docs: API specs, integration guides, troubleshooting
- User docs: Getting started, tutorials, reference
- Architecture: System context, component diagrams, ADRs
- Knowledge base: Business context, domain concepts, requirements

## Common Patterns

### Error Handling
```
✅ DO: Handle errors explicitly
✅ DO: Provide context in error messages
✅ DO: Log errors appropriately
✅ DO: Return meaningful error responses

❌ DON'T: Ignore errors silently
❌ DON'T: Use generic error messages
❌ DON'T: Expose internal details to users
```

### Configuration
```
✅ DO: Use environment variables for configuration
✅ DO: Provide sensible defaults
✅ DO: Validate configuration on startup
✅ DO: Document all configuration options

❌ DON'T: Hardcode values in source code
❌ DON'T: Commit secrets to version control
❌ DON'T: Use different config mechanisms per app
```

### API Design
```
✅ DO: Use RESTful conventions
✅ DO: Version your APIs
✅ DO: Validate input thoroughly
✅ DO: Return appropriate HTTP status codes
✅ DO: Document all endpoints

❌ DON'T: Care acout backward compatibility - its always newly launched project.
❌ DON'T: Return sensitive data unnecessarily
❌ DON'T: Use verbs in endpoint URLs
```

### Database Access
```
✅ DO: Use connection pooling
✅ DO: Use prepared statements/parameterized queries
✅ DO: Handle connection failures gracefully
✅ DO: Use transactions for multi-step operations
✅ DO: Index frequently queried columns

❌ DON'T: Build SQL with string concatenation
❌ DON'T: Leave connections open
❌ DON'T: Ignore database errors
```

## Anti-Patterns to Avoid

### Code Anti-Patterns
- **God Objects**: Classes that know/do too much
- **Spaghetti Code**: Tangled, hard-to-follow logic
- **Copy-Paste Programming**: Duplicating code instead of abstracting
- **Magic Numbers**: Unexplained numeric constants
- **Premature Optimization**: Optimizing before measuring

### Architecture Anti-Patterns
- **Big Ball of Mud**: No clear structure or organization
- **Vendor Lock-in**: Tight coupling to specific vendors
- **Golden Hammer**: Using same solution for every problem
- **Analysis Paralysis**: Over-planning without implementation

### Process Anti-Patterns
- **Cowboy Coding**: No planning, testing, or review
- **Death March**: Unrealistic deadlines and expectations
- **Scope Creep**: Continuously adding features without prioritization
- **Technical Debt Accumulation**: Never refactoring or improving code

## Commit Standards

### Conventional Commits Format
```
type(scope): brief description

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring (no feature change or bug fix)
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependency updates

**Examples**:
```
feat(auth): implement JWT authentication
fix(api): handle null user in profile endpoint
docs(readme): update installation instructions
test(cart): add unit tests for discount calculation
refactor(database): extract connection pool logic
```

## Continuous Improvement

### Proposing Changes
When you identify better patterns or improvements:

1. **Document**: Create ADR in `project-docs/architecture/decisions/`
2. **Discuss**: Propose in task or discussion forum
3. **Implement**: Update code following new pattern
4. **Update**: Modify this guide and relevant `.agents/` files
5. **Migrate**: Create migration plan for existing code
6. **Communicate**: Inform team of changes

### Learning from Mistakes
When issues occur:

1. **Root Cause Analysis**: Understand why it happened
2. **Document**: Add to knowledge base or ADR
3. **Prevent**: Update guidelines or add automation
4. **Share**: Communicate learnings to team

## Emergency Procedures

### Production Issues
1. **Assess**: Determine severity and impact
2. **Communicate**: Notify stakeholders
3. **Mitigate**: Apply immediate fix or rollback
4. **Investigate**: Find root cause
5. **Resolve**: Implement proper fix
6. **Document**: Create postmortem
7. **Prevent**: Add monitoring, tests, or safeguards

### Security Incidents
1. **Contain**: Limit damage immediately
2. **Assess**: Determine scope and impact
3. **Notify**: Follow incident response plan
4. **Remediate**: Fix vulnerability
5. **Audit**: Review for similar issues
6. **Document**: Create incident report

## Questions and Clarifications

If you encounter ambiguity or need clarification:

1. **Check Documentation**: Review `project-docs/` thoroughly
2. **Review History**: Check git history and previous decisions
3. **Ask**: Create discussion or task for clarification
4. **Document Answer**: Update relevant documentation

## Version History

- **2.0.1** (2025-11-11): Fixed documentation references, enhanced .gitignore, improved PROJECT_BRIEF.md
- **2.0.0** (2025-11-03): Complete rewrite with comprehensive guidelines
- **1.0.0** (2025-11-01): Initial version

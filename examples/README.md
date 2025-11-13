# AI Template Examples

> **Real-world demonstrations of AI-driven project generation using the AI-Optimized Project Template**

This directory contains complete examples showing how AI agents transform a simple requirements document (`PROJECT_BRIEF.md`) into production-ready applications.

---

## 📁 Available Examples

### [Task Management API](./task-management-api/)

**Description**: A complete RESTful API for task and project management with team collaboration features.

**Technology Stack**:
- Backend: Node.js + Express
- Database: PostgreSQL + Redis
- Real-time: Socket.io
- Testing: Jest + Supertest
- DevOps: Docker + GitHub Actions

**Features Demonstrated**:
- ✅ User authentication (JWT)
- ✅ CRUD operations for projects and tasks
- ✅ Role-based access control
- ✅ Real-time WebSocket updates
- ✅ Comprehensive test suite (80%+ coverage)
- ✅ Docker deployment setup
- ✅ API documentation
- ✅ CI/CD pipeline

**What's Included**:
- [`PROJECT_BRIEF.md`](./task-management-api/PROJECT_BRIEF.md) - The requirements document
- [`STEP_BY_STEP_GUIDE.md`](./task-management-api/STEP_BY_STEP_GUIDE.md) - Complete walkthrough
- [`generated/`](./task-management-api/generated/) - AI-generated application code

**Time to Generate**: 30-60 minutes with AI vs. 2-3 weeks manual development

**Learning Focus**: Full-stack backend development, API design, testing, deployment

---

## 🎯 How to Use These Examples

### 1. Study the PROJECT_BRIEF.md

Each example includes a comprehensive `PROJECT_BRIEF.md` that demonstrates:
- How to structure requirements
- What level of detail to provide
- How to specify technical preferences
- Best practices for AI comprehension

### 2. Review the Step-by-Step Guide

The `STEP_BY_STEP_GUIDE.md` in each example explains:
- The complete workflow from requirements to deployment
- How AI interprets and generates code
- Architecture decisions and patterns
- Testing and validation approaches
- Customization and extension strategies

### 3. Explore the Generated Code

The `generated/` directory contains the complete AI-generated application:
- Review code structure and organization
- Understand design patterns used
- Study test implementations
- Examine DevOps configurations

### 4. Try It Yourself

Follow these steps to recreate the example:

```bash
# 1. Clone the template
git clone https://github.com/roeiba/ai-project-template.git my-project
cd my-project

# 2. Copy the example PROJECT_BRIEF.md
cp examples/task-management-api/PROJECT_BRIEF.md PROJECT_BRIEF.md

# 3. Provide to your AI assistant
# "I've filled out PROJECT_BRIEF.md. Please generate the complete project
#  following the guidelines in .agents/project-rules.md"

# 4. Review and run the generated code
cd src/backend
npm install
npm test
docker-compose up
```

---

## 📊 Example Comparison

| Aspect | Manual Development | AI-Assisted (Template) |
|--------|-------------------|------------------------|
| **Time** | 2-3 weeks | 1-2 days |
| **Initial Setup** | 4-6 hours | 1-2 hours |
| **Code Generation** | 5-7 days | 30-60 minutes |
| **Testing** | 2-3 days | Included (10-15 min) |
| **DevOps Setup** | 1-2 days | Included (5-10 min) |
| **Documentation** | 1-2 days | Included (5-10 min) |
| **Code Quality** | Varies by developer | Consistently high |
| **Best Practices** | Requires expertise | Built-in |
| **Consistency** | Varies | Standardized |

---

## 🎓 What You'll Learn

### From Task Management API Example:

1. **Effective Requirements Writing**
   - How to structure PROJECT_BRIEF.md
   - What details AI needs to generate quality code
   - How to specify constraints and priorities

2. **AI-Driven Development Workflow**
   - Preparing requirements for AI
   - Prompting AI effectively
   - Reviewing and validating generated code
   - Iterating and refining

3. **Backend API Architecture**
   - Clean architecture principles
   - RESTful API design
   - Database modeling and relationships
   - Authentication and authorization
   - Real-time features with WebSocket

4. **Production-Ready Practices**
   - Comprehensive testing strategies
   - Error handling patterns
   - Security best practices (OWASP)
   - Logging and monitoring
   - Docker containerization
   - CI/CD pipeline setup

5. **Code Quality Standards**
   - SOLID principles in practice
   - Consistent code structure
   - Documentation standards
   - Test coverage goals

---

## 🚀 Quick Start Guide

### Option 1: Study Existing Example

```bash
# Clone the repository
git clone https://github.com/roeiba/ai-project-template.git
cd ai-project-template/examples/task-management-api

# Read the requirements
cat PROJECT_BRIEF.md

# Follow the guide
open STEP_BY_STEP_GUIDE.md

# Run the generated code
cd generated
docker-compose up
```

### Option 2: Generate Your Own

```bash
# Clone the template
git clone https://github.com/roeiba/ai-project-template.git my-project
cd my-project

# Fill out PROJECT_BRIEF.md with your requirements
vim PROJECT_BRIEF.md

# Provide to AI with this prompt:
cat << 'EOF'
I've filled out PROJECT_BRIEF.md. Please generate the complete project
following the guidelines in .agents/project-rules.md:

1. Read PROJECT_BRIEF.md carefully
2. Generate complete application code in src/
3. Include comprehensive tests (80%+ coverage)
4. Create Docker deployment configurations
5. Generate API documentation
6. Set up CI/CD pipelines
7. Follow best practices for security, performance, and maintainability

Create a production-ready application.
EOF
```

### Option 3: Adapt an Example

```bash
# Start with an example
cp -r examples/task-management-api my-custom-project
cd my-custom-project

# Modify PROJECT_BRIEF.md for your needs
vim PROJECT_BRIEF.md

# Ask AI to regenerate with your changes
# "Please update the generated code to match the modified PROJECT_BRIEF.md"
```

---

## 📚 Additional Resources

### Documentation

- [Main README](../README.md) - Template overview
- [QUICKSTART.md](../QUICKSTART.md) - Quick start guide
- [PROJECT_BRIEF.md Template](../PROJECT_BRIEF.md) - Blank template
- [AI Guidelines](./.agents/project-rules.md) - Rules for AI agents

### Best Practices

- **Writing Requirements**: See the example PROJECT_BRIEF.md files
- **AI Prompting**: Check STEP_BY_STEP_GUIDE.md for effective prompts
- **Code Review**: Generated code includes inline comments explaining patterns
- **Testing**: Example test files demonstrate comprehensive testing approaches

### Common Use Cases

1. **Learning AI-Assisted Development**
   - Start with an example
   - Study how AI interprets requirements
   - Understand generated patterns

2. **Bootstrapping New Projects**
   - Use example as template
   - Modify PROJECT_BRIEF.md
   - Generate custom application

3. **Teaching/Training**
   - Show students complete workflow
   - Demonstrate best practices
   - Compare manual vs. AI-assisted development

4. **Proof of Concepts**
   - Rapid prototyping
   - Validate ideas quickly
   - Get to production faster

---

## 🤔 FAQ

### Q: Can I use these examples in production?

**A**: The examples are designed to be production-ready starting points. However, you should:
- Review all generated code
- Add your specific business logic
- Configure security settings (secrets, API keys)
- Set up proper monitoring and logging
- Conduct security audits

### Q: How do I modify an example for my needs?

**A**:
1. Copy the example directory
2. Edit PROJECT_BRIEF.md with your requirements
3. Ask AI to regenerate or update specific parts
4. Review and test changes
5. Iterate as needed

### Q: What if the generated code doesn't work?

**A**:
1. Check that all dependencies are installed
2. Verify environment variables are set correctly
3. Ensure database and services are running
4. Review error messages and logs
5. Ask AI to fix specific issues

### Q: Can I generate examples in other languages?

**A**: Yes! The template is language-agnostic. Specify your preferred stack in PROJECT_BRIEF.md:
- Python (Django/FastAPI/Flask)
- Go (Gin/Echo/Fiber)
- Java (Spring Boot)
- Ruby (Rails)
- .NET (ASP.NET Core)

### Q: How much should I trust the generated code?

**A**: AI-generated code following this template is generally high quality, but:
- Always review security-critical sections
- Validate business logic matches requirements
- Run all tests
- Perform security scans
- Test edge cases

### Q: Can I contribute more examples?

**A**: Absolutely! We welcome contributions:
1. Create a new example directory
2. Include complete PROJECT_BRIEF.md
3. Add STEP_BY_STEP_GUIDE.md
4. Include generated code
5. Test thoroughly
6. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

## 🎯 Example Roadmap

### Coming Soon

- **Frontend React App** - Single-page application with API integration
- **Python FastAPI Service** - Async API with Python
- **Go Microservice** - High-performance microservice
- **Mobile React Native App** - Cross-platform mobile app
- **Full-Stack Next.js** - Complete web application
- **CLI Tool** - Command-line application in Go
- **Serverless Functions** - AWS Lambda/Cloud Functions
- **Data Pipeline** - ETL pipeline with Airflow

### Want a Specific Example?

Open an issue on GitHub with:
- Project type
- Technology stack
- Key features
- Use case description

---

## 📖 Example Structure

Each example follows this structure:

```
example-name/
├── README.md                    # Example overview
├── PROJECT_BRIEF.md             # Requirements document
├── STEP_BY_STEP_GUIDE.md        # Detailed walkthrough
└── generated/                   # AI-generated code
    ├── src/                     # Application source
    ├── tests/                   # Test suite
    ├── deployment/              # Docker, K8s configs
    ├── project-docs/            # Documentation
    ├── package.json             # Dependencies
    └── README.md                # Setup instructions
```

---

## 💡 Tips for Success

### 1. Start with Requirements

✅ **Do**: Spend time on comprehensive PROJECT_BRIEF.md
❌ **Don't**: Rush requirements and expect AI to fill gaps

### 2. Be Specific

✅ **Do**: "JWT authentication with email verification, password reset, 2FA"
❌ **Don't**: "Authentication"

### 3. Include Context

✅ **Do**: Explain WHY features are needed
❌ **Don't**: Just list WHAT to build

### 4. Review Generated Code

✅ **Do**: Understand the architecture and patterns
❌ **Don't**: Blindly use without review

### 5. Iterate

✅ **Do**: Start simple, add features incrementally
❌ **Don't**: Try to generate everything at once

### 6. Maintain Documentation

✅ **Do**: Update PROJECT_BRIEF.md as project evolves
❌ **Don't**: Let documentation become stale

---

## 🙏 Acknowledgments

These examples demonstrate patterns and practices from:
- Clean Architecture (Robert C. Martin)
- Domain-Driven Design (Eric Evans)
- The Twelve-Factor App
- OWASP Security Guidelines
- RESTful API Best Practices

---

## 📝 License

All examples are provided under the MIT License. Feel free to use, modify, and distribute.

---

<div align="center">

**Ready to build your own AI-generated application?**

[Get Started](../README.md) • [View Template](../) • [Report Issue](https://github.com/roeiba/ai-project-template/issues)

*Building the future, one PROJECT_BRIEF.md at a time*

</div>

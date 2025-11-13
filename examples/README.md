# Examples - AI Project Template

> **Real-world examples demonstrating how AI agents generate complete projects from requirements documents.**

This directory contains comprehensive examples showing the **end-to-end workflow** of using the AI-Optimized Project Template to build production-ready applications.

## 📁 Available Examples

### 1. Task Management Application (TaskFlow)

**Location**: [`task-management-app/`](./task-management-app/)

**What it demonstrates**:
- Complete PROJECT_BRIEF.md for a real-world SaaS application
- Generated backend API (Node.js + TypeScript + Express)
- Generated frontend (Next.js + React + Tailwind CSS)
- Real-time features with WebSocket
- Database design with PostgreSQL
- Docker and Kubernetes configurations
- Comprehensive tests and documentation
- CI/CD pipeline setup

**Technology Stack**:
- Backend: Node.js, TypeScript, Express, PostgreSQL, Redis, Socket.io
- Frontend: Next.js 14, React 18, Tailwind CSS, Zustand
- Infrastructure: Docker, Kubernetes, GitHub Actions
- Testing: Jest, Supertest, Playwright

**Key Features**:
- Task management with Kanban boards
- Real-time collaboration
- Team and project organization
- GitHub integration
- REST API with WebSocket support

**Time to Generate**: ~15-20 minutes with AI

👉 **[View Complete Example](./task-management-app/README.md)**

---

## 🎯 What These Examples Show

### For Developers
- How to write an effective PROJECT_BRIEF.md
- What AI can generate from requirements
- Code quality and architecture patterns
- Testing strategies
- Documentation approaches
- Deployment configurations

### For Product Managers
- Requirements gathering format
- Feature specification examples
- User story documentation
- Success metrics definition

### For Team Leads
- Project setup time savings
- Quality standards enforcement
- Onboarding acceleration
- Documentation consistency

---

## 🚀 How to Use These Examples

### 1. Study the Example

```bash
# Navigate to an example
cd examples/task-management-app/

# Read the requirements
cat PROJECT_BRIEF.md

# Review the generated output
ls -R generated-output/

# Read the step-by-step guide
cat README.md
```

### 2. Try It Yourself

**Option A: Modify the Example**
1. Copy the example PROJECT_BRIEF.md
2. Modify it for your needs
3. Provide to AI with generation prompt
4. Compare AI output with example

**Option B: Start Fresh**
1. Start with blank PROJECT_BRIEF.md from template root
2. Fill in your project requirements
3. Use example as reference
4. Generate your custom project

### 3. Compare Results

**What to compare**:
- Code structure and organization
- Naming conventions
- Error handling patterns
- Test coverage
- Documentation completeness
- Security implementations

---

## 📊 Example Statistics

### TaskFlow Example

| Metric | Value |
|--------|-------|
| PROJECT_BRIEF.md | 1 file (30 min to fill) |
| Generated Files | 150+ files |
| Lines of Code | 15,000+ LOC |
| Test Files | 40+ test files |
| Documentation | 20+ doc files |
| Configuration Files | 15+ config files |
| Generation Time | 15-20 minutes |
| Manual Development Time | 4-6 weeks |
| **Time Saved** | **95%** |

---

## 🎓 Learning Path

### Beginner
1. Read TaskFlow README from start to finish
2. Examine PROJECT_BRIEF.md structure
3. Browse generated code (don't need to understand every line)
4. Try generating a simple project

### Intermediate
1. Deep-dive into generated backend code
2. Understand frontend component structure
3. Review test patterns
4. Customize example for your use case

### Advanced
1. Study architecture decisions
2. Analyze security implementations
3. Optimize generated code
4. Create your own complex project

---

## 🔍 Key Files to Examine

For each example, focus on these key files:

### Requirements
- `PROJECT_BRIEF.md` - The input requirements document

### Generated Code
- `generated-output/src/backend/server.ts` - Backend entry point
- `generated-output/src/backend/models/` - Database models
- `generated-output/src/frontend/app/page.tsx` - Frontend entry
- `generated-output/tests/` - Test examples

### Infrastructure
- `generated-output/deployment/docker/docker-compose.yml` - Local dev setup
- `generated-output/deployment/kubernetes/` - Production deployment

### Documentation
- `generated-output/project-docs/architecture/system-design.md` - Architecture
- `generated-output/project-docs/docs/api/` - API documentation

---

## 💡 Tips for Success

### Writing PROJECT_BRIEF.md
✅ **Do**:
- Be specific about requirements
- Include user flows and use cases
- Specify technology preferences
- Define success metrics
- Describe target users clearly

❌ **Don't**:
- Leave sections empty
- Use vague descriptions
- Skip technical preferences
- Forget non-functional requirements

### Working with Generated Code
✅ **Do**:
- Review all generated code
- Test thoroughly
- Customize for your brand
- Add business-specific logic
- Keep documentation updated

❌ **Don't**:
- Blindly trust everything
- Skip security review
- Ignore test failures
- Deploy without review
- Forget to customize

### Iterating and Improving
✅ **Do**:
- Provide feedback to AI
- Regenerate if needed
- Refactor as you learn
- Share improvements
- Document decisions

❌ **Don't**:
- Accept poor quality
- Leave technical debt
- Skip refactoring
- Work in isolation

---

## 🤝 Contributing Examples

Want to add your own example? We'd love to see it!

### Example Criteria
- Must include complete PROJECT_BRIEF.md
- Should show generated code structure
- Must include step-by-step README
- Should demonstrate unique use case
- Must follow template guidelines

### Submission Process
1. Create example in new directory
2. Follow structure of existing examples
3. Test generation workflow
4. Document thoroughly
5. Submit pull request

**Ideas for New Examples**:
- E-commerce platform
- Blog/CMS system
- Analytics dashboard
- Mobile app backend
- Microservices architecture
- Machine learning API
- IoT data platform
- Social media app

---

## 📚 Additional Resources

### Template Documentation
- [Main README](../README.md) - Template overview
- [QUICKSTART](../QUICKSTART.md) - Getting started guide
- [Project Rules](../.agents/project-rules.md) - AI guidelines

### External Resources
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Twelve-Factor App](https://12factor.net/)
- [API Design Best Practices](https://swagger.io/resources/articles/best-practices-in-api-design/)

---

## ❓ FAQ

**Q: Can I use these examples in production?**
A: These are demonstrations. Review, test, and customize before production use.

**Q: How accurate are the generation times?**
A: Times vary by AI model and complexity. Claude Sonnet typically: 15-20 min.

**Q: What if AI generates different code than the example?**
A: That's normal! AI can generate variations. Focus on quality, not exact match.

**Q: Should I modify PROJECT_BRIEF.md after generation?**
A: Keep it as documentation of original requirements. Create new docs for changes.

**Q: Can I share my generated projects?**
A: Yes! Both template and generated code are MIT licensed.

---

## 🎉 Ready to Try?

1. **Choose an example** to study
2. **Read the complete README** for that example
3. **Examine the generated code**
4. **Try generating your own project**

Start with TaskFlow - it's the most comprehensive example!

👉 **[Get Started with TaskFlow](./task-management-app/README.md)**

---

<div align="center">

**Learn from examples** • **Generate your own** • **Ship faster**

[⭐ Star the Template](https://github.com/roeiba/ai-project-template) · [Report Issue](https://github.com/roeiba/ai-project-template/issues) · [Discussions](https://github.com/roeiba/ai-project-template/discussions)

</div>

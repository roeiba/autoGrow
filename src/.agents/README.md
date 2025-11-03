# Source Code Generation Guidelines

> **For AI Agents**: This folder is empty in the template. You will generate all application code here based on `PROJECT_BRIEF.md`.

## 🎯 Your Mission

Read `PROJECT_BRIEF.md` and generate **only the applications needed** for the project. Don't create all 11 app types - only what's required.

## 📋 Available Application Types

### Core Applications (Most Common)

**`backend/`** - Core API Server
- **When to create**: Almost always (unless pure static site)
- **Purpose**: REST/GraphQL API, business logic, data persistence
- **Tech options**: Node.js (Express/NestJS), Python (FastAPI/Django), Go (Gin/Echo), Java (Spring Boot)
- **Structure**:
  ```
  backend/
  ├── src/
  │   ├── api/          # Routes, controllers, middleware
  │   ├── core/         # Business logic, domain models
  │   ├── services/     # Application services
  │   ├── data/         # Database access, repositories
  │   ├── config/       # Configuration management
  │   └── utils/        # Helper functions
  ├── tests/
  │   ├── unit/
  │   ├── integration/
  │   └── fixtures/
  ├── package.json / requirements.txt / go.mod
  ├── .env.example
  └── README.md
  ```

**`frontend/`** - Web Application UI
- **When to create**: Web-based user interface needed
- **Purpose**: Interactive web application for end users
- **Tech options**: React, Vue.js, Angular, Svelte, Next.js
- **Structure**:
  ```
  frontend/
  ├── src/
  │   ├── components/   # Reusable UI components
  │   ├── pages/        # Page components
  │   ├── services/     # API clients, business logic
  │   ├── store/        # State management
  │   ├── hooks/        # Custom hooks
  │   ├── utils/        # Helper functions
  │   └── assets/       # Images, styles
  ├── tests/
  ├── public/
  ├── package.json
  ├── .env.example
  └── README.md
  ```

**`mobile/`** - Mobile Applications
- **When to create**: iOS/Android apps needed
- **Purpose**: Native or cross-platform mobile apps
- **Tech options**: React Native, Flutter, Native iOS (Swift), Native Android (Kotlin)
- **Structure**:
  ```
  mobile/
  ├── src/
  │   ├── screens/      # Screen components
  │   ├── components/   # Reusable components
  │   ├── navigation/   # Navigation setup
  │   ├── services/     # API clients
  │   ├── store/        # State management
  │   └── utils/
  ├── tests/
  ├── android/          # Android-specific (if React Native)
  ├── ios/              # iOS-specific (if React Native)
  ├── package.json
  └── README.md
  ```

### Specialized Applications (Create Only If Needed)

**`web/`** - Public Marketing Website
- **When to create**: Need SEO-optimized public site separate from app
- **Purpose**: Landing pages, marketing content, blog
- **Tech options**: Next.js (SSG), Astro, Hugo, Jekyll
- **Note**: Often combined with `frontend/` for simpler projects

**`portal/`** - Authenticated User Portal
- **When to create**: Need separate portal with different UX from main app
- **Purpose**: Customer portal, partner portal, user dashboard
- **Tech options**: Same as frontend
- **Note**: Often combined with `frontend/` for simpler projects

**`admin/`** - Admin Dashboard
- **When to create**: Need separate admin interface with high security
- **Purpose**: System administration, user management, analytics
- **Tech options**: React Admin, Vue Admin, custom build
- **Note**: Can be part of `frontend/` with role-based routing

**`api-gateway/`** - API Gateway
- **When to create**: Microservices architecture with multiple backend services
- **Purpose**: Request routing, authentication, rate limiting, API composition
- **Tech options**: Kong, Express Gateway, custom Node.js/Go
- **Note**: Only for microservices; skip for monolithic backend

**`marketing/`** - Marketing Automation
- **When to create**: Complex marketing campaigns and automation needed
- **Purpose**: Email campaigns, A/B testing, analytics
- **Tech options**: Custom integrations with marketing tools
- **Note**: Rare; usually handled by external tools

**`sales/`** - Sales CRM
- **When to create**: Custom CRM functionality needed
- **Purpose**: Lead management, pipeline tracking
- **Tech options**: Custom build or integrations
- **Note**: Very rare; usually use existing CRM tools

### Support Applications (Create As Needed)

**`shared/`** - Shared Code
- **When to create**: Code reused across multiple apps (especially TypeScript types)
- **Purpose**: Common types, utilities, constants, validation schemas
- **Structure**:
  ```
  shared/
  ├── src/
  │   ├── types/        # TypeScript types, interfaces
  │   ├── utils/        # Shared utilities
  │   ├── constants/    # Shared constants
  │   └── validators/   # Validation schemas
  ├── package.json
  └── README.md
  ```

**`blackboxtesting/`** - System-Wide Tests
- **When to create**: Always (for integration testing across apps)
- **Purpose**: End-to-end tests, system integration tests
- **Tech options**: Playwright, Cypress, Selenium
- **Structure**:
  ```
  blackboxtesting/
  ├── tests/
  │   ├── e2e/          # End-to-end user flows
  │   ├── integration/  # Cross-app integration tests
  │   └── performance/  # Load and performance tests
  ├── fixtures/         # Test data
  ├── package.json
  └── README.md
  ```

## 🏗️ Generation Decision Tree

```
Read PROJECT_BRIEF.md
    ↓
Does it need an API?
    ├─ YES → Create backend/
    └─ NO  → Skip (unless pure static site)
    ↓
Does it need a web UI?
    ├─ YES → Create frontend/
    └─ NO  → Skip
    ↓
Does it need mobile apps?
    ├─ YES → Create mobile/
    └─ NO  → Skip
    ↓
Is it microservices architecture?
    ├─ YES → Create api-gateway/ + split backend/ into services
    └─ NO  → Keep monolithic backend/
    ↓
Multiple TypeScript apps?
    ├─ YES → Create shared/ for common types
    └─ NO  → Skip
    ↓
Always create:
    └─ blackboxtesting/ (for system tests)
```

## 📝 Generation Checklist

For each app you create:

### 1. Project Setup
- [ ] Create folder structure
- [ ] Initialize package manager (npm, pip, go mod)
- [ ] Set up dependencies
- [ ] Create .env.example with all required variables
- [ ] Add .gitignore

### 2. Core Implementation
- [ ] Implement main functionality based on PROJECT_BRIEF.md
- [ ] Follow language-specific best practices
- [ ] Add proper error handling
- [ ] Implement logging
- [ ] Add input validation

### 3. Testing
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests
- [ ] Test configuration
- [ ] Add to blackboxtesting/ if affects multiple apps

### 4. Documentation
- [ ] Create app-specific README.md
- [ ] Document API endpoints (if backend)
- [ ] Document environment variables
- [ ] Add setup instructions

### 5. Configuration
- [ ] Development configuration
- [ ] Production configuration
- [ ] Docker configuration
- [ ] CI/CD integration

## 🎨 Example Scenarios

### Scenario 1: Simple REST API
**PROJECT_BRIEF.md says**: "Build a REST API for blog posts"

**Generate**:
```
src/
├── backend/          # Express/FastAPI API
└── blackboxtesting/  # API integration tests
```

### Scenario 2: Full-Stack Web App
**PROJECT_BRIEF.md says**: "Build a task management web app"

**Generate**:
```
src/
├── backend/          # API server
├── frontend/         # React/Vue UI
├── shared/           # TypeScript types
└── blackboxtesting/  # E2E tests
```

### Scenario 3: Mobile + Web Platform
**PROJECT_BRIEF.md says**: "Build a social platform with web and mobile"

**Generate**:
```
src/
├── backend/          # API server
├── frontend/         # Web app
├── mobile/           # React Native app
├── shared/           # API contracts, types
└── blackboxtesting/  # Cross-platform tests
```

### Scenario 4: Microservices E-commerce
**PROJECT_BRIEF.md says**: "Build e-commerce with separate services"

**Generate**:
```
src/
├── api-gateway/              # Gateway
├── backend/
│   ├── user-service/         # User management
│   ├── product-service/      # Product catalog
│   ├── order-service/        # Order processing
│   └── payment-service/      # Payment handling
├── frontend/                 # Customer UI
├── admin/                    # Admin dashboard
├── shared/                   # Common types
└── blackboxtesting/          # System tests
```

## ⚙️ Technology Selection

Choose tech stack based on PROJECT_BRIEF.md preferences:

### Backend
- **Node.js**: Express (simple), NestJS (enterprise), Fastify (performance)
- **Python**: FastAPI (modern), Django (full-featured), Flask (lightweight)
- **Go**: Gin (fast), Echo (elegant), Fiber (Express-like)
- **Java**: Spring Boot (enterprise)

### Frontend
- **React**: Most popular, huge ecosystem
- **Vue.js**: Gentle learning curve, great DX
- **Angular**: Enterprise, opinionated
- **Svelte**: Minimal, fast
- **Next.js**: React with SSR/SSG

### Mobile
- **React Native**: JavaScript, cross-platform
- **Flutter**: Dart, beautiful UI
- **Native**: Swift (iOS), Kotlin (Android)

### Database (configure in backend/)
- **PostgreSQL**: Relational, robust
- **MySQL**: Relational, popular
- **MongoDB**: Document, flexible
- **Redis**: Cache, sessions

## 🔒 Security Requirements

For every app:
- [ ] No hardcoded secrets
- [ ] Environment variables for config
- [ ] Input validation on all endpoints
- [ ] Authentication where needed
- [ ] Authorization/RBAC
- [ ] Rate limiting
- [ ] Security headers
- [ ] HTTPS in production

## 📊 Quality Standards

For every app:
- [ ] >80% test coverage
- [ ] All tests passing
- [ ] Linting configured and passing
- [ ] Code formatted consistently
- [ ] No console.log in production
- [ ] Error handling comprehensive
- [ ] Logging structured
- [ ] Performance acceptable

## 🚀 Next Steps After Generation

1. Update main README.md with project-specific info
2. Document architecture in project-docs/architecture/
3. Create initial tasks in tasks/active/
4. Set up CI/CD in deployment/ci-cd/
5. Create Docker configurations
6. Complete session log

---

**Remember**: Only create what's needed. A simple project might just need `backend/` and `frontend/`. Don't over-engineer!

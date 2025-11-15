# Agent Architecture Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     GitHub Actions Workflows                     │
│  (.github/workflows/issue-generator-agent.yml,                  │
│   issue-resolver-agent.yml, qa-agent.yml)                       │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ triggers
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CI/CD Wrapper Scripts                          │
│                   (.github/scripts/)                             │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │ issue_generator  │  │ issue_resolver   │  │  qa_agent    │  │
│  │     .py          │  │     .py          │  │    .py       │  │
│  │  (52 lines)      │  │  (61 lines)      │  │ (59 lines)   │  │
│  └────────┬─────────┘  └────────┬─────────┘  └──────┬───────┘  │
│           │                     │                    │          │
│           │ Environment Setup   │                    │          │
│           │ GitHub/Git Init     │                    │          │
│           │ Error Handling      │                    │          │
└───────────┼─────────────────────┼────────────────────┼──────────┘
            │                     │                    │
            │ imports             │                    │
            ▼                     ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Core Agent Modules                            │
│                    (src/agents/)                                 │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │ IssueGenerator   │  │ IssueResolver    │  │  QAAgent     │  │
│  │   class          │  │   class          │  │   class      │  │
│  │ (245 lines)      │  │ (399 lines)      │  │ (421 lines)  │  │
│  │                  │  │                  │  │              │  │
│  │ Methods:         │  │ Methods:         │  │ Methods:     │  │
│  │ - __init__()     │  │ - __init__()     │  │ - __init__() │  │
│  │ - check_and_     │  │ - resolve_issue()│  │ - run_qa_    │  │
│  │   generate()     │  │ - _select_issue()│  │   check()    │  │
│  │ - _generate_     │  │ - _claim_issue() │  │ - _gather_   │  │
│  │   issues()       │  │ - _create_branch()│  │   context()  │  │
│  │ - _build_prompt()│  │ - _generate_fix()│  │ - _run_qa_   │  │
│  │ - _call_claude() │  │ - _create_pr()   │  │   analysis() │  │
│  └────────┬─────────┘  └────────┬─────────┘  └──────┬───────┘  │
│           │                     │                    │          │
└───────────┼─────────────────────┼────────────────────┼──────────┘
            │                     │                    │
            │ uses                │                    │
            ▼                     ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    External Dependencies                         │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐    │
│  │   PyGithub   │  │  GitPython   │  │ Anthropic/Claude   │    │
│  │   (GitHub    │  │  (Git ops)   │  │  (AI generation)   │    │
│  │    API)      │  │              │  │                    │    │
│  └──────────────┘  └──────────────┘  └────────────────────┘    │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  src/utils/project_brief_validator.py                    │   │
│  │  (Validation utilities)                                  │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Issue Generator Flow

```
GitHub Workflow
      │
      ▼
.github/scripts/issue_generator.py
      │
      ├─ Read env vars (MIN_ISSUES, GITHUB_TOKEN, etc.)
      ├─ Initialize GitHub client
      │
      ▼
src/agents/issue_generator.py
      │
      ├─ IssueGenerator.__init__(repo, min_issues)
      │
      ▼
IssueGenerator.check_and_generate()
      │
      ├─ Count open issues
      ├─ If < min_issues:
      │   ├─ Gather repo context (README, commits)
      │   ├─ Build AI prompt
      │   ├─ Call Claude AI
      │   ├─ Parse JSON response
      │   └─ Create GitHub issues
      │
      ▼
GitHub Issues Created ✅
```

### Issue Resolver Flow

```
GitHub Workflow
      │
      ▼
.github/scripts/issue_resolver.py
      │
      ├─ Read env vars (LABELS_TO_HANDLE, etc.)
      ├─ Initialize GitHub + Git clients
      │
      ▼
src/agents/issue_resolver.py
      │
      ├─ IssueResolver.__init__(repo, git_repo, labels)
      │
      ▼
IssueResolver.resolve_issue(specific_issue)
      │
      ├─ Select issue to work on
      ├─ Claim issue (add comment + label)
      ├─ Validate PROJECT_BRIEF.md
      ├─ Create git branch
      ├─ Call Claude AI with Read/Write tools
      ├─ Commit changes
      ├─ Push branch
      └─ Create Pull Request
      │
      ▼
Pull Request Created ✅
```

### QA Agent Flow

```
GitHub Workflow
      │
      ▼
.github/scripts/qa_agent.py
      │
      ├─ Read env vars (MAX_ISSUES_TO_REVIEW, etc.)
      ├─ Initialize GitHub client
      │
      ▼
src/agents/qa_agent.py
      │
      ├─ QAAgent.__init__(repo, max_issues, max_prs)
      │
      ▼
QAAgent.run_qa_check()
      │
      ├─ Gather context:
      │   ├─ Recent issues
      │   ├─ Recent PRs
      │   └─ Recent commits
      │
      ├─ Build QA analysis prompt
      ├─ Call Claude AI
      ├─ Parse JSON response
      │
      ├─ If problems found:
      │   └─ Create QA report issue
      │
      ▼
QA Report Created (if needed) ✅
```

## Component Responsibilities

### CI/CD Layer (`.github/scripts/`)

**Responsibilities:**
- ✅ Read environment variables
- ✅ Initialize external clients (GitHub, Git)
- ✅ Instantiate core agent classes
- ✅ Call agent methods
- ✅ Handle top-level errors
- ✅ Exit with appropriate codes

**Does NOT:**
- ❌ Contain business logic
- ❌ Make AI calls
- ❌ Process data
- ❌ Make decisions

### Core Logic Layer (`src/agents/`)

**Responsibilities:**
- ✅ Implement all business logic
- ✅ Make AI calls
- ✅ Process and validate data
- ✅ Make decisions
- ✅ Interact with GitHub API
- ✅ Handle git operations
- ✅ Provide testable interfaces

**Does NOT:**
- ❌ Read environment variables directly
- ❌ Initialize GitHub/Git clients
- ❌ Handle CI/CD concerns

## Benefits of This Architecture

### 1. **Separation of Concerns**

```
┌─────────────────────────┐
│   CI/CD Layer           │  ← Environment-specific
│   (GitHub Actions)      │     Configuration
└───────────┬─────────────┘     Error handling
            │
            ▼
┌─────────────────────────┐
│   Core Logic Layer      │  ← Business logic
│   (Agent Classes)       │     AI interactions
└─────────────────────────┘     Data processing
```

### 2. **Testability**

```
Before:                     After:
┌──────────────┐           ┌──────────────┐
│ Monolithic   │           │ Core Agent   │ ← Can mock GitHub API
│ CI Script    │           │ Class        │ ← Can unit test
│              │           │              │ ← Can integration test
│ (Hard to     │           │ (Easy to     │
│  test)       │           │  test)       │
└──────────────┘           └──────────────┘
```

### 3. **Reusability**

```
┌─────────────────────────────────────────┐
│         Core Agent Classes              │
│         (src/agents/)                   │
└──────────┬──────────────────────────────┘
           │
           ├─► GitHub Actions Workflows
           ├─► CLI Tools
           ├─► API Endpoints
           ├─► Local Scripts
           └─► Unit Tests
```

### 4. **Maintainability**

```
Single Source of Truth:

src/agents/issue_generator.py
    ↓
Used by:
  - .github/scripts/issue_generator.py (CI)
  - CLI tool (future)
  - Tests
  - API (future)

Change once, works everywhere ✅
```

## File Size Comparison

### Before Refactoring

```
.github/scripts/issue_generator.py    225 lines (monolithic)
.github/scripts/issue_resolver.py     398 lines (monolithic)
.github/scripts/qa_agent.py           404 lines (monolithic)
                                      ─────────
                                      1027 lines total
```

### After Refactoring

```
Core Logic (src/agents/):
  issue_generator.py                  245 lines
  issue_resolver.py                   399 lines
  qa_agent.py                         421 lines
                                      ─────────
                                      1065 lines

CI Wrappers (.github/scripts/):
  issue_generator.py                   52 lines
  issue_resolver.py                    61 lines
  qa_agent.py                          59 lines
                                      ─────────
                                       172 lines

Total:                                1237 lines
```

**Net increase:** ~210 lines (17% increase)
- Added proper class structure
- Added docstrings
- Added error handling
- Added validation
- **Gained:** Testability, reusability, maintainability

## Migration Path

```
Step 1: Create Core Modules
  ✅ src/agents/__init__.py
  ✅ src/agents/issue_generator.py
  ✅ src/agents/issue_resolver.py
  ✅ src/agents/qa_agent.py

Step 2: Refactor to Classes
  ✅ Extract logic from scripts
  ✅ Create class interfaces
  ✅ Add proper methods

Step 3: Create Thin Wrappers
  ✅ Replace .github/scripts/*.py
  ✅ Keep only env setup + agent calls
  ✅ Maintain backward compatibility

Step 4: Document
  ✅ Architecture docs
  ✅ Migration guide
  ✅ Usage examples

Step 5: Verify
  ✅ All workflows still work
  ✅ No breaking changes
  ✅ Improved code quality
```

---

**Architecture Version:** 2.0  
**Last Updated:** November 2025  
**Status:** ✅ Production Ready

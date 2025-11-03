# Claude Agent Workflow Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Container                         │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              entrypoint.sh (Shell)                     │ │
│  │  • Validate environment variables                      │ │
│  │  • Authenticate with GitHub CLI                        │ │
│  │  • Execute Python workflow                             │ │
│  └────────────────┬───────────────────────────────────────┘ │
│                   │                                          │
│                   ▼                                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         agent_workflow.py (Python)                     │ │
│  │                                                         │ │
│  │  ┌──────────────────────────────────────────────────┐ │ │
│  │  │  AgentWorkflow Class                             │ │ │
│  │  │  • Configuration management                      │ │ │
│  │  │  • Logging setup                                 │ │ │
│  │  │  • API client initialization                     │ │ │
│  │  │  • Workflow orchestration                        │ │ │
│  │  └──────────────────────────────────────────────────┘ │ │
│  │                                                         │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │ │
│  │  │  config.py   │  │  logger.py   │  │  tests/     │ │ │
│  │  │  • AgentConfig│  │  • Structured│  │  • Unit     │ │ │
│  │  │  • Validation│  │    logging   │  │    tests    │ │ │
│  │  └──────────────┘  └──────────────┘  └─────────────┘ │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Detailed Workflow Sequence

```
START
  │
  ├─► [1] Load Configuration
  │    ├─ Read environment variables
  │    ├─ Validate required fields
  │    └─ Create AgentConfig instance
  │
  ├─► [2] Initialize Logging
  │    ├─ Setup logger with timestamps
  │    └─ Configure log levels
  │
  ├─► [3] Initialize API Clients
  │    ├─ GitHub API (PyGithub)
  │    ├─ Anthropic API (Claude)
  │    └─ Git operations (GitPython)
  │
  ├─► [4] Parse Repository Info
  │    ├─ Extract owner from URL
  │    └─ Extract repo name from URL
  │
  ├─► [5] Clone Repository
  │    ├─ Build authenticated URL
  │    ├─ Clone to /workspace/repo
  │    └─ Configure git user
  │
  ├─► [6] Get Issue Details
  │    ├─ If issue_number provided
  │    │   └─ Fetch specific issue
  │    └─ Else
  │        └─ Auto-select first open issue
  │
  ├─► [7] Create Fix Branch
  │    ├─ Generate branch name: fix/issue-{N}-{timestamp}
  │    └─ Checkout new branch
  │
  ├─► [8] Analyze Codebase
  │    ├─ Detect languages (py, js, go, etc.)
  │    ├─ Find framework files
  │    └─ Build context for Claude
  │
  ├─► [9] Generate Fix with Claude
  │    ├─ Build context-aware prompt
  │    ├─ Call Claude API (claude-3-5-sonnet)
  │    └─ Parse response (JSON or text)
  │
  ├─► [10] Apply Fix
  │    ├─ Parse fix instructions
  │    ├─ Create/modify files
  │    └─ Write code changes
  │
  ├─► [11] Commit Changes
  │    ├─ Stage all changes (git add -A)
  │    ├─ Create commit message
  │    └─ Commit with issue reference
  │
  ├─► [12] Push Branch
  │    ├─ Push to origin
  │    └─ Set upstream tracking
  │
  ├─► [13] Create Pull Request
  │    ├─ Build PR title
  │    ├─ Build PR description
  │    ├─ Create PR via GitHub API
  │    └─ Link to issue (Closes #N)
  │
  └─► [14] Complete
       ├─ Log success with PR URL
       └─ Return exit code 0
```

## Data Flow Diagram

```
┌─────────────────┐
│  Environment    │
│  Variables      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AgentConfig    │
│  • Validation   │
│  • Type safety  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│                   AgentWorkflow                          │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   GitHub     │  │   Claude     │  │     Git      │ │
│  │     API      │  │     API      │  │  Operations  │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                  │                  │         │
└─────────┼──────────────────┼──────────────────┼─────────┘
          │                  │                  │
          ▼                  ▼                  ▼
    ┌─────────┐        ┌─────────┐       ┌─────────┐
    │ Fetch   │        │Generate │       │ Clone   │
    │ Issue   │        │  Fix    │       │ & Push  │
    └────┬────┘        └────┬────┘       └────┬────┘
         │                  │                  │
         └──────────────────┼──────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Pull Request  │
                    │   Created     │
                    └───────────────┘
```

## Component Interaction

```
┌──────────────────────────────────────────────────────────────┐
│                        User Input                             │
│  • GITHUB_TOKEN                                               │
│  • ANTHROPIC_API_KEY                                          │
│  • REPO_URL                                                   │
│  • ISSUE_NUMBER (optional)                                    │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                    Docker Container                           │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Shell Layer (entrypoint.sh)                           │  │
│  │  • Minimal validation                                  │  │
│  │  • GitHub CLI auth                                     │  │
│  │  • Python invocation                                   │  │
│  └──────────────────────┬─────────────────────────────────┘  │
│                         │                                     │
│                         ▼                                     │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Python Layer                                          │  │
│  │                                                         │  │
│  │  ┌──────────────┐                                      │  │
│  │  │   config.py  │◄─────────────────┐                  │  │
│  │  │              │                   │                  │  │
│  │  │ • Load env   │                   │                  │  │
│  │  │ • Validate   │                   │                  │  │
│  │  └──────┬───────┘                   │                  │  │
│  │         │                           │                  │  │
│  │         ▼                           │                  │  │
│  │  ┌──────────────┐            ┌─────┴──────┐          │  │
│  │  │  logger.py   │            │  workflow  │          │  │
│  │  │              │◄───────────┤            │          │  │
│  │  │ • Setup logs │            │ • Parse    │          │  │
│  │  │ • Format     │            │ • Clone    │          │  │
│  │  └──────────────┘            │ • Analyze  │          │  │
│  │                              │ • Fix      │          │  │
│  │                              │ • Commit   │          │  │
│  │                              │ • PR       │          │  │
│  │                              └────────────┘          │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                    External Services                          │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   GitHub     │  │  Anthropic   │  │     Git      │       │
│  │              │  │              │  │   Remote     │       │
│  │ • Issues API │  │ • Claude API │  │ • Push       │       │
│  │ • PR API     │  │ • Sonnet 3.5 │  │ • Clone      │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└──────────────────────────────────────────────────────────────┘
```

## Error Handling Flow

```
┌─────────────────┐
│  Any Operation  │
└────────┬────────┘
         │
         ├─► Success ──────────────────────────► Continue
         │
         └─► Error
              │
              ├─► Validation Error
              │    ├─ Log error
              │    └─ Exit code 1
              │
              ├─► API Error (GitHub/Claude)
              │    ├─ Log with context
              │    ├─ Print traceback
              │    └─ Exit code 1
              │
              ├─► Git Error
              │    ├─ Log operation details
              │    ├─ Print error
              │    └─ Exit code 1
              │
              └─► Unexpected Error
                   ├─ Log full traceback
                   ├─ Print error message
                   └─ Exit code 1
```

## File System Layout

```
/workspace/                    (Container workspace)
    │
    └── repo/                  (Cloned repository)
        ├── .git/
        ├── src/
        ├── tests/
        └── [repository files]

/agent/                        (Agent code)
    │
    └── src/
        ├── agent_workflow.py
        ├── config.py
        └── utils/
            └── logger.py

/agent-scripts/                (Shell scripts)
    └── entrypoint.sh
```

## Logging Flow

```
┌─────────────────────────────────────────────────────────┐
│                    Logger Setup                          │
│  • Name: "claude-agent"                                  │
│  • Level: INFO                                           │
│  • Handler: StreamHandler (stdout)                       │
│  • Format: [YYYY-MM-DD HH:MM:SS] LEVEL: Message         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Log Messages                            │
│                                                          │
│  [2024-11-13 10:30:45] INFO: Agent workflow initialized │
│  [2024-11-13 10:30:46] INFO: Cloning repository...      │
│  [2024-11-13 10:30:50] INFO: Repository cloned          │
│  [2024-11-13 10:30:51] INFO: Using issue #42            │
│  [2024-11-13 10:30:52] INFO: Created branch: fix/...    │
│  [2024-11-13 10:30:55] INFO: Analyzing codebase...      │
│  [2024-11-13 10:31:00] INFO: Generating fix...          │
│  [2024-11-13 10:31:15] INFO: Claude response received   │
│  [2024-11-13 10:31:16] INFO: Applying fix...            │
│  [2024-11-13 10:31:17] INFO: Modified: src/main.py      │
│  [2024-11-13 10:31:18] INFO: Committing changes...      │
│  [2024-11-13 10:31:20] INFO: Changes committed          │
│  [2024-11-13 10:31:22] INFO: Pushed branch              │
│  [2024-11-13 10:31:25] INFO: Creating pull request...   │
│  [2024-11-13 10:31:27] INFO: Pull request created: ...  │
│  [2024-11-13 10:31:27] INFO: Workflow Completed!        │
└─────────────────────────────────────────────────────────┘
```

## API Integration Points

```
┌────────────────────────────────────────────────────────────┐
│                    GitHub API (PyGithub)                    │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Authentication: Personal Access Token                │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  Operations:                                                │
│  • get_repo(owner/name)         → Repository object        │
│  • get_issues(state='open')     → Issue list               │
│  • get_issue(number)            → Issue details            │
│  • create_pull(title, body, ..) → Pull Request             │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                  Anthropic API (Claude)                     │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Authentication: API Key                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  Operations:                                                │
│  • messages.create()            → Claude response          │
│    - model: claude-3-5-sonnet-20241022                     │
│    - max_tokens: 4096                                      │
│    - messages: [{"role": "user", "content": "..."}]        │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                   Git Operations (GitPython)                │
│                                                             │
│  Operations:                                                │
│  • Repo.clone_from(url, path)   → Clone repository         │
│  • repo.git.checkout('-b', ..)  → Create branch            │
│  • repo.index.add([...])        → Stage changes            │
│  • repo.index.commit(msg)       → Commit changes           │
│  • origin.push(branch)          → Push to remote           │
└────────────────────────────────────────────────────────────┘
```

## Success Path Timeline

```
Time    Action                           Component
─────────────────────────────────────────────────────────────
00:00   Start container                  Docker
00:01   Validate environment             entrypoint.sh
00:02   Authenticate GitHub CLI          entrypoint.sh
00:03   Initialize Python workflow       agent_workflow.py
00:04   Load configuration               config.py
00:05   Setup logging                    logger.py
00:06   Initialize API clients           agent_workflow.py
00:07   Parse repository URL             agent_workflow.py
00:10   Clone repository                 GitPython
00:15   Fetch issue details              PyGithub
00:16   Create fix branch                GitPython
00:17   Analyze codebase                 agent_workflow.py
00:20   Generate fix with Claude         Anthropic API
00:35   Parse Claude response            agent_workflow.py
00:36   Apply code changes               Python file I/O
00:37   Stage changes                    GitPython
00:38   Commit changes                   GitPython
00:40   Push branch                      GitPython
00:45   Create pull request              PyGithub
00:46   Log completion                   logger.py
00:47   Exit successfully                agent_workflow.py
```

## Legend

```
┌─────┐
│ Box │  Component or process
└─────┘

  │
  ▼     Flow direction

  ├─►   Branch in flow

  ◄──   Data/control flow

  •     Bullet point / feature
```

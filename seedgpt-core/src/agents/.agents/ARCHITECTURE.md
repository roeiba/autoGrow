# Specialized Agents Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     GitHub Repository                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Marketing   │  │   Product    │  │    Sales     │          │
│  │   Issues     │  │   Issues     │  │   Issues     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ Creates Issues
                              │
┌─────────────────────────────────────────────────────────────────┐
│                   Specialized Agents Layer                       │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Marketing   │  │   Product    │  │    Sales     │          │
│  │    Agent     │  │    Agent     │  │    Agent     │          │
│  │              │  │              │  │              │          │
│  │ Labels:      │  │ Labels:      │  │ Labels:      │          │
│  │ • marketing  │  │ • product    │  │ • sales      │          │
│  │ • growth     │  │ • feature    │  │ • revenue    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                  │                  │                 │
│         └──────────────────┼──────────────────┘                 │
│                            │ Inherits                           │
│                            ▼                                    │
│                  ┌──────────────────┐                           │
│                  │  BaseIssueAgent  │                           │
│                  │   (Abstract)     │                           │
│                  └──────────────────┘                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Uses
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Core Services Layer                         │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Deduplication│  │ Rate Limiter │  │  Feedback    │          │
│  │   Checker    │  │              │  │   Analyzer   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   GitHub     │  │   Claude AI  │  │   Outcome    │          │
│  │   Helpers    │  │   (CLI/API)  │  │   Tracker    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

## Class Hierarchy

```
BaseIssueAgent (ABC)
│
├── Properties:
│   ├── repo: Repository
│   ├── config: AgentConfig
│   ├── duplicate_checker: IssueDuplicateChecker
│   ├── outcome_tracker: OutcomeTracker
│   ├── feedback_analyzer: FeedbackAnalyzer
│   └── rate_limiter: RateLimiter
│
├── Abstract Methods:
│   ├── get_agent_config() -> AgentConfig
│   └── build_domain_prompt(context) -> str
│
├── Concrete Methods:
│   ├── check_and_generate() -> bool
│   ├── _filter_domain_issues(issues) -> List
│   ├── _generate_issues(needed, open_issues)
│   ├── _build_prompt(context, guidance) -> str
│   ├── _call_claude(prompt) -> str
│   └── _parse_and_create_issues(response, needed, issues)
│
└── Subclasses:
    │
    ├── MarketingAgent
    │   ├── get_agent_config() -> AgentConfig
    │   │   └── domain: "marketing"
    │   │       labels: ["marketing", "growth"]
    │   └── build_domain_prompt(context) -> str
    │       └── Marketing-specific focus areas
    │
    ├── ProductAgent
    │   ├── get_agent_config() -> AgentConfig
    │   │   └── domain: "product"
    │   │       labels: ["product", "feature"]
    │   └── build_domain_prompt(context) -> str
    │       └── Product-specific focus areas
    │
    └── SalesAgent
        ├── get_agent_config() -> AgentConfig
        │   └── domain: "sales"
        │       labels: ["sales", "revenue"]
        └── build_domain_prompt(context) -> str
            └── Sales-specific focus areas
```

## Data Flow

```
┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│ Initialize Agent            │
│ - Load config               │
│ - Setup services            │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ Check Rate Limits           │
│ - Can generate?             │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ Count Domain Issues         │
│ - Filter by labels          │
│ - Compare to min_issues     │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ Need Issues?                │
└──────┬──────────────────────┘
       │
       ├─ No ──> Exit
       │
       ▼ Yes
┌─────────────────────────────┐
│ Gather Context              │
│ - README                    │
│ - Recent commits            │
│ - Project brief             │
│ - Feedback data             │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ Build Prompt                │
│ - Base prompt               │
│ - Domain-specific prompt    │
│ - Feedback adjustments      │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ Call Claude AI              │
│ - CLI or API                │
│ - Get JSON response         │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ Parse Response              │
│ - Extract JSON              │
│ - Add domain labels         │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ Deduplication Check         │
│ - Title similarity          │
│ - Body similarity           │
│ - Semantic similarity       │
│ - Quality gates             │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ Create Issues               │
│ - For each unique issue     │
│ - Add agent signature       │
│ - Apply labels              │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ Record Metrics              │
│ - Update rate limiter       │
│ - Log statistics            │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────┐
│    End      │
└─────────────┘
```

## Component Interactions

```
┌─────────────────┐
│ MarketingAgent  │
└────────┬────────┘
         │
         │ 1. check_and_generate()
         ▼
┌─────────────────────────────────────┐
│ BaseIssueAgent                      │
│                                     │
│ 2. Check Rate Limits ──────────────┐│
│                                     ││
│ 3. Filter Domain Issues ───────────┤│
│                                     ││
│ 4. Generate if needed ─────────────┤│
│                                     ││
└─────────────────────────────────────┘│
         │                             │
         │ 5. Call services            │
         ▼                             │
┌─────────────────────────────────────┐│
│ Services                            ││
│                                     ││
│ ┌─────────────────┐                ││
│ │ RateLimiter     │◄───────────────┘│
│ └─────────────────┘                 │
│                                     │
│ ┌─────────────────┐                 │
│ │ Duplicate       │◄────────────────┤
│ │ Checker         │                 │
│ └─────────────────┘                 │
│                                     │
│ ┌─────────────────┐                 │
│ │ Claude AI       │◄────────────────┤
│ │ (CLI/API)       │                 │
│ └─────────────────┘                 │
│                                     │
│ ┌─────────────────┐                 │
│ │ GitHub API      │◄────────────────┘
│ └─────────────────┘                 │
└─────────────────────────────────────┘
```

## Configuration Flow

```
┌──────────────────────┐
│  AgentConfig         │
│  (Data Class)        │
├──────────────────────┤
│ • domain             │
│ • default_labels     │
│ • min_issues         │
│ • focus_areas        │
│ • priority_keywords  │
└──────────────────────┘
          │
          │ Defined by
          ▼
┌──────────────────────┐
│ get_agent_config()   │
│ (Abstract Method)    │
└──────────────────────┘
          │
          │ Implemented by
          ▼
┌──────────────────────────────────────┐
│ MarketingAgent.get_agent_config()    │
│ ProductAgent.get_agent_config()      │
│ SalesAgent.get_agent_config()        │
└──────────────────────────────────────┘
          │
          │ Used by
          ▼
┌──────────────────────┐
│ BaseIssueAgent       │
│ __init__()           │
└──────────────────────┘
```

## Prompt Building Flow

```
┌─────────────────────┐
│ Repository Context  │
├─────────────────────┤
│ • README            │
│ • Commits           │
│ • Project Brief     │
│ • Open Issues       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────┐
│ _build_prompt()             │
│ (Base Class)                │
├─────────────────────────────┤
│ 1. Base prompt              │
│ 2. Call build_domain_prompt │
│ 3. Add guidance             │
│ 4. Add JSON format          │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ build_domain_prompt()       │
│ (Subclass Implementation)   │
├─────────────────────────────┤
│ • Marketing focus areas     │
│ • Product focus areas       │
│ • Sales focus areas         │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────┐
│ Complete Prompt     │
│ → Claude AI         │
└─────────────────────┘
```

## Label Management

```
┌──────────────────────────────┐
│ Issue Creation               │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Ensure Domain Labels         │
│                              │
│ if 'labels' not in issue:    │
│   issue['labels'] =          │
│     config.default_labels    │
│ else:                        │
│   issue['labels'] =          │
│     issue['labels'] +        │
│     config.default_labels    │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ GitHub Issue                 │
│                              │
│ Labels:                      │
│ • [domain label]             │
│ • [category label]           │
│ • [additional labels]        │
└──────────────────────────────┘
```

## Extension Pattern

```
┌─────────────────────────────┐
│ Create New Agent            │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ 1. Inherit BaseIssueAgent   │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ 2. Implement                │
│    get_agent_config()       │
│    - Define domain          │
│    - Set labels             │
│    - Configure settings     │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ 3. Implement                │
│    build_domain_prompt()    │
│    - Add focus areas        │
│    - Define considerations  │
│    - Set priorities         │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ 4. Export in __init__.py    │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ 5. Ready to Use!            │
└─────────────────────────────┘
```

## Design Patterns Used

### 1. Template Method Pattern
- `BaseIssueAgent` defines the algorithm skeleton
- Subclasses implement specific steps

### 2. Strategy Pattern
- Different domain prompts for different agents
- Configurable through `AgentConfig`

### 3. Factory Pattern
- `AgentConfig` creates configuration objects
- Each agent factory produces its own config

### 4. Dependency Injection
- Services injected into base class
- Loose coupling between components

### 5. Single Responsibility
- Each agent handles one domain
- Each service handles one concern

## Key Benefits

1. **Maintainability**: Common logic in one place
2. **Extensibility**: Easy to add new agents
3. **Testability**: Each component can be tested independently
4. **Reusability**: Services shared across agents
5. **Scalability**: Independent rate limiting per agent
6. **Flexibility**: Configurable through `AgentConfig`

## Performance Characteristics

- **Memory**: ~50MB per agent instance
- **API Calls**: 1 Claude + 2-3 GitHub per generation
- **Execution Time**: 10-30 seconds per agent
- **Concurrency**: Safe to run agents in parallel
- **Rate Limits**: Independent per agent

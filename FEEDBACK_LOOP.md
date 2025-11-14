# 🔄 AutoGrow Feedback Loop System

## Overview

The **Feedback Loop System** enables AutoGrow to learn from its own performance and continuously improve. It tracks issue resolution success rates, PR merge status, and time-to-resolution metrics, then uses this data to dynamically adapt issue generation strategies.

## 🎯 Key Features

### 1. **Outcome Tracking**
- Records every issue resolution attempt
- Tracks PR creation, merge status, and timing
- Monitors success rates by issue type
- Stores data persistently in SQLite database

### 2. **Adaptive Generation**
- Weights issue types by historical success rate
- Prioritizes high-performing issue types
- Reduces generation of low-success types
- Injects success rate data into generation prompts

### 3. **Performance Analytics**
- Overall success metrics
- Per-type success rates with visual bars
- Time-to-resolution analysis
- Recommended type distribution

### 4. **Self-Learning**
- Exponential weight calculation (higher success = exponentially higher weight)
- Confidence adjustment based on sample size
- Dynamic prompt enhancement based on feedback

## 📊 Data Model

### Resolution Statuses

| Status | Description |
|--------|-------------|
| `pending` | Issue resolution started but not complete |
| `resolved` | PR created successfully |
| `merged` | PR was merged into main branch |
| `closed` | PR was closed without merging |
| `failed` | Failed to create PR or make changes |

### Tracked Metrics

- **Issue number and title**
- **Issue type** (feature, bug, documentation, etc.)
- **Labels** (array of GitHub labels)
- **Status** (current resolution status)
- **PR number** (if created)
- **Timestamps** (created, resolved, merged)
- **Time to resolve** (minutes from start to PR creation)
- **Time to merge** (minutes from start to merge)
- **Files changed** (count of modified files)
- **Error message** (if failed)

## 🚀 How It Works

### Issue Resolution Flow

```
1. Issue Resolver starts working
   ↓
2. Records attempt in outcome tracker (status: PENDING)
   ↓
3a. If fails → Update status to FAILED + error message
3b. If succeeds → Update status to RESOLVED + PR number
   ↓
4. Background job checks PR status periodically
   ↓
5a. If PR merged → Update status to MERGED
5b. If PR closed → Update status to CLOSED
```

### Issue Generation Flow

```
1. Issue Generator starts
   ↓
2. Queries outcome tracker for historical data
   ↓
3. Feedback Analyzer computes:
   - Success rates by type
   - High/low priority types
   - Recommended distribution
   ↓
4. Generates adaptive prompt guidance
   ↓
5. Claude generates issues with:
   - Emphasis on high-success types
   - De-emphasis on low-success types
   - Context about what works
```

## 📁 File Structure

```
src/
├── utils/
│   ├── outcome_tracker.py      # Core tracking database
│   └── feedback_analyzer.py    # Analytics and guidance
├── scripts/
│   ├── view_feedback_metrics.py   # CLI to view metrics
│   └── update_pr_status.py        # Background PR status updater
└── agents/
    ├── issue_resolver.py       # Updated with tracking
    └── issue_generator.py      # Updated with adaptive logic
```

## 🔧 Usage

### View Metrics

```bash
# Show comprehensive report
python src/scripts/view_feedback_metrics.py

# Show only recent outcomes
python src/scripts/view_feedback_metrics.py --recent --limit 20

# Export as JSON
python src/scripts/view_feedback_metrics.py --export > metrics.json

# Analyze last 7 days only
python src/scripts/view_feedback_metrics.py --days 7
```

### Update PR Status

```bash
# Check and update PR merge status
export GITHUB_TOKEN=your_token
export GITHUB_REPOSITORY=owner/repo
python src/scripts/update_pr_status.py
```

### Programmatic Access

```python
from src.utils.outcome_tracker import OutcomeTracker, ResolutionStatus
from src.utils.feedback_analyzer import FeedbackAnalyzer

# Initialize
tracker = OutcomeTracker()
analyzer = FeedbackAnalyzer(tracker)

# Record an attempt
tracker.record_attempt(
    issue_number=42,
    issue_title="Add dark mode",
    labels=["feature", "ui"],
    status=ResolutionStatus.PENDING
)

# Update status
tracker.update_status(
    issue_number=42,
    status=ResolutionStatus.RESOLVED,
    pr_number=123,
    files_changed=5
)

# Get metrics
metrics = tracker.get_type_metrics(days=30)
overall = tracker.get_overall_stats()

# Get generation guidance
guidance = analyzer.get_generation_guidance()
print(guidance.high_priority_types)
print(guidance.prompt_adjustments)
```

## 📈 Metrics Report Example

```
================================================================================
📊 AUTOGROW FEEDBACK LOOP REPORT
================================================================================

OVERALL STATISTICS:
  Total Attempts:     15
  Resolved:           12 (80.0%)
  Merged:             8 (53.3%)
  Failed:             3
  Avg Resolution Time: 45 minutes
  Avg Merge Time:      120 minutes

SUCCESS RATE BY TYPE:
--------------------------------------------------------------------------------
  feature         ████████████████████ 100.0% (5/5) [weight: 2.23]
                  ⏱️  Avg resolution: 38m
  bug             ████████████████     85.7% (6/7) [weight: 1.89]
                  ⏱️  Avg resolution: 42m
  documentation   ████████             50.0% (1/2) [weight: 0.82]
                  ⏱️  Avg resolution: 25m
  test            ████                 33.3% (0/1) [weight: 0.35]

RECENT OUTCOMES:
--------------------------------------------------------------------------------
  ✅ #45  [feature     ] Add user authentication system
  ✅ #44  [bug         ] Fix login validation error
  🔄 #43  [feature     ] Implement dashboard widgets
  ❌ #42  [test        ] Add integration tests for API
  ✅ #41  [bug         ] Resolve memory leak in cache

================================================================================
```

## 🎯 Weight Calculation

The system uses **exponential weighting** with confidence adjustment:

```python
# Base weight: exponential scaling from success rate
base_weight = exp(success_rate * 1.5) / e

# Confidence factor: based on sample size
confidence = min(1.0, sample_size / 5)

# Final weight with confidence adjustment
weight = base_weight * confidence + (1 - confidence) * 0.5
```

**Examples:**
- 100% success (10 samples): weight = 2.23
- 80% success (5 samples): weight = 1.52
- 50% success (5 samples): weight = 0.82
- 30% success (2 samples): weight = 0.42 (reduced by low confidence)

## 🔮 Adaptive Prompt Enhancement

The feedback analyzer generates dynamic prompt adjustments:

```
🎯 ADAPTIVE GENERATION GUIDANCE (Based on Success Rate Feedback)

**PRIORITIZE these issue types** (proven high success rate): feature, bug
  → feature: 100% success rate (5/5 merged)

**REDUCE these issue types** (lower success rate): test, refactor

**FAST RESOLUTION**: documentation issues resolve in ~25 minutes on average

**Current Success Metrics:**
📊 Overall success rate: 80% (12/15 resolved) | ✅ Focus on: feature, bug | ⚠️  Avoid: test
```

## 📦 Database Location

The SQLite database is stored at:
```
.autogrow/outcomes.db
```

Add `.autogrow/` to `.gitignore` to keep metrics local.

## 🔄 Background Jobs (Optional)

To automatically update PR merge status, add a scheduled workflow:

```yaml
# .github/workflows/update-pr-status.yml
name: Update PR Status
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r src/requirements.txt
      - run: python src/scripts/update_pr_status.py
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPOSITORY: ${{ github.repository }}
```

## 🧪 Testing

The feedback loop system is fully integrated into the existing agents:

1. **Automatic tracking** - Issue resolver automatically records all attempts
2. **Zero config** - Works out of the box with default settings
3. **Graceful degradation** - If no data exists, uses default generation
4. **CI compatible** - Dry mode skips database writes for testing

## 🎓 Learning Examples

### Example 1: High Feature Success
```
After 10 successful feature issues:
→ System increases feature weight from 1.0 → 2.23
→ Generation prompt emphasizes features
→ More features get generated automatically
```

### Example 2: Test Issues Failing
```
After 3 failed test issues:
→ System reduces test weight from 1.0 → 0.35
→ Generation prompt de-emphasizes tests
→ Fewer test issues generated until success improves
```

### Example 3: Documentation Is Fast
```
Documentation resolves in 25 minutes (vs 45m average):
→ Analyzer notes fast resolution time
→ Suggests documentation for quick wins
→ Balances with other priorities
```

## 🚀 Future Enhancements

Potential improvements for the feedback loop:

- [ ] Multi-repository metrics aggregation
- [ ] A/B testing of different generation strategies
- [ ] Machine learning model for optimal type distribution
- [ ] Integration with GitHub Insights API
- [ ] Real-time dashboard visualization
- [ ] Slack/Discord notifications for milestone achievements
- [ ] Comparison metrics against other projects

## 📝 Contributing

When extending the feedback loop system:

1. **Maintain backward compatibility** - Old databases should still work
2. **Add database migrations** - Use ALTER TABLE for schema changes
3. **Update documentation** - Keep this file in sync with changes
4. **Test with dry mode** - Ensure CI tests don't write to database
5. **Log insights clearly** - Help users understand what's being learned

## 🐛 Troubleshooting

### No metrics showing up
- Check if `.autogrow/outcomes.db` exists
- Verify issue resolver is running with `dry_mode=False`
- Check if outcomes are being recorded (look for "📊 Outcome tracking" logs)

### Metrics seem wrong
- Check database directly: `sqlite3 .autogrow/outcomes.db "SELECT * FROM outcomes"`
- Verify PR status updater is running periodically
- Ensure timestamps are in ISO format

### Generation not adapting
- Verify you have at least 3 samples per type (minimum for analysis)
- Check if guidance is being generated (look for "📊 Analyzing feedback" logs)
- Review prompt adjustments with `--export` flag

---

**Built for AutoGrow** - The world's first fully autonomous, self-growing software project that learns from its own performance.

# AutoGrow Scripts

Utility scripts for managing and monitoring AutoGrow agents.

## 📊 Feedback Loop Scripts

### view_feedback_metrics.py

View outcome tracking metrics and success rate analytics.

**Usage:**
```bash
# Show comprehensive report
python src/scripts/view_feedback_metrics.py

# Show only recent outcomes
python src/scripts/view_feedback_metrics.py --recent --limit 20

# Export as JSON
python src/scripts/view_feedback_metrics.py --export > metrics.json

# Analyze last 7 days
python src/scripts/view_feedback_metrics.py --days 7
```

**Options:**
- `--recent` - Show only recent outcomes
- `--export` - Export metrics as JSON
- `--days N` - Analyze last N days (default: 30)
- `--limit N` - Number of recent items (default: 10)

### update_pr_status.py

Background job to check PR merge status and update outcome tracking.

**Usage:**
```bash
export GITHUB_TOKEN=your_token
export GITHUB_REPOSITORY=owner/repo
python src/scripts/update_pr_status.py
```

**Recommended:** Run periodically via cron or GitHub Actions (every 6 hours).

## 📖 More Information

See [FEEDBACK_LOOP.md](../../FEEDBACK_LOOP.md) for complete documentation.

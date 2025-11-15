# Quick Error Reference

## Common Errors & Solutions

### 🔴 Credit Balance Too Low

**Error**:
```
❌ Claude CLI credit balance is too low. Please add credits to your Claude account.
Error: Claude CLI credit balance is too low: Credit balance is too low
```

**Fix**: Add credits at https://claude.ai/settings/billing

---

### 🔴 Rate Limit Exceeded

**Error**:
```
❌ Anthropic API rate limit exceeded.
Please retry after: 1731585600
```

**Fix**: 
- Wait for the specified time
- Implement rate limiting
- Upgrade API plan

---

### 🔴 Authentication Failed

**Error**:
```
❌ Authentication failed. Please check your API credentials.
```

**Fix**:
- Check `ANTHROPIC_API_KEY` environment variable
- Verify API key is valid
- Ensure proper permissions

---

### 🔴 GitHub API Error

**Error**:
```
❌ GitHub API error occurred.
```

**Fix**:
- Check `GITHUB_TOKEN` is valid
- Verify repository permissions
- Check GitHub status

---

## Quick Debugging Commands

```bash
# Check if API keys are set
echo $ANTHROPIC_API_KEY | cut -c1-10
echo $GITHUB_TOKEN | cut -c1-10

# Test error handling
python3 .agents/scripts/test_credit_error.py

# Run in dry mode (no actual API calls)
DRY_MODE=true python3 .github/scripts/issue_generator.py

# View recent errors
grep "ERROR" logs/agent.log | tail -20

# Check Claude CLI version
claude --version

# Test Claude CLI authentication
claude -p "Hello" --allowedTools "Read"
```

## Error Code Reference

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 1 | General error (check logs) |
| 2 | Configuration error |
| 3 | Authentication error |
| 4 | Rate limit error |

## Need Help?

1. Check logs: `logs/agent.log`
2. Review docs: `docs/ERROR_HANDLING.md`
3. Test locally: `DRY_MODE=true`
4. Open issue with error details

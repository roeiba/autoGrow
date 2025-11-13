# Claude Agent Caching - Quick Reference

## Enable/Disable Caching

```python
# Enabled (default)
agent = ClaudeAgent(enable_cache=True)

# Disabled
agent = ClaudeAgent(enable_cache=False)
```

## Basic Operations

```python
# Query with cache (default)
result = agent.query("prompt")

# Query without cache
result = agent.query("prompt", use_cache=False)

# Custom TTL
result = agent.query("prompt", cache_ttl=1800)  # 30 minutes
```

## Cache Management

```python
# View stats
stats = agent.get_cache_stats()
print(f"Hit rate: {stats['hit_rate']}")

# Clear all cache
agent.clear_cache()

# Invalidate specific entry
agent.invalidate_cache("query", prompt="specific prompt")
```

## Default TTLs

| Operation | TTL | Seconds |
|-----------|-----|---------|
| query | 1 hour | 3600 |
| code_review | 24 hours | 86400 |
| generate_docs | 7 days | 604800 |
| fix_code | 5 minutes | 300 |
| batch_process | 1 hour | 3600 |

## Configuration

```python
agent = ClaudeAgent(
    enable_cache=True,          # Enable caching
    cache_dir="/custom/path",   # Cache directory
    cache_max_size=5000,        # Max entries
    cache_ttl=7200              # Default TTL (seconds)
)
```

## Cache Statistics

```python
stats = agent.get_cache_stats()
# Returns:
{
    'size': 42,              # Number of cached entries
    'max_size': 1000,        # Maximum cache size
    'hits': 100,             # Cache hits
    'misses': 50,            # Cache misses
    'hit_rate': '66.67%',    # Hit rate percentage
    'total_requests': 150    # Total requests
}
```

## Examples

### Example 1: Batch Processing
```python
agent = ClaudeAgent(enable_cache=True)

# First run - caches all results
results = agent.batch_process("./src", "Review code")

# Second run - uses cached results
results = agent.batch_process("./src", "Review code")
```

### Example 2: Code Review
```python
# Uses 24-hour cache
result = agent.code_review("app.py")

# Skip cache
result = agent.code_review("app.py", use_cache=False)
```

### Example 3: Documentation
```python
# Uses 7-day cache
result = agent.generate_docs("api.py")
```

## Performance Tips

1. **Enable caching** for batch operations (default)
2. **Use longer TTLs** for stable content (docs, reviews)
3. **Use shorter TTLs** for frequently changing content (fixes)
4. **Monitor hit rates** with `get_cache_stats()`
5. **Clear cache** after major code changes

## Cost Savings

- **50% hit rate** → 50% cost reduction
- **90% hit rate** → 90% cost reduction
- **Cache hits** are 1000x faster than API calls

## Troubleshooting

### Low Hit Rate
- Check if prompts are slightly different
- Increase TTL values
- Increase cache size

### Stale Cache
- Call `agent.clear_cache()`
- Invalidate specific entries
- Reduce TTL for that operation

### Cache Not Working
- Verify `enable_cache=True`
- Check `agent.cache` is not None
- Verify disk permissions for cache_dir

## More Information

- Full documentation: `CACHING.md`
- Demo script: `examples/caching_demo.py`
- Tests: `tests/unit/test_claude_cache.py`

# Claude Agent Caching System

## Overview

The Claude Agent now includes an intelligent caching mechanism that reduces API costs and improves performance by caching repeated queries, code reviews, and documentation generation. This is especially beneficial for batch operations where the same files or queries might be processed multiple times.

## Features

- **Content-based Cache Keys**: Uses SHA-256 hashing of prompts and content to generate unique cache keys
- **TTL (Time-to-Live) Support**: Configurable expiration times for different operation types
- **LRU Eviction**: Automatic least-recently-used eviction when cache size limits are reached
- **Persistent Storage**: Optional disk-based caching that survives process restarts
- **Thread-Safe Operations**: Safe for concurrent access
- **Cache Statistics**: Track hit rates, misses, and cache performance
- **Operation-Specific Caching**: Different TTL strategies for queries, reviews, docs, and fixes

## Quick Start

### Basic Usage with Caching (Default)

```python
from claude_cli_agent import ClaudeAgent

# Caching is enabled by default
agent = ClaudeAgent(verbose=True)

# First call - makes API request and caches result
result = agent.query("What are Python best practices?")

# Second call - returns cached result (no API call)
result = agent.query("What are Python best practices?")

# View cache statistics
stats = agent.get_cache_stats()
print(stats)
# Output: {'size': 1, 'hits': 1, 'misses': 0, 'hit_rate': '100.00%', ...}
```

### Disabling Cache

```python
# Disable caching entirely
agent = ClaudeAgent(enable_cache=False)

# Or disable for specific operations
result = agent.query("prompt", use_cache=False)
```

### Custom Cache Configuration

```python
agent = ClaudeAgent(
    enable_cache=True,
    cache_dir="/custom/cache/path",  # Custom cache directory
    cache_max_size=5000,              # Max 5000 entries
    cache_ttl=7200                    # Default TTL: 2 hours
)
```

## Operation Types and Default TTLs

The caching system uses different Time-to-Live (TTL) values for different operation types:

| Operation Type | Default TTL | Duration | Use Case |
|---------------|-------------|----------|----------|
| `query` | 3600s | 1 hour | General queries |
| `code_review` | 86400s | 24 hours | Code reviews (stable) |
| `generate_docs` | 604800s | 7 days | Documentation (very stable) |
| `fix_code` | 300s | 5 minutes | Code fixes (may change quickly) |
| `batch_process` | 3600s | 1 hour | Batch operations |

### Customizing TTL per Operation

```python
# Override TTL for specific query
result = agent.query("prompt", cache_ttl=1800)  # 30 minutes

# Batch processing with custom cache
results = agent.batch_process(
    directory="./src",
    prompt="Analyze this code",
    use_cache=True  # Will cache each file's result
)
```

## Cache Management

### Viewing Cache Statistics

```python
stats = agent.get_cache_stats()
print(f"Cache size: {stats['size']}")
print(f"Hit rate: {stats['hit_rate']}")
print(f"Total requests: {stats['total_requests']}")
```

### Clearing Cache

```python
# Clear all cached entries
agent.clear_cache()
```

### Invalidating Specific Entries

```python
# Invalidate a specific cached query
agent.invalidate_cache(
    operation_type="query",
    prompt="What are Python best practices?"
)

# Invalidate a code review cache
agent.invalidate_cache(
    operation_type="code_review",
    file_path="/path/to/file.py"
)
```

## Batch Processing with Caching

Batch processing automatically uses caching to avoid re-processing the same files:

```python
agent = ClaudeAgent(verbose=True)

# First batch run - processes all files and caches results
results = agent.batch_process(
    directory="./src",
    prompt="Review this code for security issues",
    file_pattern="*.py"
)

# Second batch run - uses cached results for unchanged files
results = agent.batch_process(
    directory="./src",
    prompt="Review this code for security issues",
    file_pattern="*.py"
)

# Output shows cache statistics:
# ✓ Batch processing cache stats: 15 hits, 0 misses (100.0% hit rate)
```

## How Cache Keys Are Generated

Cache keys are generated using SHA-256 hashing of:

1. **Operation type** (query, code_review, generate_docs, etc.)
2. **Prompt text** (the actual prompt sent to Claude)
3. **Additional parameters** (file paths, system prompts, etc.)

This ensures that:
- Same inputs always produce the same cache key
- Different inputs always produce different cache keys
- Cache keys are consistent across sessions

Example:
```python
# These will use the SAME cache entry:
agent.query("Hello")
agent.query("Hello")

# These will use DIFFERENT cache entries:
agent.query("Hello")
agent.query("Hi")
agent.query("Hello", system_prompt="Be concise")
```

## Cache Storage

### In-Memory Cache

By default, cache entries are stored in memory for fast access.

### Disk-Based Persistence

Cache entries are also persisted to disk (enabled by default):

- **Location**: `~/.cache/claude-agent/` (customizable)
- **Format**: Pickled Python objects
- **Behavior**: Automatically loaded on startup, saved after each cache write

```python
# Custom cache directory
agent = ClaudeAgent(cache_dir="/custom/path")

# Disable disk caching (memory-only)
from claude_cache import ClaudeCache
cache = ClaudeCache(enable_disk_cache=False)
```

## Cache Eviction Policy

When the cache reaches its maximum size (`cache_max_size`):

1. The least recently used (LRU) entries are identified
2. Oldest 10% of entries are removed
3. Both memory and disk entries are cleaned up

```python
# Configure max cache size
agent = ClaudeAgent(cache_max_size=10000)  # Up to 10,000 entries
```

## Best Practices

### 1. Enable Caching for Batch Operations

```python
# DO: Use caching for batch processing
agent = ClaudeAgent(enable_cache=True)
results = agent.batch_process("./src", "Review code", use_cache=True)
```

### 2. Use Appropriate TTLs

```python
# DO: Use longer TTL for stable content
agent.generate_docs("stable_api.py", use_cache=True)  # Uses 7-day TTL

# DO: Use shorter TTL for frequently changing content
agent.fix_code("experimental.py", "Fix bug", use_cache=True)  # Uses 5-min TTL
```

### 3. Monitor Cache Performance

```python
# DO: Check cache statistics periodically
stats = agent.get_cache_stats()
if float(stats['hit_rate'].rstrip('%')) < 50:
    print("Low cache hit rate - consider adjusting TTL or cache size")
```

### 4. Clear Cache When Needed

```python
# DO: Clear cache after major code changes
agent.clear_cache()  # Start fresh

# DO: Invalidate specific entries when content changes
agent.invalidate_cache("code_review", file_path="updated_file.py")
```

### 5. Disable Caching for Streaming

```python
# Streaming output automatically bypasses cache
result = agent.query("prompt", stream_output=True)
```

## Performance Impact

### Cost Savings

Example: Reviewing 100 Python files with caching enabled

- **Without cache**: 100 API calls = 100% cost
- **With cache (50% hit rate)**: 50 API calls = 50% cost savings
- **With cache (90% hit rate)**: 10 API calls = 90% cost savings

### Speed Improvements

Cache hits are typically **1000x faster** than API calls:

- **API call**: ~1-5 seconds
- **Cache hit**: ~0.001-0.005 seconds

### Batch Processing Example

```python
import time

agent = ClaudeAgent(enable_cache=True, verbose=True)

# First run - no cache
start = time.time()
results = agent.batch_process("./src", "Review code", file_pattern="*.py")
first_run_time = time.time() - start
print(f"First run: {first_run_time:.2f}s")

# Second run - with cache
start = time.time()
results = agent.batch_process("./src", "Review code", file_pattern="*.py")
second_run_time = time.time() - start
print(f"Second run: {second_run_time:.2f}s")

speedup = first_run_time / second_run_time
print(f"Speedup: {speedup:.2f}x")

# Output example:
# First run: 45.23s
# Second run: 0.12s
# Speedup: 376.92x
```

## Thread Safety

The caching system is thread-safe and can be used with concurrent operations:

```python
from concurrent.futures import ThreadPoolExecutor

agent = ClaudeAgent(enable_cache=True)

def process_file(file_path):
    return agent.code_review(file_path)

with ThreadPoolExecutor(max_workers=10) as executor:
    files = ["file1.py", "file2.py", "file3.py"]
    results = list(executor.map(process_file, files))
```

## Troubleshooting

### Cache Not Working

1. **Check if caching is enabled**:
   ```python
   print(agent.enable_cache)  # Should be True
   print(agent.cache)  # Should not be None
   ```

2. **Verify cache hits**:
   ```python
   stats = agent.get_cache_stats()
   print(stats)
   ```

3. **Check disk permissions**:
   ```python
   print(agent.cache.cache_dir)  # Ensure directory is writable
   ```

### High Cache Misses

1. **Prompts may be slightly different** (whitespace, formatting)
2. **TTL may be too short** - increase `cache_ttl`
3. **Cache size may be too small** - increase `cache_max_size`

### Stale Cache Entries

1. **Clear cache manually**: `agent.clear_cache()`
2. **Invalidate specific entries**: `agent.invalidate_cache(...)`
3. **Reduce TTL** for frequently changing operations

## API Reference

### ClaudeAgent Methods

#### `__init__(..., enable_cache=True, cache_dir=None, cache_max_size=1000, cache_ttl=3600)`
Initialize agent with caching configuration.

#### `query(..., use_cache=True, cache_ttl=None)`
Send query with optional caching.

#### `code_review(file_path, use_cache=True)`
Review code with caching (24-hour default TTL).

#### `generate_docs(file_path, use_cache=True)`
Generate documentation with caching (7-day default TTL).

#### `fix_code(file_path, issue, use_cache=True)`
Fix code with caching (5-minute default TTL).

#### `batch_process(..., use_cache=True)`
Batch process files with caching.

#### `get_cache_stats()`
Get cache statistics dictionary.

#### `clear_cache()`
Clear all cached entries.

#### `invalidate_cache(operation_type, **kwargs)`
Invalidate specific cache entry.

### Cache Statistics

The `get_cache_stats()` method returns:

```python
{
    'size': 42,              # Number of cached entries
    'max_size': 1000,        # Maximum cache size
    'hits': 100,             # Number of cache hits
    'misses': 50,            # Number of cache misses
    'hit_rate': '66.67%',    # Cache hit rate percentage
    'total_requests': 150    # Total cache requests
}
```

## Examples

### Example 1: Document Generation Pipeline

```python
from claude_cli_agent import ClaudeAgent
from pathlib import Path

agent = ClaudeAgent(enable_cache=True, verbose=True)

# Generate docs for all Python files
docs_dir = Path("./docs/api")
docs_dir.mkdir(exist_ok=True)

for py_file in Path("./src").rglob("*.py"):
    # Uses cache - won't regenerate if file content unchanged
    result = agent.generate_docs(str(py_file))

    # Save documentation
    doc_file = docs_dir / f"{py_file.stem}.md"
    doc_file.write_text(result['result'])

print("Cache stats:", agent.get_cache_stats())
```

### Example 2: CI/CD Code Review

```python
import sys
from claude_cli_agent import ClaudeAgent

agent = ClaudeAgent(enable_cache=True)

# Get changed files from git
import subprocess
result = subprocess.run(
    ["git", "diff", "--name-only", "HEAD^", "HEAD"],
    capture_output=True,
    text=True
)
changed_files = result.stdout.strip().split('\n')

# Review only changed Python files
issues_found = False
for file in changed_files:
    if file.endswith('.py'):
        review = agent.code_review(file)

        if "CRITICAL" in review['result'] or "HIGH" in review['result']:
            print(f"❌ Issues found in {file}")
            print(review['result'])
            issues_found = True

if issues_found:
    sys.exit(1)  # Fail CI pipeline
```

### Example 3: Interactive Development

```python
from claude_cli_agent import ClaudeAgent

agent = ClaudeAgent(enable_cache=True, verbose=True)

# During development, run multiple times
# Cache ensures fast iteration

def analyze_project():
    results = agent.batch_process(
        directory="./src",
        prompt="Find potential bugs and suggest improvements",
        file_pattern="*.py"
    )

    for result in results:
        if not result['success']:
            print(f"Error in {result['file']}: {result['error']}")
        elif result.get('cached'):
            print(f"✓ {result['file']} (cached)")
        else:
            print(f"✓ {result['file']} (analyzed)")

# First run: analyzes all files
analyze_project()

# Subsequent runs: mostly cached results
analyze_project()

# Show performance improvement
stats = agent.get_cache_stats()
print(f"\nCache performance: {stats['hit_rate']} hit rate")
```

## Conclusion

The caching mechanism provides significant cost savings and performance improvements for Claude CLI Agent operations. By intelligently caching results based on content and operation type, you can:

- Reduce API costs by up to 90% for repeated operations
- Speed up batch processing by 100-1000x for cached results
- Improve development iteration speed
- Maintain consistency across multiple runs

Enable caching by default and adjust TTL values based on your specific use case for optimal performance.

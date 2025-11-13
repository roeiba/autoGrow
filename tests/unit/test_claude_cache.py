#!/usr/bin/env python3
"""
Unit tests for ClaudeCache system
Tests the intelligent caching mechanism for Claude CLI API calls
"""

import pytest
import time
import tempfile
import shutil
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "claude-agent"))

from claude_cache import ClaudeCache, CacheEntry, CacheConfig, get_cache


class TestCacheEntry:
    """Test CacheEntry class"""

    def test_cache_entry_creation(self):
        """Test creating a cache entry"""
        entry = CacheEntry("test_value", ttl=3600)
        assert entry.value == "test_value"
        assert entry.ttl == 3600
        assert entry.access_count == 0
        assert not entry.is_expired()

    def test_cache_entry_no_ttl(self):
        """Test cache entry without TTL (never expires)"""
        entry = CacheEntry("test_value", ttl=None)
        assert not entry.is_expired()

    def test_cache_entry_expiration(self):
        """Test cache entry expiration"""
        entry = CacheEntry("test_value", ttl=0.1)  # 100ms
        assert not entry.is_expired()
        time.sleep(0.2)
        assert entry.is_expired()

    def test_cache_entry_access(self):
        """Test cache entry access tracking"""
        entry = CacheEntry("test_value")
        assert entry.access_count == 0

        value = entry.access()
        assert value == "test_value"
        assert entry.access_count == 1

        entry.access()
        assert entry.access_count == 2

    def test_cache_entry_serialization(self):
        """Test cache entry serialization"""
        entry = CacheEntry("test_value", ttl=3600)
        entry.access()

        data = entry.to_dict()
        assert data['value'] == "test_value"
        assert data['ttl'] == 3600
        assert data['access_count'] == 1

        # Deserialize
        restored = CacheEntry.from_dict(data)
        assert restored.value == "test_value"
        assert restored.ttl == 3600
        assert restored.access_count == 1


class TestClaudeCache:
    """Test ClaudeCache class"""

    @pytest.fixture
    def temp_cache_dir(self):
        """Create a temporary cache directory"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def cache(self, temp_cache_dir):
        """Create a cache instance for testing"""
        return ClaudeCache(
            cache_dir=temp_cache_dir,
            max_size=100,
            default_ttl=3600,
            enable_disk_cache=True
        )

    def test_cache_initialization(self, temp_cache_dir):
        """Test cache initialization"""
        cache = ClaudeCache(cache_dir=temp_cache_dir)
        assert cache.max_size == 1000  # default
        assert cache.default_ttl == 3600  # default
        assert cache.enable_disk_cache is True
        assert cache.hits == 0
        assert cache.misses == 0

    def test_cache_key_generation(self, cache):
        """Test cache key generation"""
        key1 = cache._generate_key("test prompt", "query")
        key2 = cache._generate_key("test prompt", "query")
        key3 = cache._generate_key("different prompt", "query")

        # Same inputs produce same key
        assert key1 == key2

        # Different inputs produce different keys
        assert key1 != key3

    def test_cache_key_with_params(self, cache):
        """Test cache key generation with additional parameters"""
        key1 = cache._generate_key("prompt", "query", param1="value1")
        key2 = cache._generate_key("prompt", "query", param1="value1")
        key3 = cache._generate_key("prompt", "query", param1="value2")

        assert key1 == key2
        assert key1 != key3

    def test_cache_set_and_get(self, cache):
        """Test basic cache set and get operations"""
        key = cache._generate_key("test", "query")
        cache.set(key, {"result": "test_data"})

        result = cache.get(key)
        assert result == {"result": "test_data"}
        assert cache.hits == 1
        assert cache.misses == 0

    def test_cache_miss(self, cache):
        """Test cache miss"""
        result = cache.get("nonexistent_key")
        assert result is None
        assert cache.hits == 0
        assert cache.misses == 1

    def test_cache_expiration(self, cache):
        """Test cache entry expiration"""
        key = cache._generate_key("test", "query")
        cache.set(key, "test_data", ttl=0.1)  # 100ms TTL

        # Should be available immediately
        result = cache.get(key)
        assert result == "test_data"

        # Wait for expiration
        time.sleep(0.2)

        # Should be expired
        result = cache.get(key)
        assert result is None
        assert cache.misses == 1

    def test_cache_clear(self, cache):
        """Test cache clearing"""
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        assert len(cache._cache) == 2

        cache.clear()
        assert len(cache._cache) == 0
        assert cache.hits == 0
        assert cache.misses == 0

    def test_cache_invalidate(self, cache):
        """Test cache invalidation"""
        key = cache._generate_key("test", "query")
        cache.set(key, "test_data")

        # Should exist
        assert cache.get(key) == "test_data"

        # Invalidate
        result = cache.invalidate(key)
        assert result is True

        # Should no longer exist
        assert cache.get(key) is None

    def test_cache_invalidate_nonexistent(self, cache):
        """Test invalidating nonexistent key"""
        result = cache.invalidate("nonexistent_key")
        assert result is False

    def test_cache_stats(self, cache):
        """Test cache statistics"""
        cache.set("key1", "value1")
        cache.get("key1")  # hit
        cache.get("key2")  # miss

        stats = cache.get_stats()
        assert stats['size'] == 1
        assert stats['hits'] == 1
        assert stats['misses'] == 1
        assert stats['total_requests'] == 2
        assert '50.00%' in stats['hit_rate']

    def test_cache_lru_eviction(self, temp_cache_dir):
        """Test LRU eviction when cache is full"""
        cache = ClaudeCache(
            cache_dir=temp_cache_dir,
            max_size=10,
            enable_disk_cache=False
        )

        # Fill cache beyond max_size
        for i in range(15):
            cache.set(f"key{i}", f"value{i}")

        # Cache should be limited to max_size
        assert len(cache._cache) <= 10

    def test_cache_disk_persistence(self, temp_cache_dir):
        """Test disk persistence"""
        # Create cache and add entry
        cache1 = ClaudeCache(
            cache_dir=temp_cache_dir,
            enable_disk_cache=True
        )
        key = cache1._generate_key("test", "query")
        cache1.set(key, "persistent_data")

        # Create new cache instance (should load from disk)
        cache2 = ClaudeCache(
            cache_dir=temp_cache_dir,
            enable_disk_cache=True
        )

        result = cache2.get(key)
        assert result == "persistent_data"

    def test_cache_disabled_disk(self, temp_cache_dir):
        """Test cache with disk persistence disabled"""
        cache = ClaudeCache(
            cache_dir=temp_cache_dir,
            enable_disk_cache=False
        )

        key = cache._generate_key("test", "query")
        cache.set(key, "data")

        # Verify no cache files created
        cache_files = list(Path(temp_cache_dir).glob("*.cache"))
        assert len(cache_files) == 0

    def test_cached_call_function(self, cache):
        """Test cached_call wrapper"""
        call_count = 0

        def expensive_function():
            nonlocal call_count
            call_count += 1
            return "result"

        key = "test_key"

        # First call - function should execute
        result1 = cache.cached_call(expensive_function, key)
        assert result1 == "result"
        assert call_count == 1

        # Second call - should use cache
        result2 = cache.cached_call(expensive_function, key)
        assert result2 == "result"
        assert call_count == 1  # Function not called again

    def test_cached_call_force_refresh(self, cache):
        """Test cached_call with force refresh"""
        call_count = 0

        def function():
            nonlocal call_count
            call_count += 1
            return f"result_{call_count}"

        key = "test_key"

        result1 = cache.cached_call(function, key)
        assert result1 == "result_1"

        # Force refresh
        result2 = cache.cached_call(function, key, force_refresh=True)
        assert result2 == "result_2"
        assert call_count == 2


class TestCacheConfig:
    """Test CacheConfig class"""

    def test_ttl_constants(self):
        """Test TTL constant values"""
        assert CacheConfig.TTL_SHORT == 300
        assert CacheConfig.TTL_MEDIUM == 3600
        assert CacheConfig.TTL_LONG == 86400
        assert CacheConfig.TTL_WEEK == 604800

    def test_operation_ttls(self):
        """Test operation-specific TTLs"""
        assert CacheConfig.get_ttl("query") == CacheConfig.TTL_MEDIUM
        assert CacheConfig.get_ttl("code_review") == CacheConfig.TTL_LONG
        assert CacheConfig.get_ttl("generate_docs") == CacheConfig.TTL_WEEK
        assert CacheConfig.get_ttl("fix_code") == CacheConfig.TTL_SHORT
        assert CacheConfig.get_ttl("unknown") == CacheConfig.TTL_MEDIUM


class TestGlobalCache:
    """Test global cache singleton"""

    def test_get_cache_singleton(self, temp_cache_dir):
        """Test that get_cache returns singleton"""
        # Note: This test may affect other tests due to global state
        cache1 = get_cache(cache_dir=temp_cache_dir)
        cache2 = get_cache(cache_dir=temp_cache_dir)

        assert cache1 is cache2


class TestCacheIntegration:
    """Integration tests for caching system"""

    @pytest.fixture
    def temp_cache_dir(self):
        """Create a temporary cache directory"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_multiple_operations_caching(self, temp_cache_dir):
        """Test caching multiple different operations"""
        cache = ClaudeCache(cache_dir=temp_cache_dir)

        # Cache different operation types
        query_key = cache._generate_key("test query", "query")
        review_key = cache._generate_key("test code", "code_review")
        docs_key = cache._generate_key("test code", "generate_docs")

        cache.set(query_key, "query_result")
        cache.set(review_key, "review_result")
        cache.set(docs_key, "docs_result")

        # Verify all are cached independently
        assert cache.get(query_key) == "query_result"
        assert cache.get(review_key) == "review_result"
        assert cache.get(docs_key) == "docs_result"

    def test_cache_with_complex_data(self, temp_cache_dir):
        """Test caching complex data structures"""
        cache = ClaudeCache(cache_dir=temp_cache_dir)

        complex_data = {
            "result": "test",
            "metadata": {
                "tokens": 100,
                "model": "claude-3",
                "nested": {
                    "value": [1, 2, 3]
                }
            }
        }

        key = cache._generate_key("test", "query")
        cache.set(key, complex_data)

        retrieved = cache.get(key)
        assert retrieved == complex_data
        assert retrieved["metadata"]["nested"]["value"] == [1, 2, 3]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

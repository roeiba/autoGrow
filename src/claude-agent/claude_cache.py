#!/usr/bin/env python3
"""
Intelligent caching system for Claude CLI API calls
Reduces API costs and improves performance for repeated queries
"""

import hashlib
import json
import os
import pickle
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional, Callable
import threading


class CacheEntry:
    """Represents a single cache entry with metadata"""

    def __init__(self, value: Any, ttl: Optional[int] = None):
        """
        Initialize cache entry.

        Args:
            value: The cached value
            ttl: Time to live in seconds (None for no expiration)
        """
        self.value = value
        self.created_at = time.time()
        self.ttl = ttl
        self.access_count = 0
        self.last_accessed = self.created_at

    def is_expired(self) -> bool:
        """Check if the cache entry has expired"""
        if self.ttl is None:
            return False
        return time.time() - self.created_at > self.ttl

    def access(self) -> Any:
        """Record access and return value"""
        self.access_count += 1
        self.last_accessed = time.time()
        return self.value

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'value': self.value,
            'created_at': self.created_at,
            'ttl': self.ttl,
            'access_count': self.access_count,
            'last_accessed': self.last_accessed
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CacheEntry':
        """Deserialize from dictionary"""
        entry = cls(data['value'], data['ttl'])
        entry.created_at = data['created_at']
        entry.access_count = data['access_count']
        entry.last_accessed = data['last_accessed']
        return entry


class ClaudeCache:
    """
    Intelligent caching system for Claude API calls.

    Features:
    - Content-based cache keys using hashing
    - TTL (time-to-live) support
    - LRU eviction when cache size limits reached
    - Persistent storage with disk backing
    - Thread-safe operations
    - Cache statistics and monitoring
    """

    def __init__(
        self,
        cache_dir: Optional[str] = None,
        max_size: int = 1000,
        default_ttl: Optional[int] = 3600,
        enable_disk_cache: bool = True
    ):
        """
        Initialize the cache system.

        Args:
            cache_dir: Directory for persistent cache storage
            max_size: Maximum number of entries (LRU eviction when exceeded)
            default_ttl: Default time-to-live in seconds (None for no expiration)
            enable_disk_cache: Enable persistent disk storage
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.enable_disk_cache = enable_disk_cache

        # In-memory cache
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = threading.Lock()

        # Statistics
        self.hits = 0
        self.misses = 0

        # Setup cache directory
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path.home() / ".cache" / "claude-agent"

        if self.enable_disk_cache:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            self._load_from_disk()

    def _generate_key(
        self,
        prompt: str,
        operation_type: str = "query",
        **kwargs
    ) -> str:
        """
        Generate a unique cache key based on input parameters.

        Args:
            prompt: The prompt text
            operation_type: Type of operation (query, review, docs, etc.)
            **kwargs: Additional parameters that affect the result

        Returns:
            Cache key string
        """
        # Create a consistent representation of the input
        cache_data = {
            'operation': operation_type,
            'prompt': prompt,
            'params': sorted(kwargs.items())
        }

        # Serialize to JSON for consistent ordering
        cache_str = json.dumps(cache_data, sort_keys=True)

        # Generate hash
        return hashlib.sha256(cache_str.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        with self._lock:
            entry = self._cache.get(key)

            if entry is None:
                self.misses += 1
                return None

            if entry.is_expired():
                del self._cache[key]
                self.misses += 1
                return None

            self.hits += 1
            return entry.access()

    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> None:
        """
        Store value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses default_ttl if None)
        """
        with self._lock:
            if ttl is None:
                ttl = self.default_ttl

            entry = CacheEntry(value, ttl)
            self._cache[key] = entry

            # Check size and evict if necessary
            if len(self._cache) > self.max_size:
                self._evict_lru()

            # Persist to disk
            if self.enable_disk_cache:
                self._save_entry_to_disk(key, entry)

    def _evict_lru(self) -> None:
        """Evict least recently used entries"""
        # Sort by last accessed time
        sorted_entries = sorted(
            self._cache.items(),
            key=lambda x: x[1].last_accessed
        )

        # Remove oldest 10% of entries
        num_to_remove = max(1, len(self._cache) // 10)
        for key, _ in sorted_entries[:num_to_remove]:
            del self._cache[key]
            # Also remove from disk
            if self.enable_disk_cache:
                cache_file = self.cache_dir / f"{key}.cache"
                if cache_file.exists():
                    cache_file.unlink()

    def clear(self) -> None:
        """Clear all cache entries"""
        with self._lock:
            self._cache.clear()
            self.hits = 0
            self.misses = 0

            if self.enable_disk_cache:
                # Remove all cache files
                for cache_file in self.cache_dir.glob("*.cache"):
                    cache_file.unlink()

    def invalidate(self, key: str) -> bool:
        """
        Invalidate a specific cache entry.

        Args:
            key: Cache key to invalidate

        Returns:
            True if entry was removed, False if not found
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]

                if self.enable_disk_cache:
                    cache_file = self.cache_dir / f"{key}.cache"
                    if cache_file.exists():
                        cache_file.unlink()

                return True
            return False

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        with self._lock:
            total_requests = self.hits + self.misses
            hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0

            return {
                'size': len(self._cache),
                'max_size': self.max_size,
                'hits': self.hits,
                'misses': self.misses,
                'hit_rate': f"{hit_rate:.2f}%",
                'total_requests': total_requests
            }

    def _save_entry_to_disk(self, key: str, entry: CacheEntry) -> None:
        """Save cache entry to disk"""
        cache_file = self.cache_dir / f"{key}.cache"
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(entry.to_dict(), f)
        except Exception as e:
            # Silently fail - disk caching is optional
            pass

    def _load_from_disk(self) -> None:
        """Load cache entries from disk on initialization"""
        try:
            for cache_file in self.cache_dir.glob("*.cache"):
                try:
                    with open(cache_file, 'rb') as f:
                        data = pickle.load(f)
                        entry = CacheEntry.from_dict(data)

                        # Only load non-expired entries
                        if not entry.is_expired():
                            key = cache_file.stem
                            self._cache[key] = entry
                        else:
                            # Remove expired cache files
                            cache_file.unlink()
                except Exception:
                    # Skip corrupted cache files
                    cache_file.unlink()
        except Exception:
            # If loading fails, start with empty cache
            pass

    def cached_call(
        self,
        func: Callable,
        cache_key: str,
        ttl: Optional[int] = None,
        force_refresh: bool = False
    ) -> Any:
        """
        Wrapper for caching function calls.

        Args:
            func: Function to call if cache miss
            cache_key: Cache key for this call
            ttl: Time-to-live override
            force_refresh: Force cache refresh even if entry exists

        Returns:
            Function result (cached or fresh)
        """
        if not force_refresh:
            cached_value = self.get(cache_key)
            if cached_value is not None:
                return cached_value

        # Call function and cache result
        result = func()
        self.set(cache_key, result, ttl)
        return result


class CacheConfig:
    """Configuration for cache behavior"""

    # Cache TTL presets (in seconds)
    TTL_SHORT = 300      # 5 minutes - for rapidly changing data
    TTL_MEDIUM = 3600    # 1 hour - default for most queries
    TTL_LONG = 86400     # 24 hours - for stable data
    TTL_WEEK = 604800    # 7 days - for documentation/reviews

    # Operation-specific TTL defaults
    OPERATION_TTLS = {
        'query': TTL_MEDIUM,
        'code_review': TTL_LONG,
        'generate_docs': TTL_WEEK,
        'fix_code': TTL_SHORT,
        'batch_process': TTL_MEDIUM
    }

    @classmethod
    def get_ttl(cls, operation_type: str) -> int:
        """Get default TTL for operation type"""
        return cls.OPERATION_TTLS.get(operation_type, cls.TTL_MEDIUM)


# Singleton cache instance
_global_cache: Optional[ClaudeCache] = None


def get_cache(
    cache_dir: Optional[str] = None,
    max_size: int = 1000,
    default_ttl: Optional[int] = 3600,
    enable_disk_cache: bool = True
) -> ClaudeCache:
    """
    Get or create global cache instance.

    Args:
        cache_dir: Directory for persistent cache storage
        max_size: Maximum number of entries
        default_ttl: Default time-to-live in seconds
        enable_disk_cache: Enable persistent disk storage

    Returns:
        Global cache instance
    """
    global _global_cache

    if _global_cache is None:
        _global_cache = ClaudeCache(
            cache_dir=cache_dir,
            max_size=max_size,
            default_ttl=default_ttl,
            enable_disk_cache=enable_disk_cache
        )

    return _global_cache

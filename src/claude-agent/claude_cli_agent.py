#!/usr/bin/env python3
"""
Claude CLI Agent - Python wrapper for Claude Code CLI headless mode
Provides a Python interface to interact with Claude CLI in headless mode
"""

import json
import os
import subprocess
from typing import Dict, List, Optional, Any
from pathlib import Path

# Import caching system
try:
    from claude_cache import ClaudeCache, CacheConfig, get_cache
except ImportError:
    from .claude_cache import ClaudeCache, CacheConfig, get_cache


class ClaudeAgent:
    """
    Python wrapper for Claude Code CLI in headless mode.
    Enables programmatic access to Claude's capabilities.
    """
    
    def __init__(
        self,
        output_format: str = "json",
        verbose: bool = False,
        allowed_tools: Optional[List[str]] = None,
        disallowed_tools: Optional[List[str]] = None,
        permission_mode: Optional[str] = None,
        enable_cache: bool = True,
        cache_dir: Optional[str] = None,
        cache_max_size: int = 1000,
        cache_ttl: Optional[int] = 3600
    ):
        """
        Initialize the Claude CLI Agent.

        Args:
            output_format: Output format (text, json, stream-json)
            verbose: Enable verbose output
            allowed_tools: List of allowed tools
            disallowed_tools: List of disallowed tools
            permission_mode: Permission mode (acceptEdits, etc.)
            enable_cache: Enable intelligent caching to reduce API costs
            cache_dir: Custom cache directory (default: ~/.cache/claude-agent)
            cache_max_size: Maximum number of cache entries
            cache_ttl: Default cache TTL in seconds (None for no expiration)
        """
        self.output_format = output_format
        self.verbose = verbose
        self.allowed_tools = allowed_tools
        self.disallowed_tools = disallowed_tools
        self.permission_mode = permission_mode
        self.enable_cache = enable_cache

        # Initialize cache if enabled
        if self.enable_cache:
            self.cache = get_cache(
                cache_dir=cache_dir,
                max_size=cache_max_size,
                default_ttl=cache_ttl,
                enable_disk_cache=True
            )
        else:
            self.cache = None

        # Check if claude CLI is installed
        if not self._is_claude_installed():
            raise RuntimeError(
                "Claude Code CLI is not installed. Install it from:\n"
                "  https://code.claude.com/"
            )
    
    def _is_claude_installed(self) -> bool:
        """Check if claude CLI is installed."""
        try:
            subprocess.run(
                ["claude", "--version"],
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _build_command(
        self,
        prompt: str,
        additional_args: Optional[List[str]] = None
    ) -> List[str]:
        """
        Build the claude CLI command.
        
        Args:
            prompt: The prompt to send
            additional_args: Additional command line arguments
            
        Returns:
            List of command arguments
        """
        cmd = ["claude", "-p", prompt]
        
        # Add output format
        if self.output_format:
            cmd.extend(["--output-format", self.output_format])
        
        # Add verbose flag
        if self.verbose:
            cmd.append("--verbose")
        
        # Add allowed tools
        if self.allowed_tools:
            cmd.extend(["--allowedTools", ",".join(self.allowed_tools)])
        
        # Add disallowed tools
        if self.disallowed_tools:
            cmd.extend(["--disallowedTools", ",".join(self.disallowed_tools)])
        
        # Add permission mode
        if self.permission_mode:
            cmd.extend(["--permission-mode", self.permission_mode])
        
        # Add any additional arguments
        if additional_args:
            cmd.extend(additional_args)
        
        return cmd
    
    def query(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        mcp_config: Optional[str] = None,
        stream_output: bool = False,
        use_cache: bool = True,
        cache_ttl: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Send a query to Claude in headless mode.

        Args:
            prompt: The prompt to send
            system_prompt: Additional system prompt
            mcp_config: Path to MCP configuration file
            stream_output: If True, print output in real-time
            use_cache: Whether to use caching for this query
            cache_ttl: Override default cache TTL for this query

        Returns:
            Dict containing response and metadata
        """
        # Check cache if enabled
        if self.enable_cache and use_cache and self.cache and not stream_output:
            cache_key = self.cache._generate_key(
                prompt,
                operation_type="query",
                system_prompt=system_prompt,
                mcp_config=mcp_config
            )

            cached_result = self.cache.get(cache_key)
            if cached_result is not None:
                if self.verbose:
                    print("✓ Cache hit - returning cached result")
                return cached_result

        additional_args = []

        if system_prompt:
            additional_args.extend(["--append-system-prompt", system_prompt])

        if mcp_config:
            additional_args.extend(["--mcp-config", mcp_config])
        
        cmd = self._build_command(prompt, additional_args)
        
        try:
            if stream_output:
                # Stream output in real-time
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1
                )
                
                stdout_lines = []
                stderr_lines = []
                
                # Read stdout in real-time
                for line in process.stdout:
                    print(line, end='', flush=True)
                    stdout_lines.append(line)
                
                # Wait for completion and get stderr
                process.wait()
                stderr_output = process.stderr.read()
                
                stdout_text = ''.join(stdout_lines)
                
                # Handle stderr - distinguish between warnings and errors
                if stderr_output:
                    stderr_lower = stderr_output.lower()
                    is_warning_only = (
                        "warn:" in stderr_lower or 
                        "warning:" in stderr_lower
                    ) and stdout_text.strip()  # Has actual output
                    
                    if is_warning_only:
                        print(f"\n⚠️  Warning: {stderr_output.strip()}", flush=True)
                    else:
                        print(f"\n❌ Error: {stderr_output}", flush=True)
                        stderr_lines.append(stderr_output)
                
                # Only raise error if returncode is non-zero AND it's not just a warning
                if process.returncode != 0:
                    stderr_lower = stderr_output.lower() if stderr_output else ""
                    is_warning_only = (
                        "warn:" in stderr_lower or 
                        "warning:" in stderr_lower
                    ) and stdout_text.strip()
                    
                    if not is_warning_only:
                        raise RuntimeError(f"Claude CLI error: {stderr_output}")
                
                if self.output_format == "json":
                    result_data = json.loads(stdout_text)
                else:
                    result_data = {"result": stdout_text}

                # Note: Streaming results are not cached
                return result_data
            else:
                # Capture all output at once
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=False  # Don't raise on non-zero exit, we'll check manually
                )
                
                # Check if there's actual output despite warnings in stderr
                # Bun/AVX warnings shouldn't be treated as fatal errors
                if result.returncode != 0:
                    # Check if stderr contains only warnings (not actual errors)
                    stderr_lower = result.stderr.lower() if result.stderr else ""
                    is_warning_only = (
                        "warn:" in stderr_lower or 
                        "warning:" in stderr_lower
                    ) and result.stdout.strip()  # Has actual output
                    
                    if not is_warning_only:
                        # Provide more context in error message
                        error_msg = f"Claude CLI error (exit code {result.returncode})"
                        if result.stderr:
                            error_msg += f": {result.stderr}"
                        else:
                            error_msg += ": No error message provided"
                        if result.stdout:
                            error_msg += f"\nStdout: {result.stdout[:200]}"
                        raise RuntimeError(error_msg)
                    else:
                        # Log warning but continue
                        if self.verbose and result.stderr:
                            print(f"⚠️  Warning from Claude CLI: {result.stderr.strip()}", flush=True)
                
                # Check if we have any output
                if not result.stdout or not result.stdout.strip():
                    error_msg = "Claude CLI returned no output"
                    if result.stderr:
                        error_msg += f"\nStderr: {result.stderr}"
                    raise RuntimeError(error_msg)

                if self.output_format == "json":
                    result_data = json.loads(result.stdout)
                else:
                    result_data = {"result": result.stdout}

                # Cache the result if caching is enabled
                if self.enable_cache and use_cache and self.cache:
                    if cache_ttl is None:
                        cache_ttl = CacheConfig.get_ttl("query")

                    self.cache.set(cache_key, result_data, cache_ttl)
                    if self.verbose:
                        print("✓ Result cached for future use")

                return result_data

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Claude CLI error: {e.stderr}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse JSON response: {e}")
    
    def query_with_stdin(
        self,
        prompt: str,
        stdin_content: str,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a query with stdin input.
        
        Args:
            prompt: The prompt to send
            stdin_content: Content to send via stdin
            system_prompt: Additional system prompt
            
        Returns:
            Dict containing response and metadata
        """
        additional_args = []
        
        if system_prompt:
            additional_args.extend(["--append-system-prompt", system_prompt])
        
        cmd = self._build_command(prompt, additional_args)
        
        try:
            result = subprocess.run(
                cmd,
                input=stdin_content,
                capture_output=True,
                text=True,
                check=True
            )
            
            if self.output_format == "json":
                return json.loads(result.stdout)
            else:
                return {"result": result.stdout}
                
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Claude CLI error: {e.stderr}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse JSON response: {e}")
    
    def continue_conversation(
        self,
        prompt: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Continue a previous conversation.
        
        Args:
            prompt: The prompt to send
            session_id: Session ID to resume (None for most recent)
            
        Returns:
            Dict containing response and metadata
        """
        if session_id:
            cmd = ["claude", "--resume", session_id, prompt]
        else:
            cmd = ["claude", "--continue", prompt]
        
        # Add output format
        if self.output_format:
            cmd.extend(["--output-format", self.output_format])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if self.output_format == "json":
                return json.loads(result.stdout)
            else:
                return {"result": result.stdout}
                
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Claude CLI error: {e.stderr}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse JSON response: {e}")
    
    def code_review(
        self,
        file_path: str,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Perform a code review on a file.

        Args:
            file_path: Path to the file to review
            use_cache: Whether to use caching for this review

        Returns:
            Dict containing review results
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r') as f:
            file_content = f.read()

        # Check cache if enabled
        if self.enable_cache and use_cache and self.cache:
            cache_key = self.cache._generate_key(
                file_content,
                operation_type="code_review",
                file_path=file_path
            )

            cached_result = self.cache.get(cache_key)
            if cached_result is not None:
                if self.verbose:
                    print(f"✓ Cache hit for code review: {file_path}")
                return cached_result

        prompt = f"""Review this code for:
        1. Security vulnerabilities
        2. Performance issues
        3. Code quality and best practices
        4. Potential bugs
        5. Suggestions for improvement

        File: {file_path}

        Provide a structured analysis with severity levels."""

        result = self.query_with_stdin(prompt, file_content)

        # Cache the result
        if self.enable_cache and use_cache and self.cache:
            cache_ttl = CacheConfig.get_ttl("code_review")
            self.cache.set(cache_key, result, cache_ttl)
            if self.verbose:
                print("✓ Code review cached for future use")

        return result
    
    def generate_docs(
        self,
        file_path: str,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Generate documentation for a file.

        Args:
            file_path: Path to the file to document
            use_cache: Whether to use caching for this documentation

        Returns:
            Dict containing generated documentation
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r') as f:
            file_content = f.read()

        # Check cache if enabled
        if self.enable_cache and use_cache and self.cache:
            cache_key = self.cache._generate_key(
                file_content,
                operation_type="generate_docs",
                file_path=file_path
            )

            cached_result = self.cache.get(cache_key)
            if cached_result is not None:
                if self.verbose:
                    print(f"✓ Cache hit for documentation: {file_path}")
                return cached_result

        prompt = f"""Generate comprehensive documentation for this code including:
        1. Overview and purpose
        2. Function/class descriptions
        3. Parameters and return values
        4. Usage examples
        5. Dependencies

        File: {file_path}

        Format as Markdown."""

        result = self.query_with_stdin(prompt, file_content)

        # Cache the result with longer TTL for documentation
        if self.enable_cache and use_cache and self.cache:
            cache_ttl = CacheConfig.get_ttl("generate_docs")
            self.cache.set(cache_key, result, cache_ttl)
            if self.verbose:
                print("✓ Documentation cached for future use")

        return result
    
    def fix_code(
        self,
        file_path: str,
        issue_description: str,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Fix code issues.

        Args:
            file_path: Path to the file to fix
            issue_description: Description of the issue to fix
            use_cache: Whether to use caching for this fix

        Returns:
            Dict containing fix results
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r') as f:
            file_content = f.read()

        # Check cache if enabled
        if self.enable_cache and use_cache and self.cache:
            cache_key = self.cache._generate_key(
                file_content,
                operation_type="fix_code",
                file_path=file_path,
                issue=issue_description
            )

            cached_result = self.cache.get(cache_key)
            if cached_result is not None:
                if self.verbose:
                    print(f"✓ Cache hit for code fix: {file_path}")
                return cached_result

        prompt = f"""Fix the following issue in this code:

        Issue: {issue_description}

        File: {file_path}

        Provide the fixed code and explanation of changes."""

        result = self.query_with_stdin(prompt, file_content)

        # Cache the result with shorter TTL for fixes
        if self.enable_cache and use_cache and self.cache:
            cache_ttl = CacheConfig.get_ttl("fix_code")
            self.cache.set(cache_key, result, cache_ttl)
            if self.verbose:
                print("✓ Code fix cached for future use")

        return result
    
    def batch_process(
        self,
        directory: str,
        prompt: str,
        file_pattern: str = "*.py",
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Process multiple files in a directory with intelligent caching.

        Args:
            directory: Directory to process
            prompt: Prompt to apply to each file
            file_pattern: Glob pattern for files to process
            use_cache: Whether to use caching for batch operations

        Returns:
            List of results for each file
        """
        results = []
        path = Path(directory)
        cache_hits = 0
        cache_misses = 0

        for file_path in path.rglob(file_pattern):
            if file_path.is_file():
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()

                    # Check cache if enabled
                    cache_hit = False
                    if self.enable_cache and use_cache and self.cache:
                        cache_key = self.cache._generate_key(
                            content,
                            operation_type="batch_process",
                            prompt=prompt,
                            file_path=str(file_path)
                        )

                        cached_result = self.cache.get(cache_key)
                        if cached_result is not None:
                            results.append({
                                "file": str(file_path),
                                "result": cached_result,
                                "success": True,
                                "cached": True
                            })
                            cache_hit = True
                            cache_hits += 1

                    if not cache_hit:
                        result = self.query_with_stdin(
                            f"{prompt}\n\nFile: {file_path}",
                            content
                        )

                        # Cache the result
                        if self.enable_cache and use_cache and self.cache:
                            cache_ttl = CacheConfig.get_ttl("batch_process")
                            self.cache.set(cache_key, result, cache_ttl)
                            cache_misses += 1

                        results.append({
                            "file": str(file_path),
                            "result": result,
                            "success": True,
                            "cached": False
                        })
                except Exception as e:
                    results.append({
                        "file": str(file_path),
                        "error": str(e),
                        "success": False,
                        "cached": False
                    })

        if self.verbose and self.enable_cache and use_cache:
            total = cache_hits + cache_misses
            if total > 0:
                hit_rate = (cache_hits / total) * 100
                print(f"\n✓ Batch processing cache stats: {cache_hits} hits, {cache_misses} misses ({hit_rate:.1f}% hit rate)")

        return results

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics or None if caching disabled
        """
        if self.cache:
            return self.cache.get_stats()
        return {"caching_enabled": False}

    def clear_cache(self) -> None:
        """Clear all cached entries."""
        if self.cache:
            self.cache.clear()
            if self.verbose:
                print("✓ Cache cleared")

    def invalidate_cache(self, operation_type: str, **kwargs) -> bool:
        """
        Invalidate specific cache entries.

        Args:
            operation_type: Type of operation to invalidate
            **kwargs: Additional parameters to identify cache entry

        Returns:
            True if entry was invalidated, False otherwise
        """
        if self.cache:
            # Generate the same key that was used for caching
            cache_key = self.cache._generate_key(
                kwargs.get('prompt', ''),
                operation_type=operation_type,
                **kwargs
            )
            return self.cache.invalidate(cache_key)
        return False


def main():
    """Example usage of ClaudeAgent with caching."""
    import sys

    try:
        # Initialize agent with caching enabled (default)
        agent = ClaudeAgent(verbose=True)

        print("🤖 Claude CLI Agent - Python Interface with Intelligent Caching")
        print("=" * 70)

        # Example 1: Simple query
        print("\n1. Simple Query (first call - will be cached):")
        result = agent.query("What are the best practices for Python error handling?")
        if "result" in result:
            print(result["result"])
        else:
            print(json.dumps(result, indent=2))

        # Example 2: Same query (should hit cache)
        print("\n2. Same Query (should hit cache):")
        result = agent.query("What are the best practices for Python error handling?")
        if "result" in result:
            print(result["result"][:100] + "..." if len(result["result"]) > 100 else result["result"])

        # Example 3: Code review (if file provided)
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            print(f"\n3. Code Review: {file_path}")
            result = agent.code_review(file_path)
            if "result" in result:
                print(result["result"])
            else:
                print(json.dumps(result, indent=2))

        # Example 4: Show cache statistics
        print("\n4. Cache Statistics:")
        stats = agent.get_cache_stats()
        print(json.dumps(stats, indent=2))

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

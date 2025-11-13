#!/usr/bin/env python3
"""
Issue Generator Agent - Core Logic

Ensures minimum number of open issues by generating new ones with Claude AI using Agent SDK
"""

import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Optional
from collections import defaultdict

# Add src directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent / "claude-agent"))
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import model configuration
from models_config import CLAUDE_MODELS, SystemPrompts

# Import Claude CLI Agent or fallback to Anthropic SDK
try:
    from claude_cli_agent import ClaudeAgent

    USE_CLAUDE_CLI = True
except ImportError:
    USE_CLAUDE_CLI = False
    try:
        from anthropic import Anthropic
    except ImportError:
        print("❌ Neither claude_cli_agent nor anthropic SDK available")
        raise


class IssueGenerator:
    """Generates GitHub issues using AI based on repository context"""

    def __init__(
        self, repo, anthropic_api_key: Optional[str] = None, min_issues: int = 3
    ):
        """
        Initialize the Issue Generator

        Args:
            repo: PyGithub Repository object
            anthropic_api_key: Anthropic API key (required if not using Claude CLI)
            min_issues: Minimum number of open issues to maintain
        """
        self.repo = repo
        self.anthropic_api_key = anthropic_api_key
        self.min_issues = min_issues

    def check_and_generate(self) -> bool:
        """
        Check issue count and generate if needed

        Returns:
            bool: True if issues were generated, False otherwise
        """
        print(f"🔍 Checking issue count (minimum: {self.min_issues})")

        # Count open issues (excluding pull requests)
        open_issues = list(self.repo.get_issues(state="open"))
        open_issues = [i for i in open_issues if not i.pull_request]
        issue_count = len(open_issues)

        print(f"📊 Current open issues: {issue_count}")

        if issue_count >= self.min_issues:
            print(f"✅ Sufficient issues exist ({issue_count} >= {self.min_issues})")
            return False

        # Need to generate issues
        needed = self.min_issues - issue_count
        print(f"🤖 Generating {needed} new issue(s)...")

        self._generate_issues(needed, open_issues)
        return True

    def _generate_issues(self, needed: int, open_issues: List) -> None:
        """
        Generate issues using Claude AI

        Args:
            needed: Number of issues to generate
            open_issues: List of current open issues
        """
        # Get repository context
        print("📖 Analyzing repository for potential issues...")

        try:
            readme = self.repo.get_readme().decoded_content.decode("utf-8")[:1000]
        except:
            readme = "No README found"

        recent_commits = list(self.repo.get_commits()[:5])
        commit_messages = "\n".join(
            [f"- {c.commit.message.split(chr(10))[0]}" for c in recent_commits]
        )

        # Get enhanced context analysis
        print("🔍 Analyzing project structure...")
        directory_structure = self._analyze_directory_structure()

        print("📊 Analyzing file types...")
        file_types = self._analyze_file_types()

        print("🔬 Analyzing code patterns...")
        code_patterns = self._analyze_code_patterns()

        # Build prompt for Claude
        prompt = self._build_prompt(
            needed, readme, commit_messages, open_issues,
            directory_structure, file_types, code_patterns
        )

        print(f"📝 Prompt length: {len(prompt)} chars")

        # Call Claude AI
        response_text = self._call_claude(prompt)

        if not response_text:
            print("❌ Failed to get response from Claude")
            sys.exit(1)

        # Parse and create issues
        self._parse_and_create_issues(response_text, needed)

    def _analyze_directory_structure(self) -> str:
        """Analyze and summarize the repository directory structure"""
        try:
            # Get repository contents recursively (up to 2 levels deep)
            contents = []

            def get_tree(path="", level=0, max_level=2):
                if level > max_level:
                    return
                try:
                    items = self.repo.get_contents(path)
                    if not isinstance(items, list):
                        items = [items]

                    for item in items:
                        indent = "  " * level
                        if item.type == "dir":
                            contents.append(f"{indent}{item.name}/")
                            get_tree(item.path, level + 1, max_level)
                        elif level < 2:  # Only show files at top levels
                            contents.append(f"{indent}{item.name}")
                except Exception as e:
                    pass

            get_tree()

            if not contents:
                return "Unable to analyze directory structure"

            # Limit to first 50 entries to avoid huge output
            structure = "\n".join(contents[:50])
            if len(contents) > 50:
                structure += f"\n... and {len(contents) - 50} more items"

            return structure
        except Exception as e:
            return f"Error analyzing directory structure: {str(e)}"

    def _analyze_file_types(self) -> str:
        """Analyze file types and technologies used in the repository"""
        try:
            file_types = defaultdict(int)
            total_files = 0

            # Get all files from repository (limited scan)
            contents = self.repo.get_contents("")
            to_process = list(contents) if isinstance(contents, list) else [contents]
            processed = 0
            max_files = 200  # Limit to avoid API rate limits

            while to_process and processed < max_files:
                item = to_process.pop(0)
                processed += 1

                if item.type == "dir":
                    try:
                        dir_contents = self.repo.get_contents(item.path)
                        if isinstance(dir_contents, list):
                            to_process.extend(dir_contents)
                    except:
                        pass
                elif item.type == "file":
                    total_files += 1
                    # Get file extension
                    ext = Path(item.name).suffix.lower()
                    if ext:
                        file_types[ext] += 1
                    else:
                        # Check for common config files without extensions
                        if item.name.lower() in ['dockerfile', 'makefile', 'readme']:
                            file_types[f"[{item.name}]"] += 1

            if not file_types:
                return "No files analyzed"

            # Sort by count and format
            sorted_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)
            analysis = [f"Total files scanned: {total_files}"]
            analysis.append("File types:")
            for ext, count in sorted_types[:15]:  # Top 15 file types
                percentage = (count / total_files * 100) if total_files > 0 else 0
                analysis.append(f"  {ext}: {count} ({percentage:.1f}%)")

            return "\n".join(analysis)
        except Exception as e:
            return f"Error analyzing file types: {str(e)}"

    def _analyze_code_patterns(self) -> str:
        """Analyze code patterns and project characteristics"""
        try:
            patterns = []

            # Check for common project files and patterns
            checks = {
                "Python project": ["setup.py", "requirements.txt", "pyproject.toml"],
                "Node.js project": ["package.json", "package-lock.json"],
                "Docker support": ["Dockerfile", "docker-compose.yml"],
                "CI/CD": [".github/workflows", ".gitlab-ci.yml", "Jenkinsfile"],
                "Testing": ["tests/", "test/", "pytest.ini", "jest.config.js"],
                "Documentation": ["docs/", "README.md", "CONTRIBUTING.md"],
                "Infrastructure as Code": ["terraform/", "k8s/", "kubernetes/"],
            }

            for pattern_name, files in checks.items():
                for file_path in files:
                    try:
                        self.repo.get_contents(file_path)
                        patterns.append(f"✓ {pattern_name}")
                        break  # Found one, move to next pattern
                    except:
                        continue

            # Check for specific technologies by examining package files
            try:
                package_json = self.repo.get_contents("package.json")
                if package_json:
                    content = package_json.decoded_content.decode("utf-8")
                    if "react" in content.lower():
                        patterns.append("✓ React framework detected")
                    if "express" in content.lower():
                        patterns.append("✓ Express.js detected")
                    if "typescript" in content.lower():
                        patterns.append("✓ TypeScript project")
            except:
                pass

            try:
                requirements = self.repo.get_contents("requirements.txt")
                if requirements:
                    content = requirements.decoded_content.decode("utf-8")
                    if "django" in content.lower():
                        patterns.append("✓ Django framework detected")
                    if "flask" in content.lower():
                        patterns.append("✓ Flask framework detected")
                    if "fastapi" in content.lower():
                        patterns.append("✓ FastAPI framework detected")
            except:
                pass

            if not patterns:
                return "No specific patterns detected"

            return "Project characteristics:\n" + "\n".join(patterns)
        except Exception as e:
            return f"Error analyzing code patterns: {str(e)}"

    def _build_prompt(
        self, needed: int, readme: str, commit_messages: str, open_issues: List,
        directory_structure: str, file_types: str, code_patterns: str
    ) -> str:
        """Build the prompt for Claude"""
        return f"""Analyze this GitHub repository and suggest {needed} new issue(s).

Repository: {self.repo.full_name}

README excerpt:
{readme}

Recent commits:
{commit_messages}

Current open issues:
{chr(10).join([f"- #{i.number}: {i.title}" for i in open_issues[:10]])}

PROJECT STRUCTURE:
{directory_structure}

FILE TYPES ANALYSIS:
{file_types}

CODE PATTERNS & TECHNOLOGIES:
{code_patterns}

Based on this comprehensive analysis, generate {needed} realistic, actionable issue(s).
Consider the project's technology stack, existing patterns, directory organization, and current development trajectory.
Focus on meaningful improvements that align with the project's architecture and goals.

Respond with ONLY a JSON object in this exact format:
{{
  "issues": [
    {{
      "title": "Brief title (max 80 chars)",
      "body": "Description (max 300 chars)",
      "labels": ["feature"]
    }}
  ]
}}

Use appropriate labels: feature, bug, documentation, refactor, test, performance, security, ci/cd

Keep descriptions brief and output ONLY the JSON, nothing else."""

    def _call_claude(self, prompt: str) -> Optional[str]:
        """Call Claude AI (CLI or API)"""
        try:
            if USE_CLAUDE_CLI:
                print("🤖 Using Claude CLI...")
                agent = ClaudeAgent(output_format="text", verbose=True)

                result = agent.query(
                    prompt, system_prompt=SystemPrompts.ISSUE_GENERATOR
                )

                # Extract response
                if isinstance(result, dict) and "result" in result:
                    return result["result"]
                else:
                    return str(result)
            else:
                print("🤖 Using Anthropic API...")
                client = Anthropic(api_key=self.anthropic_api_key)

                message = client.messages.create(
                    model=CLAUDE_MODELS.ISSUE_GENERATION,
                    max_tokens=CLAUDE_MODELS.DEFAULT_MAX_TOKENS,
                    system=SystemPrompts.ISSUE_GENERATOR,
                    messages=[{"role": "user", "content": prompt}],
                )

                return message.content[0].text

        except Exception as e:
            print(f"❌ Error calling Claude: {e}")
            import traceback

            traceback.print_exc()
            return None

    def _parse_and_create_issues(self, response_text: str, needed: int) -> None:
        """Parse Claude response and create GitHub issues"""
        try:
            print("🔍 Parsing Claude response...")

            # Clean up response - remove markdown code blocks if present
            cleaned_response = response_text.strip()
            if "```json" in cleaned_response:
                cleaned_response = (
                    cleaned_response.split("```json")[1].split("```")[0].strip()
                )
                print("📝 Removed ```json``` markers")
            elif "```" in cleaned_response:
                cleaned_response = (
                    cleaned_response.split("```")[1].split("```")[0].strip()
                )
                print("📝 Removed ``` markers")

            # Find JSON object in response
            start_idx = cleaned_response.find("{")
            end_idx = cleaned_response.rfind("}") + 1

            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON object found in response")

            json_str = cleaned_response[start_idx:end_idx]
            print(f"📊 Extracted JSON: {len(json_str)} chars")

            data = json.loads(json_str)
            issues_to_create = data.get("issues", [])[:needed]

            if not issues_to_create:
                print("⚠️  No issues generated by Claude")
                return

            # Create issues
            for issue_data in issues_to_create:
                title = issue_data.get("title", "Untitled Issue")[
                    :80
                ]  # Limit title length
                body = issue_data.get("body", "")
                labels = issue_data.get("labels", [])

                full_body = f"{body}\n\n---\n*Generated by Issue Generator Agent*"

                new_issue = self.repo.create_issue(
                    title=title, body=full_body, labels=labels
                )

                print(f"✅ Created issue #{new_issue.number}: {title}")

            print(f"🎉 Successfully generated {len(issues_to_create)} issue(s)")

        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse Claude response as JSON: {e}")
            print(f"Response (first 1000 chars): {response_text[:1000]}")
            print(f"Response (last 500 chars): {response_text[-500:]}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error creating issues: {e}")
            import traceback

            traceback.print_exc()
            sys.exit(1)

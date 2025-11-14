#!/usr/bin/env python3
"""
Issue Resolver Agent - Core Logic

Takes an open issue, analyzes it with Claude AI using Agent SDK, implements a fix, and creates a PR
"""

import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Tuple
import git

# Add src directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent / "claude-agent"))
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import Claude CLI Agent
try:
    from claude_cli_agent import ClaudeAgent

    USE_CLAUDE_CLI = True
except ImportError:
    print("⚠️  claude_cli_agent not available, falling back to anthropic SDK")
    from anthropic import Anthropic

    USE_CLAUDE_CLI = False

# Import validator and retry utilities
from utils.project_brief_validator import validate_project_brief
from utils.retry import retry_github_api
from utils.outcome_tracker import OutcomeTracker, ResolutionStatus


class IssueResolver:
    """Resolves GitHub issues using AI and creates pull requests"""

    def __init__(
        self,
        repo,
        git_repo,
        anthropic_api_key: Optional[str] = None,
        labels_to_handle: Optional[List[str]] = None,
        labels_to_skip: Optional[List[str]] = None,
        max_time: int = 480,
        dry_mode: bool = False,
    ):
        """
        Initialize the Issue Resolver

        Args:
            repo: PyGithub Repository object
            git_repo: GitPython Repo object
            anthropic_api_key: Anthropic API key (required if not using Claude CLI)
            labels_to_handle: List of labels to handle (default: bug, enhancement)
            labels_to_skip: List of labels to skip (default: wontfix, duplicate, in-progress)
            max_time: Maximum execution time in seconds
            dry_mode: If True, skip all GitHub write operations (for CI validation)
        """
        self.repo = repo
        self.git_repo = git_repo
        self.anthropic_api_key = anthropic_api_key
        self.labels_to_handle = labels_to_handle or ["bug", "enhancement"]
        self.labels_to_skip = labels_to_skip or ["wontfix", "duplicate", "in-progress"]
        self.max_time = max_time
        self.dry_mode = dry_mode
        self.start_time = time.time()

        # Initialize outcome tracker for feedback loop
        self.outcome_tracker = OutcomeTracker()

        print("🤖 Issue Resolver Agent Initialized")
        print(f"📋 Config:")
        print(f"   - Labels to handle: {self.labels_to_handle}")
        print(f"   - Labels to skip: {self.labels_to_skip}")
        print(f"   - Dry mode: {self.dry_mode}")
        print(f"   - Outcome tracking: enabled")
        print(
            f"   - Supports: features, bugs, documentation, refactoring, tests, performance, security, CI/CD"
        )

    def resolve_issue(self, specific_issue: Optional[int] = None) -> bool:
        """
        Resolve an issue and create a PR

        Args:
            specific_issue: Specific issue number to resolve (optional)

        Returns:
            bool: True if issue was resolved, False otherwise
        """
        print("\n" + "="*80)
        print("🚀 STARTING ISSUE RESOLUTION WORKFLOW")
        print("="*80)
        
        # Select issue
        selected_issue = self._select_issue(specific_issue)

        if not selected_issue:
            print("\n❌ WORKFLOW ABORTED: No suitable issues found")
            print("="*80 + "\n")
            return False

        print(f"\n✅ ISSUE SELECTED")
        print(f"   Issue: #{selected_issue.number}")
        print(f"   Title: {selected_issue.title}")
        print(f"   Labels: {[label.name for label in selected_issue.labels]}")
        print(f"   Created: {selected_issue.created_at}")

        # Record attempt in outcome tracker
        issue_labels = [label.name for label in selected_issue.labels]
        if not self.dry_mode:
            self.outcome_tracker.record_attempt(
                issue_number=selected_issue.number,
                issue_title=selected_issue.title,
                labels=issue_labels,
                status=ResolutionStatus.PENDING
            )
            print(f"   📊 Outcome tracking: Recorded attempt")

        # Claim the issue
        issue_claimed = self._claim_issue(selected_issue)

        # Get issue details for validation check
        issue_body = selected_issue.body or "No description provided"
        issue_labels = [label.name for label in selected_issue.labels]

        # Validate PROJECT_BRIEF.md before proceeding
        is_valid, validation_msg = self._validate_project_brief_if_exists(
            issue_title=selected_issue.title,
            issue_body=issue_body,
            issue_labels=issue_labels,
        )

        if not is_valid:
            print("❌ PROJECT_BRIEF.md validation failed - aborting to save API calls")
            if not self.dry_mode:
                selected_issue.create_comment(
                    f"❌ **Pre-flight check failed**\n\n{validation_msg}\n\n"
                    "Please fix PROJECT_BRIEF.md validation errors before I can proceed.\n\n"
                    "---\n*Issue Resolver Agent*"
                )
            else:
                print("   🔍 DRY MODE: Would post validation failure comment")
            return False

        # Add validation success to issue comment if there was a validation
        if validation_msg:
            if not self.dry_mode:
                selected_issue.create_comment(validation_msg)
            else:
                print("   🔍 DRY MODE: Would post validation success comment")

        # Create branch
        branch_name = f"fix/issue-{selected_issue.number}-{int(time.time())}"
        if not self._create_branch(branch_name, selected_issue, issue_claimed):
            return False

        # Generate fix using Claude
        summary = self._generate_fix(selected_issue, issue_body, issue_labels)

        if summary is None:
            if issue_claimed and not self.dry_mode:
                selected_issue.create_comment("❌ Failed to generate fix")
                # Track failure
                self.outcome_tracker.update_status(
                    issue_number=selected_issue.number,
                    status=ResolutionStatus.FAILED,
                    error_message="Failed to generate fix with Claude AI"
                )
                print("   📊 Outcome tracking: Marked as FAILED")
            elif issue_claimed:
                print("   🔍 DRY MODE: Would post fix generation failure comment")
            return False

        # Check if files were modified and create PR
        return self._create_pr_if_changes(selected_issue, branch_name, summary)

    def _select_issue(self, specific_issue: Optional[int]) -> Optional[object]:
        """Select an issue to work on"""
        print("\n" + "-"*80)
        print("📋 STEP 1: ISSUE SELECTION")
        print("-"*80)

        if specific_issue:
            print(f"🎯 Mode: Specific issue requested")
            print(f"   Issue number: #{specific_issue}")

            @retry_github_api
            def get_issue():
                return self.repo.get_issue(int(specific_issue))

            issue = get_issue()
            print(f"   ✅ Found issue: {issue.title}")
            return issue

        print(f"🔍 Mode: Searching for suitable issue")
        print(f"   Criteria:")
        print(f"   - State: open")
        print(f"   - Must have labels: {self.labels_to_handle}")
        print(f"   - Must NOT have labels: {self.labels_to_skip}")
        print(f"   - Not already claimed by agent")

        @retry_github_api
        def get_open_issues():
            return self.repo.get_issues(
                state="open", sort="created", direction="asc"
            )

        open_issues = get_open_issues()

        issues_checked = 0
        for issue in open_issues:
            issues_checked += 1
            
            if issue.pull_request:
                print(f"   ⏭️  Skipping #{issue.number}: Is a pull request")
                continue

            issue_labels = [label.name for label in issue.labels]
            
            if any(skip_label in issue_labels for skip_label in self.labels_to_skip):
                skip_label_found = [l for l in issue_labels if l in self.labels_to_skip]
                print(f"   ⏭️  Skipping #{issue.number}: Has skip label {skip_label_found}")
                continue

            if self.labels_to_handle and not any(
                handle_label in issue_labels for handle_label in self.labels_to_handle
            ):
                print(f"   ⏭️  Skipping #{issue.number}: No matching labels (has: {issue_labels})")
                continue

            comments = list(issue.get_comments())
            if any(
                "Issue Resolver Agent" in c.body and "claimed" in c.body.lower()
                for c in comments
            ):
                print(f"   ⏭️  Skipping #{issue.number}: Already claimed by agent")
                continue

            print(f"\n   ✅ SELECTED: Issue #{issue.number}")
            print(f"      Title: {issue.title}")
            print(f"      Labels: {issue_labels}")
            print(f"      Reason: Matches all criteria")
            print(f"      (Checked {issues_checked} issues total)")
            return issue

        print(f"\n   ❌ No suitable issues found (checked {issues_checked} issues)")
        return None

    def _claim_issue(self, issue) -> bool:
        """Claim an issue by adding a comment and label"""
        print("\n" + "-"*80)
        print("📋 STEP 2: CLAIMING ISSUE")
        print("-"*80)

        claim_message = f"""🤖 **Issue Resolver Agent**

I'm working on this issue now.

**Started at:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}
**Status:** In Progress

---
*Automated by GitHub Actions*"""

        if self.dry_mode:
            print("   🔍 DRY MODE: Would add 'in-progress' label")
            print("   🔍 DRY MODE: Would post claim comment to issue")
            return True

        @retry_github_api
        def create_comment():
            return issue.create_comment(claim_message)

        @retry_github_api
        def add_label():
            return issue.add_to_labels("in-progress")

        create_comment()
        add_label()
        print("   ✅ Added 'in-progress' label")
        print("   ✅ Posted claim comment to issue")
        return True

    def _should_skip_validation(
        self, issue_title: str, issue_body: str, issue_labels: List[str]
    ) -> bool:
        """Determine if PROJECT_BRIEF.md validation should be skipped"""
        skip_keywords = [
            "project_brief",
            "project brief",
            "template",
            "example",
            "documentation",
            "readme",
            "setup",
            "initial",
            "bootstrap",
        ]

        text_to_check = f"{issue_title} {issue_body}".lower()
        if any(keyword in text_to_check for keyword in skip_keywords):
            return True

        skip_labels = ["documentation", "setup", "template"]
        if any(label in skip_labels for label in issue_labels):
            return True

        return False

    def _validate_project_brief_if_exists(
        self,
        issue_title: str = "",
        issue_body: str = "",
        issue_labels: Optional[List[str]] = None,
    ) -> Tuple[bool, Optional[str]]:
        """Validate PROJECT_BRIEF.md if it exists"""
        print("\n" + "-"*80)
        print("📋 STEP 3: PROJECT BRIEF VALIDATION")
        print("-"*80)
        
        issue_labels = issue_labels or []

        if self._should_skip_validation(issue_title, issue_body, issue_labels):
            print(
                "   ℹ️  Skipping validation (issue is about templates/documentation)"
            )
            return True, None

        project_brief_path = Path("PROJECT_BRIEF.md")

        if not project_brief_path.exists():
            print("   ℹ️  No PROJECT_BRIEF.md found (optional)")
            return True, None

        print("   📋 Validating PROJECT_BRIEF.md...")
        result = validate_project_brief(project_brief_path)

        if result.is_valid:
            print("   ✅ PROJECT_BRIEF.md validation passed")
            validation_msg = "✅ PROJECT_BRIEF.md validated successfully"

            if result.warnings:
                print(f"   ⚠️  Validation warnings: {len(result.warnings)}")
                for warning in result.warnings[:3]:
                    print(f"      - {warning}")
                validation_msg += f"\n\n**Warnings ({len(result.warnings)}):**\n"
                for warning in result.warnings[:5]:
                    validation_msg += f"- {warning}\n"

            return True, validation_msg
        else:
            print("   ❌ PROJECT_BRIEF.md validation failed")
            for error in result.errors[:5]:
                print(f"      - {error}")

            validation_msg = "❌ PROJECT_BRIEF.md validation failed\n\n**Errors:**\n"
            for error in result.errors[:5]:
                validation_msg += f"- {error}\n"

            if result.warnings:
                validation_msg += f"\n**Warnings:**\n"
                for warning in result.warnings[:3]:
                    validation_msg += f"- {warning}\n"

            return False, validation_msg

    def _create_branch(self, branch_name: str, issue, issue_claimed: bool) -> bool:
        """Create a new git branch"""
        print("\n" + "-"*80)
        print("📋 STEP 4: BRANCH CREATION")
        print("-"*80)
        print(f"   Branch name: {branch_name}")
        
        try:
            self.git_repo.git.checkout("-b", branch_name)
            print(f"   ✅ Branch created successfully")
            return True
        except Exception as e:
            print(f"   ❌ Failed to create branch: {e}")
            if issue_claimed and not self.dry_mode:
                issue.create_comment(f"❌ Failed to create branch: {e}")
            elif issue_claimed:
                print("   🔍 DRY MODE: Would post branch creation failure comment")
            return False

    def _generate_fix(
        self, issue, issue_body: str, issue_labels: List[str]
    ) -> Optional[str]:
        """Generate a fix using Claude AI"""
        print("\n" + "-"*80)
        print("📋 STEP 5: GENERATING FIX WITH CLAUDE AI")
        print("-"*80)
        
        # Get context with retry
        @retry_github_api
        def get_readme():
            try:
                return self.repo.get_readme().decoded_content.decode("utf-8")[:2000]
            except:
                return "No README found"

        try:
            readme = get_readme()
            if readme == "No README found":
                print("   ⚠️  No README found")
            else:
                print("   ✅ Loaded README context")
        except:
            readme = "No README found"
            print("   ⚠️  No README found")

        # Build prompt for Claude CLI
        cli_prompt = f"""You are an expert software engineer. Fix this GitHub issue by modifying the necessary files.

Repository: {self.repo.full_name}
Issue #{issue.number}: {issue.title}

Description:
{issue_body}

Labels: {', '.join(issue_labels)}

Context from README:
{readme}

Instructions:
1. Analyze the issue carefully
2. Use the Read tool to examine relevant files
3. Use the Write tool to create or modify files with your fixes
4. Make complete, working changes
5. After making changes, summarize what you did

You have access to Read and Write tools to modify files in the current directory."""

        print(f"   📝 Prompt prepared ({len(cli_prompt)} chars)")
        print(f"   🎯 Issue type: {', '.join(issue_labels)}")

        # Try Claude CLI first if available
        if USE_CLAUDE_CLI:
            print("\n   🤖 Attempting to use Claude CLI Agent...")
            print("   Tools enabled: Read, Write, Bash")
            print("   Permission mode: acceptEdits")

            try:
                # Try to initialize with require_cli=False to check availability
                agent = ClaudeAgent(
                    output_format="text",
                    verbose=True,
                    allowed_tools=["Read", "Write", "Bash"],
                    permission_mode="acceptEdits",
                    require_cli=False,
                )

                if agent.cli_available:
                    print("\n   📤 Sending query to Claude CLI...")
                    print("   " + "="*76)
                    result = agent.query(cli_prompt, stream_output=True)
                    print("   " + "="*76)

                    # Extract the response
                    if isinstance(result, dict) and "result" in result:
                        summary = result["result"]
                    else:
                        summary = str(result)

                    print(f"\n   ✅ Claude CLI completed work successfully")
                    print(f"   📊 Response length: {len(summary)} chars")
                    
                    # Print the full output
                    print("\n   📄 CLAUDE OUTPUT:")
                    print("   " + "-"*76)
                    for line in summary.split('\n'):
                        print(f"   {line}")
                    print("   " + "-"*76)

                    return summary
                else:
                    print("   ⚠️  Claude CLI not available, falling back to Anthropic SDK")

            except Exception as e:
                print(f"\n   ⚠️  Claude CLI error: {e}")
                print("   ℹ️  Falling back to Anthropic SDK")

        # Fallback to Anthropic SDK
        print("\n   🤖 Using Anthropic SDK (API-based approach)")
        
        if not self.anthropic_api_key:
            print("   ❌ No Anthropic API key provided")
            return None

        try:
            client = Anthropic(api_key=self.anthropic_api_key)
            
            # Build a simpler prompt for API (no tool use)
            api_prompt = f"""You are an expert software engineer. Analyze this GitHub issue and provide a detailed solution.

Repository: {self.repo.full_name}
Issue #{issue.number}: {issue.title}

Description:
{issue_body}

Labels: {', '.join(issue_labels)}

Context from README:
{readme}

Please provide:
1. Analysis of the issue
2. Detailed solution approach
3. Specific code changes needed (with file paths and code snippets)
4. Testing recommendations

Format your response clearly with sections."""

            print("\n   📤 Sending query to Claude API...")
            
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                messages=[{"role": "user", "content": api_prompt}]
            )
            
            summary = response.content[0].text
            
            print(f"\n   ✅ Claude API completed successfully")
            print(f"   📊 Response length: {len(summary)} chars")
            
            # Print the output
            print("\n   📄 CLAUDE OUTPUT:")
            print("   " + "-"*76)
            summary_lines = summary.split('\n')
            for line in summary_lines[:50]:  # Limit output
                print(f"   {line}")
            if len(summary_lines) > 50:
                remaining_lines = len(summary_lines) - 50
                print(f"   ... ({remaining_lines} more lines)")
            print("   " + "-"*76)
            
            print("\n   ⚠️  Note: API mode provides guidance only")
            print("   ℹ️  Manual code changes may be needed based on the suggestions")

            return summary

        except Exception as e:
            print(f"\n   ❌ Anthropic SDK error: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _create_pr_if_changes(self, issue, branch_name: str, summary: str) -> bool:
        """Create a PR if files were modified"""
        print("\n" + "-"*80)
        print("📋 STEP 6: COMMITTING CHANGES & CREATING PR")
        print("-"*80)
        
        if not self.git_repo.is_dirty(untracked_files=True):
            print("   ⚠️  No files were modified")
            if not self.dry_mode:
                issue.create_comment(
                    "⚠️ No changes were made. The issue may need manual review."
                )
                # Track as failed (no changes)
                self.outcome_tracker.update_status(
                    issue_number=issue.number,
                    status=ResolutionStatus.FAILED,
                    error_message="No file changes generated"
                )
                print("   📊 Outcome tracking: Marked as FAILED (no changes)")
            else:
                print("   🔍 DRY MODE: Would post no changes comment")
            return False

        # Get list of changed files
        changed_files = [item.a_path for item in self.git_repo.index.diff(None)]
        untracked_files = self.git_repo.untracked_files
        files_modified = changed_files + untracked_files

        print(f"   📝 Files modified: {len(files_modified)}")
        for f in files_modified:
            print(f"      ✏️  {f}")

        # Commit changes
        print("\n   📦 Committing changes...")
        self.git_repo.git.add("-A")
        commit_message = f"""Fix: Resolve issue #{issue.number}

{issue.title}

Closes #{issue.number}

---
Generated by Issue Resolver Agent using Claude Agent SDK"""

        self.git_repo.index.commit(commit_message)
        print("   ✅ Changes committed")

        if self.dry_mode:
            print(f"   🔍 DRY MODE: Would push branch '{branch_name}' to origin")
            print("   🔍 DRY MODE: Would create pull request")
            print("   🔍 DRY MODE: Would update issue with results")
            print("\n" + "="*80)
            print("🎉 DRY MODE: WORKFLOW VALIDATION COMPLETED SUCCESSFULLY")
            print("="*80)
            print(f"\n📊 SUMMARY (DRY MODE):")
            print(f"   Issue: #{issue.number} - {issue.title}")
            print(f"   Branch: {branch_name}")
            print(f"   Files changed: {len(files_modified)}")
            print(f"   Status: ✅ Would be ready for review")
            print("\n" + "="*80 + "\n")
            return True

        # Push
        print(f"   📤 Pushing branch '{branch_name}' to origin...")
        origin = self.git_repo.remote("origin")
        try:
            push_info = origin.push(branch_name)
            if push_info and push_info[0].flags & push_info[0].ERROR:
                raise Exception(f"Push failed: {push_info[0].summary}")
            print(f"   ✅ Branch pushed successfully")
        except Exception as e:
            print(f"   ❌ Failed to push branch: {e}")
            raise

        # Create PR with retry
        print("\n   🔀 Creating Pull Request...")
        pr_title = f"Fix: {issue.title}"
        pr_body = f"""{summary[:500]}

## Changes
{chr(10).join(['- ' + f for f in files_modified[:20]])}

Closes #{issue.number}

---
*Generated by Issue Resolver Agent using Claude Agent SDK*"""

        @retry_github_api
        def create_pr():
            # Verify branch exists on remote before creating PR
            try:
                self.repo.get_branch(branch_name)
            except Exception as e:
                print(f"   ⚠️  Branch not found on remote yet, retrying... ({e})")
                raise
            
            return self.repo.create_pull(
                title=pr_title, body=pr_body, head=branch_name, base="main"
            )

        pr = create_pr()

        print(f"   ✅ Pull Request created: #{pr.number}")
        print(f"   🔗 URL: {pr.html_url}")

        # Track successful PR creation
        self.outcome_tracker.update_status(
            issue_number=issue.number,
            status=ResolutionStatus.RESOLVED,
            pr_number=pr.number,
            files_changed=len(files_modified)
        )
        print(f"   📊 Outcome tracking: Marked as RESOLVED (PR #{pr.number})")

        # Update issue with retry
        print("\n   💬 Updating issue with results...")

        @retry_github_api
        def update_issue():
            return issue.create_comment(
                f"""✅ **Solution Ready**

Pull Request: #{pr.number}

**Changes:**
{chr(10).join(['- ' + f for f in files_modified[:10]])}

---
*Completed at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}*"""
            )

        update_issue()
        print("   ✅ Issue updated")

        print("\n" + "="*80)
        print("🎉 WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*80)
        print(f"\n📊 SUMMARY:")
        print(f"   Issue: #{issue.number} - {issue.title}")
        print(f"   Branch: {branch_name}")
        print(f"   PR: #{pr.number}")
        print(f"   Files changed: {len(files_modified)}")
        print(f"   Status: ✅ Ready for review")
        print("\n" + "="*80 + "\n")
        return True

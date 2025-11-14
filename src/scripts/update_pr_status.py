#!/usr/bin/env python3
"""
Update PR Status - Background job to track PR merge status

This script checks PRs linked to tracked issues and updates their status
when they are merged or closed.

Usage:
    python update_pr_status.py
"""

import os
import sys
from pathlib import Path
from github import Github

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.outcome_tracker import OutcomeTracker, ResolutionStatus


def main():
    # Get GitHub token from environment
    github_token = os.environ.get("GITHUB_TOKEN")
    repo_url = os.environ.get("GITHUB_REPOSITORY")

    if not github_token:
        print("❌ GITHUB_TOKEN environment variable not set")
        sys.exit(1)

    if not repo_url:
        print("❌ GITHUB_REPOSITORY environment variable not set")
        sys.exit(1)

    print("🔄 Updating PR merge status...")
    print(f"   Repository: {repo_url}")

    # Initialize GitHub client
    g = Github(github_token)
    repo = g.get_repo(repo_url)

    # Initialize tracker
    tracker = OutcomeTracker()

    # Get all resolved issues that might need status update
    import sqlite3
    conn = sqlite3.connect(tracker.db_path)
    cursor = conn.cursor()

    # Find all resolved (but not merged/closed) issues with PR numbers
    cursor.execute("""
        SELECT issue_number, pr_number
        FROM outcomes
        WHERE status = 'resolved'
        AND pr_number IS NOT NULL
        ORDER BY created_at DESC
    """)

    pending_prs = cursor.fetchall()
    conn.close()

    if not pending_prs:
        print("   ℹ️  No PRs pending status update")
        return

    print(f"   Found {len(pending_prs)} PR(s) to check")

    updated_count = 0
    for issue_number, pr_number in pending_prs:
        try:
            pr = repo.get_pull(pr_number)

            if pr.merged:
                print(f"   ✅ PR #{pr_number} (Issue #{issue_number}) was merged")
                tracker.update_status(
                    issue_number=issue_number,
                    status=ResolutionStatus.MERGED,
                    pr_number=pr_number
                )
                updated_count += 1
            elif pr.state == "closed":
                print(f"   🚫 PR #{pr_number} (Issue #{issue_number}) was closed without merge")
                tracker.update_status(
                    issue_number=issue_number,
                    status=ResolutionStatus.CLOSED,
                    pr_number=pr_number
                )
                updated_count += 1

        except Exception as e:
            print(f"   ⚠️  Error checking PR #{pr_number}: {e}")
            continue

    print(f"\n✅ Updated {updated_count} PR status(es)")


if __name__ == "__main__":
    main()

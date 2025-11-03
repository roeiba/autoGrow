#!/usr/bin/env python3
"""
Issue Resolver Agent
Takes an open issue, analyzes it with Claude AI, implements a fix, and creates a PR
"""

import os
import sys
import json
import time
from datetime import datetime
from github import Github
from anthropic import Anthropic
import git

# Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
REPO_NAME = os.getenv('REPO_NAME')
SPECIFIC_ISSUE = os.getenv('SPECIFIC_ISSUE')
LABELS_TO_HANDLE = os.getenv('ISSUE_LABELS_TO_HANDLE', 'bug,enhancement').split(',')
LABELS_TO_SKIP = os.getenv('ISSUE_LABELS_TO_SKIP', 'wontfix,duplicate,in-progress').split(',')
MAX_TIME = int(os.getenv('MAX_EXECUTION_TIME', '8')) * 60

start_time = time.time()

print("🤖 Issue Resolver Agent Starting")

# Initialize clients
gh = Github(GITHUB_TOKEN)
repo = gh.get_repo(REPO_NAME)
anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)
git_repo = git.Repo('.')

# Select issue
selected_issue = None

if SPECIFIC_ISSUE:
    print(f"🎯 Working on specific issue #{SPECIFIC_ISSUE}")
    selected_issue = repo.get_issue(int(SPECIFIC_ISSUE))
else:
    print("🔍 Searching for issue to resolve...")
    open_issues = repo.get_issues(state='open', sort='created', direction='asc')
    
    for issue in open_issues:
        if issue.pull_request:
            continue
        
        issue_labels = [label.name for label in issue.labels]
        if any(skip_label in issue_labels for skip_label in LABELS_TO_SKIP):
            continue
        
        if LABELS_TO_HANDLE and not any(handle_label in issue_labels for handle_label in LABELS_TO_HANDLE):
            continue
        
        comments = list(issue.get_comments())
        if any('Issue Resolver Agent' in c.body and 'claimed' in c.body.lower() for c in comments):
            continue
        
        selected_issue = issue
        break

if not selected_issue:
    print("ℹ️  No suitable issues found")
    sys.exit(0)

print(f"✅ Selected issue #{selected_issue.number}: {selected_issue.title}")

# Claim the issue
claim_message = f"""🤖 **Issue Resolver Agent**

I'm working on this issue now.

**Started at:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}
**Status:** In Progress

---
*Automated by GitHub Actions*"""

selected_issue.create_comment(claim_message)
selected_issue.add_to_labels('in-progress')
print("📝 Claimed issue")

# Get context
try:
    readme = repo.get_readme().decoded_content.decode('utf-8')[:2000]
except:
    readme = "No README found"

issue_body = selected_issue.body or "No description provided"
issue_labels = [label.name for label in selected_issue.labels]

# Build prompt
prompt = f"""You are an expert software engineer fixing a GitHub issue.

Repository: {REPO_NAME}
Issue #{selected_issue.number}: {selected_issue.title}

Description:
{issue_body}

Labels: {', '.join(issue_labels)}

Context:
{readme}

Provide a fix in JSON format:
{{
  "analysis": "Your analysis",
  "files_to_modify": [
    {{
      "path": "relative/path/to/file",
      "action": "create|modify|delete",
      "content": "Complete file content",
      "explanation": "Why this change"
    }}
  ],
  "pr_title": "Concise PR title",
  "pr_body": "Detailed PR description"
}}

Provide complete, working code."""

# Call Claude
print("🤖 Calling Claude AI...")
message = anthropic.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    messages=[{"role": "user", "content": prompt}]
)

response_text = message.content[0].text
print("✅ Received solution")

# Parse response
try:
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0].strip()
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0].strip()
    
    solution = json.loads(response_text)
    
except json.JSONDecodeError as e:
    print(f"❌ Failed to parse response: {e}")
    selected_issue.create_comment(f"❌ Failed to parse AI response. Will retry later.")
    selected_issue.remove_from_labels('in-progress')
    sys.exit(1)

# Create branch
branch_name = f"fix/issue-{selected_issue.number}-{int(time.time())}"
print(f"🌿 Creating branch: {branch_name}")
git_repo.git.checkout('-b', branch_name)

# Apply changes
files_modified = []
for file_change in solution.get('files_to_modify', []):
    file_path = file_change.get('path')
    action = file_change.get('action', 'modify')
    content = file_change.get('content', '')
    
    if not file_path:
        continue
    
    full_path = os.path.join('.', file_path)
    
    if action == 'delete':
        if os.path.exists(full_path):
            os.remove(full_path)
            files_modified.append(f"Deleted: {file_path}")
    else:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
        files_modified.append(f"{action.capitalize()}: {file_path}")

if not files_modified:
    print("⚠️  No files modified")
    selected_issue.create_comment("⚠️ No changes generated.")
    selected_issue.remove_from_labels('in-progress')
    sys.exit(0)

# Commit
git_repo.git.add('-A')
commit_message = f"""Fix: {solution.get('pr_title', f'Resolve issue #{selected_issue.number}')}

Closes #{selected_issue.number}

---
Generated by Issue Resolver Agent"""

git_repo.index.commit(commit_message)
print("✅ Committed")

# Push
origin = git_repo.remote('origin')
origin.push(branch_name)
print(f"✅ Pushed branch")

# Create PR
pr_title = solution.get('pr_title', f"Fix: Resolve issue #{selected_issue.number}")
pr_body = f"""{solution.get('pr_body', '')}

## Changes
{chr(10).join(['- ' + f for f in files_modified])}

Closes #{selected_issue.number}

---
*Generated by Issue Resolver Agent*"""

pr = repo.create_pull(
    title=pr_title,
    body=pr_body,
    head=branch_name,
    base='main'
)

print(f"✅ Created PR #{pr.number}")

# Update issue
selected_issue.create_comment(f"""✅ **Solution Ready**

Pull Request: #{pr.number}

**Changes:**
{chr(10).join(['- ' + f for f in files_modified])}

---
*Completed at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}*""")

selected_issue.remove_from_labels('in-progress')

print("🎉 Complete!")

# PROJECT_BRIEF.md Validation Skip Logic

## Problem

The issue resolver was validating PROJECT_BRIEF.md for **all** issues, which caused problems when:
- Creating PROJECT_BRIEF.md templates
- Fixing PROJECT_BRIEF.md itself
- Working on documentation issues
- Setting up initial project structure

Example failure:
```
✅ Selected issue #2: Create example PROJECT_BRIEF.md templates for common project types
❌ PROJECT_BRIEF.md validation failed
   - Missing required section: 'Technical Preferences'
   - Found empty sections: 📋 Core Requirements, 🏗️ Technical Preferences
❌ PROJECT_BRIEF.md validation failed - aborting to save API calls
```

## Solution

Added intelligent skip logic that detects when an issue is **about** PROJECT_BRIEF.md or templates, and skips validation in those cases.

## Implementation

### 1. Skip Detection Function

```python
def should_skip_validation(issue_title, issue_body, issue_labels):
    """
    Determine if PROJECT_BRIEF.md validation should be skipped for this issue
    """
    # Keywords that indicate the issue is about creating/fixing PROJECT_BRIEF.md itself
    skip_keywords = [
        'project_brief',
        'project brief',
        'template',
        'example',
        'documentation',
        'readme',
        'setup',
        'initial',
        'bootstrap'
    ]
    
    # Check if issue is about PROJECT_BRIEF.md or templates
    text_to_check = f"{issue_title} {issue_body}".lower()
    if any(keyword in text_to_check for keyword in skip_keywords):
        return True
    
    # Check labels
    skip_labels = ['documentation', 'setup', 'template']
    if any(label in skip_labels for label in issue_labels):
        return True
    
    return False
```

### 2. Updated Validation Function

```python
def validate_project_brief_if_exists(issue_title="", issue_body="", issue_labels=None):
    """
    Validate PROJECT_BRIEF.md if it exists in the repository
    
    Args:
        issue_title: The issue title (for skip detection)
        issue_body: The issue body (for skip detection)
        issue_labels: List of issue labels (for skip detection)
    """
    issue_labels = issue_labels or []
    
    # Check if we should skip validation for this issue
    if should_skip_validation(issue_title, issue_body, issue_labels):
        print("ℹ️  Skipping PROJECT_BRIEF.md validation (issue is about templates/documentation)")
        return True, None
    
    # ... rest of validation logic
```

### 3. Usage in Issue Resolver

```python
# Get issue details for validation check
issue_body = selected_issue.body or "No description provided"
issue_labels = [label.name for label in selected_issue.labels]

# Validate PROJECT_BRIEF.md before proceeding (may skip for certain issues)
is_valid, validation_msg = validate_project_brief_if_exists(
    issue_title=selected_issue.title,
    issue_body=issue_body,
    issue_labels=issue_labels
)
```

## Skip Triggers

Validation is skipped when the issue contains:

### Keywords in Title/Body
- `project_brief` or `project brief`
- `template`
- `example`
- `documentation`
- `readme`
- `setup`
- `initial`
- `bootstrap`

### Labels
- `documentation`
- `setup`
- `template`

## Examples

### Issues That Skip Validation ✅

1. **"Create example PROJECT_BRIEF.md templates for common project types"**
   - Contains: `template`, `project_brief`
   - Skip: ✅

2. **"Fix PROJECT_BRIEF.md validation errors"**
   - Contains: `project_brief`
   - Skip: ✅

3. **"Add documentation for setup process"**
   - Contains: `documentation`, `setup`
   - Skip: ✅

4. **Issue with label: `documentation`**
   - Label: `documentation`
   - Skip: ✅

### Issues That Require Validation ❌

1. **"Add user authentication feature"**
   - No skip keywords
   - Skip: ❌ (validates PROJECT_BRIEF.md)

2. **"Fix bug in payment processing"**
   - No skip keywords
   - Skip: ❌ (validates PROJECT_BRIEF.md)

3. **"Improve API performance"**
   - No skip keywords
   - Skip: ❌ (validates PROJECT_BRIEF.md)

## Benefits

1. ✅ **Allows bootstrap issues** - Can create templates without valid PROJECT_BRIEF.md
2. ✅ **Prevents circular dependencies** - Can fix PROJECT_BRIEF.md issues
3. ✅ **Saves API calls** - Doesn't abort on validation for meta-issues
4. ✅ **Flexible** - Easy to add more skip keywords/labels
5. ✅ **Safe** - Still validates for actual feature/bug work

## Testing

### Test Case 1: Template Creation Issue
```bash
Issue: "Create example PROJECT_BRIEF.md templates"
Expected: Skip validation ✅
Result: ℹ️  Skipping PROJECT_BRIEF.md validation (issue is about templates/documentation)
```

### Test Case 2: Feature Issue
```bash
Issue: "Add user login functionality"
Expected: Validate PROJECT_BRIEF.md ✅
Result: 📋 Validating PROJECT_BRIEF.md...
```

### Test Case 3: Documentation Label
```bash
Issue: "Update API docs"
Label: documentation
Expected: Skip validation ✅
Result: ℹ️  Skipping PROJECT_BRIEF.md validation (issue is about templates/documentation)
```

## Configuration

To add more skip conditions, update the `should_skip_validation()` function:

```python
# Add more keywords
skip_keywords = [
    'project_brief',
    'template',
    'your_new_keyword',  # Add here
]

# Add more labels
skip_labels = ['documentation', 'setup', 'template', 'your_new_label']  # Add here
```

## Edge Cases

### Case 1: Issue mentions PROJECT_BRIEF.md but isn't about it
**Example:** "Add feature X as described in PROJECT_BRIEF.md"
**Behavior:** Will skip validation (mentions PROJECT_BRIEF.md)
**Acceptable:** Yes, because the issue is referencing the brief, likely for context

### Case 2: Issue has "template" in unrelated context
**Example:** "Use template pattern for database connections"
**Behavior:** Will skip validation (contains "template")
**Acceptable:** Mostly yes, but could be refined with more context analysis

### Case 3: Multiple skip conditions
**Example:** Issue has both "template" keyword AND "documentation" label
**Behavior:** Skips on first match (efficient)
**Acceptable:** Yes

## Future Improvements

Potential enhancements:
- [ ] More sophisticated NLP-based detection
- [ ] Configurable skip rules via environment variables
- [ ] Per-repository skip configuration
- [ ] Whitelist/blacklist patterns
- [ ] Skip validation only for specific file paths
- [ ] Context-aware keyword matching

## Related Files

- `.github/scripts/issue_resolver.py` - Main implementation
- `src/utils/project_brief_validator.py` - Validation logic
- `.agents/ISSUE_RESOLVER_DEBUG_SUMMARY.md` - Debugging guide

## Summary

The skip logic makes the issue resolver smarter by:
1. Detecting meta-issues about PROJECT_BRIEF.md itself
2. Allowing documentation and setup work without validation
3. Still enforcing validation for actual feature/bug work
4. Preventing circular dependencies and bootstrap problems

This enables the issue resolver to handle a wider range of issues intelligently.

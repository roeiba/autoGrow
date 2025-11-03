# Custom Prompts Guide

Complete guide to customizing the Claude agent's behavior using external prompt templates.

## Quick Start

### Using Built-in Templates

```bash
# Use the default template (balanced)
export PROMPT_TEMPLATE=default

# Use minimal template (concise)
export PROMPT_TEMPLATE=minimal

# Use detailed template (comprehensive)
export PROMPT_TEMPLATE=detailed
```

### Using Custom Templates

```bash
# Create your custom prompt
cat > my-prompt.txt << 'EOF'
Fix this issue: {issue_title}

{issue_body}

Provide JSON with files_to_modify array.
EOF

# Use your custom prompt
export PROMPT_TEMPLATE=/path/to/my-prompt.txt
```

## Built-in Templates

### default.txt
**Best for**: General purpose issue fixing

**Characteristics**:
- Balanced detail level
- Requests JSON output
- Includes context about languages and frameworks
- Asks for analysis and testing notes

**When to use**:
- Most bug fixes
- Feature implementations
- General maintenance tasks

### minimal.txt
**Best for**: Simple, straightforward fixes

**Characteristics**:
- Very concise
- Minimal context
- Quick fixes

**When to use**:
- Typos and simple bugs
- Documentation fixes
- Quick patches

### detailed.txt
**Best for**: Complex issues requiring thorough analysis

**Characteristics**:
- Comprehensive instructions
- Requests root cause analysis
- Emphasizes testing and side effects
- Includes solution approach

**When to use**:
- Complex bugs
- Performance issues
- Architectural changes
- Critical fixes

## Template Variables

All templates have access to these variables:

| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| `{repo_owner}` | string | `microsoft` | Repository owner |
| `{repo_name}` | string | `vscode` | Repository name |
| `{languages}` | list | `python, javascript` | Detected languages |
| `{key_files}` | list | `package.json, setup.py` | Framework files |
| `{issue_number}` | int | `42` | Issue number |
| `{issue_title}` | string | `Fix memory leak` | Issue title |
| `{issue_body}` | string | Full text | Issue description |
| `{issue_labels}` | list | `bug, critical` | Issue labels |
| `{issue_url}` | string | `https://...` | Issue URL |

## Creating Custom Prompts

### Basic Template

```text
You are fixing issue #{issue_number} in {repo_owner}/{repo_name}.

Issue: {issue_title}
{issue_body}

Languages: {languages}

Provide your fix in JSON format.
```

### Advanced Template

```text
CONTEXT:
Repository: {repo_owner}/{repo_name}
Languages: {languages}
Frameworks: {key_files}

ISSUE #{issue_number}: {issue_title}
Labels: {issue_labels}

{issue_body}

INSTRUCTIONS:
1. Analyze the root cause
2. Design a minimal fix
3. Provide complete code
4. Explain testing approach

OUTPUT (JSON):
{{
    "analysis": "...",
    "files_to_modify": [
        {{"path": "...", "code": "...", "reasoning": "..."}}
    ],
    "testing_notes": "..."
}}
```

### Language-Specific Template

```text
You are a {languages} expert fixing issue #{issue_number}.

{issue_title}
{issue_body}

Follow {languages} best practices and idioms.
Ensure type safety and error handling.

Provide JSON with files_to_modify.
```

## Usage Examples

### Example 1: Use Detailed Template

```bash
cd deployment/docker-agents/claude-agent

# Set in .env
echo "PROMPT_TEMPLATE=detailed" >> .env

# Or export
export PROMPT_TEMPLATE=detailed

./run-agent.sh
```

### Example 2: Custom Template File

```bash
# Create custom prompt
cat > prompts/security-focused.txt << 'EOF'
SECURITY REVIEW for issue #{issue_number}

{issue_title}
{issue_body}

Repository: {repo_owner}/{repo_name}
Languages: {languages}

SECURITY REQUIREMENTS:
1. Input validation
2. Error handling
3. No SQL injection
4. No XSS vulnerabilities
5. Secure defaults

Provide secure fix in JSON format.
EOF

# Use it
export PROMPT_TEMPLATE=security-focused
./run-agent.sh
```

### Example 3: Testing-Focused Template

```bash
cat > prompts/test-driven.txt << 'EOF'
TEST-DRIVEN FIX for #{issue_number}

{issue_title}
{issue_body}

Languages: {languages}

APPROACH:
1. Write failing test first
2. Implement minimal fix
3. Ensure test passes
4. Refactor if needed

OUTPUT:
{{
    "test_file": {{"path": "...", "code": "..."}},
    "implementation": {{"path": "...", "code": "..."}},
    "test_results": "..."
}}
EOF

export PROMPT_TEMPLATE=test-driven
./run-agent.sh
```

### Example 4: Documentation Template

```bash
cat > prompts/docs-focused.txt << 'EOF'
DOCUMENTATION FIX for #{issue_number}

{issue_title}
{issue_body}

Improve documentation with:
- Clear examples
- API documentation
- Usage guidelines
- Common pitfalls

Provide updated docs in JSON.
EOF

export PROMPT_TEMPLATE=docs-focused
./run-agent.sh
```

## Best Practices

### 1. Start Simple
Begin with a basic template and iterate:

```text
Fix: {issue_title}
{issue_body}
Provide JSON with files_to_modify.
```

### 2. Be Explicit
Clear instructions produce better results:

```text
❌ "Fix the bug"
✅ "Identify root cause, implement minimal fix, add unit test"
```

### 3. Request Structure
JSON output is easier to parse:

```json
{
    "analysis": "...",
    "files_to_modify": [...]
}
```

### 4. Provide Context
Help Claude understand the codebase:

```text
Repository: {repo_owner}/{repo_name}
Languages: {languages}
Key files: {key_files}
```

### 5. Set Quality Standards
Define what good looks like:

```text
Requirements:
- Follow existing code style
- Add error handling
- Include tests
- Update documentation
```

## Testing Your Prompts

### 1. Create Test Issue

Create a simple test issue in a test repository.

### 2. Test Prompt

```bash
export REPO_URL=https://github.com/your-test/repo
export ISSUE_NUMBER=1
export PROMPT_TEMPLATE=your-template
./run-agent.sh
```

### 3. Review Output

Check the generated PR for:
- Correct understanding of issue
- Appropriate fix
- Code quality
- Completeness

### 4. Iterate

Refine your prompt based on results.

## Troubleshooting

### Issue: Invalid JSON Response

**Problem**: Claude returns text instead of JSON

**Solution**: Be explicit in prompt:
```text
IMPORTANT: Respond ONLY with valid JSON.
No markdown code blocks, no explanations outside JSON.

{{
    "files_to_modify": [...]
}}
```

### Issue: Incomplete Fixes

**Problem**: Fix doesn't fully address issue

**Solution**: Request thorough analysis:
```text
1. Analyze root cause (not just symptoms)
2. Design complete solution
3. Consider edge cases
4. Provide all necessary changes
```

### Issue: Too Broad Changes

**Problem**: Agent modifies unrelated code

**Solution**: Request minimal changes:
```text
Provide the MINIMAL fix that solves the issue.
Do NOT refactor unrelated code.
Only modify files directly related to the issue.
```

### Issue: Missing Context

**Problem**: Agent doesn't understand codebase

**Solution**: Provide more context:
```text
Repository: {repo_owner}/{repo_name}
Languages: {languages}
Frameworks: {key_files}
Issue labels: {issue_labels}
```

## Advanced Techniques

### Conditional Instructions

```text
{%- if "critical" in issue_labels %}
This is CRITICAL. Prioritize correctness over elegance.
{%- else %}
Focus on clean, maintainable code.
{%- endif %}
```

### Multi-Step Process

```text
STEP 1: Root Cause Analysis
Identify the underlying cause.

STEP 2: Solution Design
Plan your approach.

STEP 3: Implementation
Provide complete code.

STEP 4: Testing
Explain verification.
```

### Role-Based Prompts

```text
You are a SENIOR {languages} ENGINEER with 10+ years experience.

Your reputation depends on:
- Code quality
- Thorough testing
- Clear documentation
- Minimal changes
```

## Prompt Library

### Bug Fix Template
```text
BUG FIX: {issue_title}

{issue_body}

Repository: {repo_owner}/{repo_name}
Languages: {languages}

1. Identify root cause
2. Implement minimal fix
3. Add regression test
4. Verify no side effects

JSON output required.
```

### Feature Template
```text
FEATURE: {issue_title}

Requirements:
{issue_body}

Languages: {languages}
Frameworks: {key_files}

Implement with:
- Clean code
- Tests
- Documentation
- Examples

JSON output required.
```

### Refactoring Template
```text
REFACTOR: {issue_title}

Current issues:
{issue_body}

Goals:
- Improve clarity
- Enhance performance
- Maintain compatibility

Languages: {languages}

JSON output required.
```

## Contributing Templates

Share your templates with the community:

1. Test thoroughly
2. Document use case
3. Add to `prompts/` directory
4. Update this guide
5. Submit PR

## Resources

- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Prompt Templates Directory](./prompts/)
- [Agent Architecture](./ARCHITECTURE.md)

## Support

For help with custom prompts:
- Check [prompts/README.md](./prompts/README.md)
- Review built-in templates
- Test with simple issues first
- Iterate based on results

# Prompt Templates

This directory contains prompt templates for the Claude agent. You can customize how the agent analyzes and fixes issues by creating your own prompts.

## Available Templates

### default.txt
The standard prompt template with balanced detail and structure.

**Use when**: General purpose issue fixing

### minimal.txt
A concise prompt for simple, straightforward fixes.

**Use when**: Simple bugs, typos, or quick fixes

### detailed.txt
A comprehensive prompt for complex issues requiring thorough analysis.

**Use when**: Complex bugs, architectural changes, or critical fixes

## Creating Custom Prompts

### Template Variables

Your prompt can use these variables (will be replaced at runtime):

| Variable | Description | Example |
|----------|-------------|---------|
| `{repo_owner}` | Repository owner | `microsoft` |
| `{repo_name}` | Repository name | `vscode` |
| `{languages}` | Detected languages | `python, javascript` |
| `{key_files}` | Framework files | `package.json, requirements.txt` |
| `{issue_number}` | Issue number | `42` |
| `{issue_title}` | Issue title | `Fix memory leak` |
| `{issue_body}` | Issue description | Full issue text |
| `{issue_labels}` | Issue labels | `bug, high-priority` |
| `{issue_url}` | Issue URL | `https://github.com/...` |

### Example Custom Prompt

Create `prompts/my-custom.txt`:

```
You are fixing issue #{issue_number} in {repo_owner}/{repo_name}.

Issue: {issue_title}
Details: {issue_body}

The codebase uses: {languages}

Provide a JSON response with files_to_modify array.
```

### Using Custom Prompts

Set the `PROMPT_TEMPLATE` environment variable:

```bash
# Use a built-in template
export PROMPT_TEMPLATE=detailed

# Use a custom template file
export PROMPT_TEMPLATE=/path/to/my-prompt.txt

# Or in .env file
PROMPT_TEMPLATE=detailed
```

## Best Practices

### 1. Be Specific
Clear instructions lead to better fixes:
```
❌ "Fix the issue"
✅ "Analyze the root cause, then provide a minimal fix with tests"
```

### 2. Request Structured Output
JSON format makes parsing easier:
```json
{
    "analysis": "...",
    "files_to_modify": [...]
}
```

### 3. Provide Context
Help Claude understand the codebase:
```
Repository uses {languages}
Key frameworks: {key_files}
```

### 4. Set Expectations
Define what a good fix looks like:
```
- Follow existing code style
- Add error handling
- Consider edge cases
```

### 5. Request Explanations
Understanding helps with review:
```
For each change, explain:
- What you're changing
- Why it fixes the issue
- Potential side effects
```

## Prompt Engineering Tips

### For Simple Fixes
- Keep it concise
- Focus on the specific issue
- Request minimal changes

### For Complex Issues
- Ask for root cause analysis
- Request solution design before implementation
- Include testing requirements
- Ask about side effects

### For Learning
- Request detailed explanations
- Ask for alternative approaches
- Include reasoning for decisions

## Testing Your Prompts

1. Create your prompt file
2. Set `PROMPT_TEMPLATE` to your file
3. Run the agent on a test issue
4. Review the generated fix
5. Iterate on the prompt

## Examples by Use Case

### Bug Fix
```
Analyze this bug: {issue_title}

{issue_body}

Find the root cause and provide a minimal fix.
Include unit tests to prevent regression.
```

### Feature Implementation
```
Implement this feature: {issue_title}

Requirements: {issue_body}

Provide:
1. Implementation plan
2. Code changes
3. Tests
4. Documentation updates
```

### Refactoring
```
Refactor the code related to: {issue_title}

Current issues: {issue_body}

Improve:
- Code clarity
- Performance
- Maintainability

Ensure backward compatibility.
```

### Documentation
```
Improve documentation for: {issue_title}

Current state: {issue_body}

Add:
- Clear examples
- API documentation
- Usage guidelines
```

## Advanced Features

### Conditional Logic
Use template variables to adjust behavior:

```
You are fixing a {issue_labels} issue in {languages}.

{%- if "critical" in issue_labels %}
This is CRITICAL. Prioritize correctness over elegance.
{%- else %}
Focus on clean, maintainable code.
{%- endif %}
```

### Multi-Language Support
Adjust prompts based on detected languages:

```
{%- if "python" in languages %}
Follow PEP 8 style guidelines.
{%- elif "javascript" in languages %}
Follow Airbnb JavaScript style guide.
{%- endif %}
```

## Troubleshooting

### Issue: Agent produces invalid JSON
**Solution**: Be explicit about JSON format in prompt:
```
IMPORTANT: Respond ONLY with valid JSON. No markdown, no explanations outside JSON.
```

### Issue: Fixes are too broad
**Solution**: Request minimal changes:
```
Provide the MINIMAL fix that solves the issue. Do not refactor unrelated code.
```

### Issue: Missing context
**Solution**: Include more template variables:
```
Repository: {repo_owner}/{repo_name}
Languages: {languages}
Frameworks: {key_files}
```

## Contributing Prompts

Have a great prompt template? Share it!

1. Create your prompt file
2. Test it on various issues
3. Document its use case
4. Submit a PR with your template

## License

Prompt templates are part of the AI Project Template.

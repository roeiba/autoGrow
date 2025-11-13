# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please report it via GitHub's private vulnerability reporting feature.

**Include**:
- Description of the vulnerability
- Steps to reproduce
- Potential impact

**Response Time**: We aim to acknowledge within 48 hours and provide updates weekly.

## Security Best Practices

### API Keys
- Never commit API keys to version control
- Use environment variables (`.env` file)
- Follow the `.env.example` template
- Add `.env` to `.gitignore`

### Dependencies
- Keep dependencies updated
- Review security advisories regularly
- Use `pip-audit` or similar tools

### CI/CD
- Store secrets in GitHub Secrets
- Never log sensitive information
- Use minimal permissions for workflows

Thank you for helping keep this project secure!

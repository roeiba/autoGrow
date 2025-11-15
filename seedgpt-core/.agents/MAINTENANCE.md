# Repository Maintenance Guide

> **For maintainers and contributors working on the template itself**

## Overview

This guide covers maintaining and improving the AI Project Template repository. For using the template to create projects, see the main README.

## Repository Structure

### Core Template Files
- **PROJECT_BRIEF.md** - Template for users to fill out their requirements
- **README.md** - Public-facing documentation for GitHub
- **QUICKSTART.md** - Quick start guide for users
- **.agents/** - AI agent guidelines and maintenance docs (this folder)
- **.ai-prompts/** - AI session tracking templates

### Template Directories
- **src/** - Empty structure for generated code
- **project-docs/** - Documentation structure template
- **tasks/** - Task management system template
- **deployment/** - Infrastructure templates
- **scripts/** - Automation script templates

### Repository Metadata
- **CHANGELOG.md** - Version history
- **CONTRIBUTING.md** - Contribution guidelines
- **CODE_OF_CONDUCT.md** - Community standards
- **SECURITY.md** - Security policy
- **.github/** - GitHub-specific configurations

## Maintenance Tasks

### Regular Updates

**Monthly:**
- Review and update dependencies in example files
- Check for broken links in documentation
- Update technology stack examples
- Review and merge community PRs

**Quarterly:**
- Update version numbers
- Review and update best practices
- Audit security guidelines
- Update CI/CD examples

**Annually:**
- Major version updates
- Comprehensive documentation review
- Technology stack modernization
- User feedback integration

### Version Management

Follow semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes to template structure
- **MINOR**: New features or significant improvements
- **PATCH**: Bug fixes and minor improvements

Update these files when releasing:
1. `CHANGELOG.md` - Add release notes
2. `.agents/project-rules.md` - Update version number
3. `README.md` - Update version badge
4. Git tag - Create release tag

### Documentation Maintenance

**Keep Updated:**
- Technology stack examples (as new frameworks emerge)
- Best practices (as industry standards evolve)
- Security guidelines (as threats change)
- AI agent instructions (as AI capabilities improve)

**Consistency Checks:**
- Cross-reference all internal links
- Ensure examples match current structure
- Verify all paths are correct
- Check code snippets for accuracy

### Quality Assurance

**Before Each Release:**
- [ ] Test template generation with AI agents
- [ ] Verify all directory structures exist
- [ ] Check all README files are present
- [ ] Validate .gitignore patterns
- [ ] Test example workflows
- [ ] Review documentation for clarity
- [ ] Check for typos and formatting issues

### Community Management

**Issue Triage:**
1. Label issues appropriately (bug, enhancement, question)
2. Respond within 48 hours
3. Request additional information if needed
4. Close duplicates and link to originals
5. Prioritize based on impact and effort

**Pull Request Review:**
1. Check for breaking changes
2. Verify documentation updates
3. Test changes locally
4. Ensure conventional commit format
5. Merge or request changes within 1 week

### Improvement Process

**Proposing Changes:**
1. Create issue describing the improvement
2. Discuss with maintainers
3. Create ADR if architectural change
4. Implement and test
5. Update documentation
6. Submit PR with clear description

**Adding New Features:**
1. Ensure it aligns with template philosophy
2. Document in appropriate `.agents/` folder
3. Add examples and templates
4. Update main README if user-facing
5. Add to CHANGELOG

## File Organization Rules

### What Goes in `.agents/`
- **project-rules.md** - Master AI guidelines
- **MAINTENANCE.md** - This file (repo maintenance)
- **CONTRIBUTING_GUIDE.md** - Detailed contribution process
- **RELEASE_PROCESS.md** - How to create releases
- Any other maintainer-focused documentation

### What Stays in Root
- **README.md** - User-facing documentation
- **PROJECT_BRIEF.md** - User template
- **QUICKSTART.md** - User quick start
- **CHANGELOG.md** - Public version history
- **LICENSE** - License file
- **CODE_OF_CONDUCT.md** - Community standards
- **SECURITY.md** - Security policy

### What Goes in `.github/`
- Workflow files
- Issue templates
- PR templates
- GitHub-specific configurations

## Testing the Template

### Manual Testing Checklist

**Basic Structure:**
- [ ] Clone fresh copy
- [ ] Verify all directories exist
- [ ] Check all README files are present
- [ ] Validate .gitignore works

**AI Agent Testing:**
- [ ] Fill out PROJECT_BRIEF.md with test project
- [ ] Run AI agent generation
- [ ] Verify generated structure
- [ ] Check generated documentation
- [ ] Test generated code (if applicable)

**Documentation Testing:**
- [ ] Follow QUICKSTART.md step-by-step
- [ ] Verify all links work
- [ ] Check code examples are valid
- [ ] Ensure instructions are clear

### Automated Testing

Consider adding:
- Link checker for documentation
- Structure validator
- Example code linter
- CI workflow to verify template integrity

## Common Issues and Solutions

### Issue: Outdated Technology Examples
**Solution:** Review quarterly and update based on:
- npm/PyPI download statistics
- GitHub stars and activity
- Industry adoption trends
- Community feedback

### Issue: Confusing Documentation
**Solution:**
- Gather user feedback
- Identify pain points
- Simplify language
- Add more examples
- Create visual diagrams

### Issue: Template Too Complex
**Solution:**
- Review each directory's necessity
- Consider making some parts optional
- Improve documentation
- Add progressive disclosure

### Issue: AI Agents Misunderstanding Guidelines
**Solution:**
- Make instructions more explicit
- Add concrete examples
- Test with multiple AI models
- Gather feedback from AI-assisted sessions

## Release Process

### Pre-Release
1. Update CHANGELOG.md
2. Update version in project-rules.md
3. Update version in README.md
4. Run full test suite
5. Review all documentation
6. Check for broken links

### Release
1. Create git tag: `git tag -a v2.x.x -m "Release v2.x.x"`
2. Push tag: `git push origin v2.x.x`
3. Create GitHub release with notes
4. Announce in discussions/social media

### Post-Release
1. Monitor for issues
2. Respond to feedback
3. Plan next version improvements
4. Update roadmap

## Roadmap Planning

### Short-term (Next Release)
- Bug fixes
- Documentation improvements
- Minor feature additions

### Medium-term (Next Quarter)
- New template features
- Enhanced AI guidelines
- Additional examples

### Long-term (Next Year)
- Major architectural improvements
- New technology integrations
- Advanced automation

## Contact and Support

**For Maintainers:**
- Use GitHub Discussions for questions
- Create issues for bugs/features
- Use PR reviews for code discussions

**For Users:**
- Direct to main README and QUICKSTART
- Use GitHub Issues for bug reports
- Use Discussions for questions

## Version History

- **2.0.1** (2025-11-11): Reorganized for GitHub launch
- **2.0.0** (2025-11-03): Complete rewrite
- **1.0.0** (2025-11-01): Initial version

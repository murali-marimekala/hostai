# 🤝 Contributing to AI Personal Productivity Assistant

Thank you for your interest in contributing to the AI Personal Productivity Assistant! This document provides guidelines for contributing to the project while maintaining security and privacy standards.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Security Guidelines](#security-guidelines)
- [Contributing Guidelines](#contributing-guidelines)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## 🤝 Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- Be respectful and inclusive
- Focus on constructive feedback
- Maintain user privacy and security
- Follow the security guidelines outlined in [SECURITY.md](SECURITY.md)

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of machine learning concepts
- Familiarity with privacy and security best practices

### Quick Setup

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/ai-productivity-assistant.git
   cd ai-productivity-assistant
   ```
3. **Set up development environment**:
   ```bash
   ./setup.sh
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🛠️ Development Setup

### Environment Configuration

1. **Copy environment template**:
   ```bash
   cp .env.example .env
   ```

2. **Edit configuration** (optional for development):
   ```bash
   nano .env
   ```

3. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

### IDE Setup

We recommend using VS Code with the following extensions:
- Python
- Pylance
- GitLens
- Prettier (for documentation)

## 🔒 Security Guidelines

### Critical Security Rules

1. **Never commit sensitive data**:
   - Database files (`.db`, `.sqlite`)
   - Log files (`.log`)
   - User configuration files
   - API keys or credentials
   - Trained models with user data

2. **Always check before committing**:
   ```bash
   git status
   git diff --cached
   ```

3. **Use environment variables** for sensitive configuration:
   ```python
   # Good
   import os
   api_key = os.getenv('API_KEY')

   # Bad - hardcoded
   api_key = "sk-your-secret-key"
   ```

4. **Follow the principle of least privilege**:
   - Request minimal permissions
   - Validate all inputs
   - Sanitize data before processing

### Security Checklist

Before submitting a pull request, ensure:

- [ ] No sensitive data is committed
- [ ] No hardcoded secrets in code
- [ ] Input validation is implemented
- [ ] Error messages don't leak sensitive information
- [ ] Dependencies are from trusted sources
- [ ] Code follows secure coding practices

## 📝 Contributing Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write descriptive variable and function names
- Add docstrings to all public functions and classes

### Commit Messages

Use clear, descriptive commit messages:

```bash
# Good
feat: add privacy filter for sensitive file types
fix: resolve memory leak in activity monitor
docs: update security guidelines

# Bad
update
fix bug
changes
```

### Branch Naming

```bash
feature/add-privacy-controls
bugfix/fix-memory-leak
docs/update-security-guide
hotfix/critical-security-patch
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/

# Run specific test file
pytest tests/test_privacy.py

# Run tests in verbose mode
pytest -v
```

### Writing Tests

- Write unit tests for all new functions
- Include integration tests for new features
- Test error conditions and edge cases
- Mock external dependencies
- Test privacy controls thoroughly

### Test Coverage

Maintain test coverage above 80% for new code. Run coverage reports:

```bash
pytest --cov=src/ --cov-report=html
open htmlcov/index.html
```

## 📤 Submitting Changes

### Pull Request Process

1. **Ensure your branch is up to date**:
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Run all checks**:
   ```bash
   # Security checks
   git status  # Ensure no sensitive files

   # Code quality
   black --check src/
   isort --check-only src/
   flake8 src/

   # Tests
   pytest --cov=src/
   ```

3. **Create a pull request**:
   - Use a descriptive title
   - Provide detailed description
   - Reference related issues
   - Add screenshots for UI changes

4. **Address review feedback**:
   - Make requested changes
   - Re-run tests and checks
   - Update documentation if needed

### Pull Request Template

Please use this template for pull requests:

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update
- [ ] Security enhancement

## Security Checklist
- [ ] No sensitive data committed
- [ ] Privacy controls implemented
- [ ] Input validation added
- [ ] Dependencies reviewed

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Additional Notes
Any additional information or context
```

## 🐛 Reporting Issues

### Security Issues
**🚨 NEVER report security vulnerabilities publicly!**

For security issues:
1. Email maintainers directly
2. Use encrypted communication if possible
3. Allow time for fixes before disclosure

### Bug Reports

Use the issue template and include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- System information
- Log files (sanitized)

### Feature Requests

For new features:
- Describe the problem you're trying to solve
- Explain why it's important
- Suggest implementation approach
- Consider privacy implications

## 📚 Additional Resources

- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [SECURITY.md](SECURITY.md) - Security guidelines
- [README.md](README.md) - Project overview
- [API Documentation](docs/api.md) - Code documentation

## 🙏 Recognition

Contributors will be recognized in:
- CHANGELOG.md for significant contributions
- GitHub contributors list
- Release notes

Thank you for contributing to making productivity tools more secure and privacy-respecting! 🔒✨
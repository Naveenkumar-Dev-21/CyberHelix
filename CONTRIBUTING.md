# Contributing to AutoPenTest

We welcome contributions to AutoPenTest! This document provides guidelines for contributing to this project.

## Code of Conduct

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

## Getting Started

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/autopentest.git
   cd autopentest
   ```

3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

5. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Development Guidelines

#### Code Style
- Use [Black](https://black.readthedocs.io/) for code formatting: `black .`
- Use [isort](https://pycqa.github.io/isort/) for import sorting: `isort .`
- Follow PEP 8 guidelines
- Use type hints where possible

#### Testing
- Write tests for all new features and bug fixes
- Maintain or improve test coverage
- Run tests before submitting: `pytest`
- Run with coverage: `pytest --cov=src`

#### Security Considerations
- **NEVER** commit actual API keys or credentials
- Use environment variables for sensitive configuration
- Run security checks: `bandit -r src/`
- Validate all user inputs
- Follow responsible disclosure practices

#### Documentation
- Update README.md if needed
- Add docstrings to all functions and classes
- Update inline comments for complex logic
- Include usage examples

## Types of Contributions

### Bug Fixes
1. Check if the bug is already reported in Issues
2. Create a new issue if not exists
3. Fork and create a fix
4. Include tests that verify the fix
5. Submit a pull request

### New Features
1. Create an issue to discuss the feature first
2. Ensure it aligns with project goals
3. Implement the feature with tests
4. Update documentation
5. Submit a pull request

### Security Tools Integration
When adding new security tools:
1. Ensure the tool is legitimate and widely used
2. Add proper error handling
3. Include version detection
4. Add configuration options
5. Update the tool availability checker

### New Exploit Modules
For adding exploit capabilities:
1. **Educational Purpose Only** - All exploits must be for educational/authorized testing
2. Include proper warnings and disclaimers
3. Add safeguards against misuse
4. Document required permissions/setup
5. Include cleanup procedures

## Pull Request Process

1. **Pre-submission Checklist:**
   - [ ] Code follows style guidelines
   - [ ] Tests pass locally
   - [ ] Security checks pass
   - [ ] Documentation updated
   - [ ] No sensitive data committed

2. **Pull Request Requirements:**
   - Clear title and description
   - Link to related issues
   - List of changes made
   - Testing instructions
   - Screenshots (if UI changes)

3. **Review Process:**
   - Maintainers will review within 48 hours
   - Address feedback promptly
   - Keep PR focused and small
   - Rebase on main branch if needed

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_reconnaissance.py

# Run with verbose output
pytest -v
```

### Test Categories
- **Unit Tests**: Test individual functions/methods
- **Integration Tests**: Test module interactions
- **System Tests**: Test full workflows
- **Security Tests**: Test for vulnerabilities

### Mock External Dependencies
- Mock all external tool calls
- Use sample data for API responses
- Don't make real network requests in tests

## Performance Considerations

- Profile code with heavy computations
- Use async/await for I/O operations where beneficial
- Consider memory usage for large scan results
- Add timeout handling for all external calls

## Security Guidelines

### For Contributors
- Never test on systems without explicit permission
- Use isolated lab environments for testing
- Follow responsible disclosure for any vulnerabilities found
- Don't include actual exploit code that could cause harm

### For Code Review
- Check for input validation
- Verify proper error handling
- Ensure no credentials are hardcoded
- Review for potential misuse scenarios

## Issue Guidelines

### Bug Reports
Include:
- AutoPenTest version
- Operating system
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs
- Minimal reproduction example

### Feature Requests
Include:
- Clear use case description
- Proposed implementation approach
- Alternative solutions considered
- Potential drawbacks/concerns

## Release Process

1. Update version numbers
2. Update CHANGELOG.md
3. Run full test suite
4. Update documentation
5. Create release notes
6. Tag the release

## Getting Help

- Check existing Issues and Discussions
- Join our community channels
- Read the documentation thoroughly
- Ask specific, detailed questions

## Recognition

Contributors will be acknowledged in:
- CONTRIBUTORS.md file
- Release notes
- Documentation credits

## Legal and Ethical Considerations

By contributing, you acknowledge:
- Your contributions are original or properly attributed
- You have rights to contribute the code
- You agree to the project license terms
- You understand this tool is for authorized testing only

## Questions?

If you have questions about contributing, please:
1. Check this document first
2. Search existing issues
3. Create a new issue with the "question" label
4. Contact maintainers directly for sensitive matters

Thank you for contributing to AutoPenTest! 🛡️

---

**Remember: This tool is for authorized security testing only. Always ensure you have explicit permission before testing any systems.**

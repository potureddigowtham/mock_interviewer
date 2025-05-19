# Contributing to AI Interviewer

Thank you for considering contributing to the AI Interviewer project! We welcome all contributions, from bug reports to new features and documentation improvements.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)
- [Code Style](#code-style)
- [Commit Message Guidelines](#commit-message-guidelines)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs
- Check if the bug has already been reported in the [issues](https://github.com/potureddigowtham/mock_interviewer/issues)
- If not, create a new issue with a clear title and description
- Include steps to reproduce the issue and expected vs actual behavior
- Add screenshots or logs if applicable

### Feature Requests
- Open an issue with the "enhancement" label
- Clearly describe the feature and why it would be valuable
- Include any relevant use cases or examples

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/mock_interviewer.git
   cd mock_interviewer
   ```
3. Set up the backend:
   ```bash
   cd server
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Set up the frontend:
   ```bash
   cd ../client
   npm install
   ```
5. Create a `.env` file based on `.env.example` and update with your configuration

### Pull Request Process

1. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number-description
   ```
2. Make your changes following the code style guidelines
3. Add tests for your changes if applicable
4. Run tests and ensure they pass
5. Commit your changes following the commit message guidelines
6. Push to your fork and open a Pull Request
7. Ensure all CI checks pass
8. Address any code review feedback

## Code Style

### Python
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints for all new code
- Keep functions small and focused
- Document public APIs with docstrings
- Format code with Black (run `black .`)
- Sort imports with isort (run `isort .`)

### JavaScript/TypeScript
- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use TypeScript for all new code
- Use functional components with hooks
- Document component props with PropTypes or TypeScript interfaces
- Format code with Prettier (run `npm run format`)

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification. Here are some examples:

```
feat: add user authentication
fix: resolve login redirect issue
docs: update README with setup instructions
style: format code with Prettier
refactor: improve database query performance
test: add unit tests for user service
chore: update dependencies
```

## License

By contributing, you agree that your contributions will be licensed under its MIT License.

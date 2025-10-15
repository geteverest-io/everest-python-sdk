# Contributing to Everest API Python Client

Thank you for your interest in contributing to the Everest API Python Client! We welcome contributions from the community.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/everest-python-sdk.git
   cd everest-python-sdk
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Development Workflow

### Setting up your environment

We recommend using a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
pip install -r requirements-dev.txt
```

### Running Tests

Run the test suite with pytest:

```bash
pytest tests/
```

Run tests with coverage:

```bash
pytest tests/ --cov=everest_api --cov-report=html
```

### Code Style

This project follows PEP 8 style guidelines. Please ensure your code is formatted properly:

```bash
# Format code with black
black everest_api/ tests/

# Check code style with flake8
flake8 everest_api/ tests/

# Type checking with mypy
mypy everest_api/
```

### Making Changes

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and ensure all tests pass

3. Add tests for new functionality

4. Update documentation as needed

5. Commit your changes:
   ```bash
   git commit -m "Add your descriptive commit message"
   ```

6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

7. Open a Pull Request

## Pull Request Guidelines

- Keep pull requests focused on a single issue or feature
- Write clear, descriptive commit messages
- Include tests for new functionality
- Update documentation as needed
- Ensure all tests pass
- Follow the existing code style

## Reporting Issues

When reporting issues, please include:

- Python version
- Operating system
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Any error messages or stack traces

## Code of Conduct

Please be respectful and constructive in all interactions with the project and its community.

## Questions?

If you have questions, feel free to:
- Open an issue on GitHub
- Contact the maintainers

Thank you for contributing!

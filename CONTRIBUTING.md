# Contributing to TruthLens AI

Thank you for your interest in contributing. This document outlines the guidelines and workflow for submitting contributions.

---

## Ways to Contribute

- **Bug Reports** — Report issues encountered while using the project
- **Feature Requests** — Propose new features or improvements
- **Code Contributions** — Submit pull requests with bug fixes or new functionality
- **Documentation** — Improve README, docstrings, or guides
- **Testing** — Expand test coverage and report findings

---

## Reporting Issues

Before opening an issue, check whether it already exists. When filing a new one, include:

1. A clear description of the problem
2. Steps to reproduce the behavior
3. Expected vs. actual behavior
4. Relevant error messages or logs
5. Your environment (OS, Python version, device type)

**Issue Template:**

```
## Description
Brief description of the issue.

## Steps to Reproduce
1. Step 1
2. Step 2

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Environment
- OS: [Windows / macOS / Linux]
- Python: [version]
- Device: [CPU / GPU]
- Error: [if applicable]
```

---

## Feature Requests

When proposing a feature, provide:

1. A clear description of the feature and its purpose
2. Use cases that justify it
3. How it fits within the existing architecture
4. Any relevant references or examples

---

## Development Setup

### 1. Fork and Clone

```bash
git clone https://github.com/yourusername/truthlens-ai.git
cd truthlens-ai
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -e .  # Install in development mode
```

### 4. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

---

## Code Standards

### Style Guide

- Follow **PEP 8** for Python code
- Use **Black** for formatting
- Use **Flake8** for linting

```bash
black src/ app.py main.py
flake8 src/ app.py main.py
```

### Docstrings

All public functions must include docstrings:

```python
def analyze(self, image_path: str, caption: str) -> Dict[str, Any]:
    """
    Analyze an image-caption pair for authenticity indicators.

    Args:
        image_path (str): Absolute or relative path to the image file.
        caption (str): Caption text associated with the image.

    Returns:
        dict: Dictionary containing:
            - verdict (str): AUTHENTIC, SUSPICIOUS, or FAKE
            - confidence (int): Confidence score 0-100
            - evidence (list): Supporting evidence items

    Raises:
        FileNotFoundError: If the image file does not exist.
        ValueError: If the caption is empty or None.
    """
```

### Type Hints

Use type hints on all function signatures:

```python
from typing import Dict, List, Any, Optional

def process_images(
    image_paths: List[str],
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, List[Any]]:
    """Process a batch of images."""
```

### Comments

Comment to explain intent, not implementation:

```python
# Use weighted scoring rather than simple averaging because visual
# anomalies carry stronger signal than absent metadata alone.
fake_signals = weighted_score(anomalies, weights=[4, 2, 1])
```

---

## Testing

### Writing Tests

Add tests to the `tests/` directory:

```python
import pytest
from src.vision_analyzer import VisionAnalyzer

def test_vision_analyzer_initialization():
    """VisionAnalyzer should initialize without raising exceptions."""
    analyzer = VisionAnalyzer(api_key="test_key")
    assert analyzer is not None
```

### Running Tests

```bash
pytest tests/ -v
```

---

## Submitting Pull Requests

### Before Submitting

1. Ensure all tests pass: `pytest tests/ -v`
2. Format code: `black src/ app.py main.py`
3. Lint: `flake8 src/ app.py main.py`
4. Update documentation as needed
5. Verify no breaking changes are introduced

### PR Checklist

- [ ] Code follows PEP 8 and is Black-formatted
- [ ] Tests added or updated
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Commit messages follow the format below

### Commit Message Format

```
type: brief description

Optional extended explanation.

Fixes #issue_number
```

**Types:**

| Type       | Description              |
|------------|--------------------------|
| `feat`     | New feature              |
| `fix`      | Bug fix                  |
| `docs`     | Documentation changes    |
| `style`    | Formatting only          |
| `refactor` | Code restructuring       |
| `test`     | Test additions/changes   |
| `chore`    | Maintenance tasks        |

**Examples:**

```
feat: add batch image analysis support

fix: correct CLIP similarity threshold calculation

docs: update installation instructions for Windows

refactor: simplify metadata extraction logic
```

### PR Template

```
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] No new warnings introduced

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests updated or added
- [ ] Documentation updated
- [ ] No breaking changes
```

---

## Review Process

1. **Automated checks** — Tests and linting run on every PR
2. **Code review** — A maintainer will review your changes
3. **Feedback** — Changes may be requested before approval
4. **Merge** — Approved PRs are merged into the main branch

Respond to review comments in a timely manner. Request a re-review once requested changes are addressed.

---

## Code of Conduct

All contributors are expected to:

- Engage respectfully and professionally
- Provide constructive, focused feedback
- Use inclusive language
- Welcome diverse perspectives
- Credit contributors appropriately

---

## Resources

- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Git Workflow Reference](https://git-scm.com/docs)
- [pytest Documentation](https://pytest.org/)
- [GitHub Docs](https://docs.github.com/)

---

## Questions

Open a Discussion or Issue on GitHub for clarification before starting significant work.

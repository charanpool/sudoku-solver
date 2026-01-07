# Contributing to Sudoku Solver 🧩

First off, **thank you** for considering contributing to this project! Every contribution helps make this solver better.

This document provides guidelines and steps for contributing. Following these guidelines helps communicate that you respect the time of the developers managing and developing this open-source project.

---

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)

---

## 🚀 Getting Started

### New to Open Source?

If you're new to open source, welcome! Here are some resources to get you started:
- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [First Timers Only](https://www.firsttimersonly.com/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

### New to This Project?

1. Read the [README](README.md) to understand what the project does
2. Look through [open issues](../../issues) to see what needs work
3. Check out issues labeled `good first issue` for beginner-friendly tasks

---

## 🤝 How Can I Contribute?

### 🐛 Reporting Bugs

Found a bug? Please open an issue with:

1. **A clear title** describing the problem
2. **Steps to reproduce** the behavior
3. **Expected behavior** – what should have happened?
4. **Actual behavior** – what actually happened?
5. **Environment details** – Python version, OS, etc.

### 💡 Suggesting Features

Have an idea? We'd love to hear it! Open an issue with:

1. **A clear title** for the feature
2. **The problem** it would solve
3. **Your proposed solution**
4. **Any alternatives** you've considered

### 📝 Improving Documentation

Documentation improvements are always welcome:
- Fix typos or unclear explanations
- Add examples or use cases
- Improve code comments

### 💻 Contributing Code

Ready to code? Here's how:

1. Look for issues labeled `help wanted` or `good first issue`
2. Comment on the issue to let others know you're working on it
3. Fork the repo and create your branch
4. Write your code and tests
5. Submit a pull request

---

## 🔧 Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/sudoku-solver.git
   cd sudoku-solver
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

---

## 🔄 Pull Request Process

1. **Update documentation** if you're changing functionality
2. **Add tests** for new features when applicable
3. **Ensure your code runs** without errors
4. **Write a clear PR description** explaining:
   - What changes you made
   - Why you made them
   - Any relevant issue numbers (use `Fixes #123` or `Closes #123`)

5. **Be responsive** to feedback and make requested changes

### PR Title Format

Use clear, descriptive titles:
- `feat: Add backtracking solver`
- `fix: Correct hidden single detection in boxes`
- `docs: Update installation instructions`
- `refactor: Simplify markup cell computation`

---

## 📏 Style Guidelines

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and reasonably sized

### Example

```python
def check_in_row(row: list, value: int) -> bool:
    """
    Check if a value exists in the given row.
    
    Args:
        row: A list of integers representing a Sudoku row
        value: The value to search for (1-9)
    
    Returns:
        True if value is found, False otherwise
    """
    return value in row
```

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Keep the first line under 50 characters
- Reference issues when relevant

---

## 🎉 Recognition

All contributors will be recognized in the project! Your contributions make this project better for everyone.

---

## ❓ Questions?

Don't hesitate to ask! Open an issue with your question or start a discussion. We're here to help.

**Thank you for contributing! 🙏**

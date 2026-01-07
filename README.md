# 🧩 Sudoku Solver

A Python-based Sudoku puzzle solver that uses human-like solving techniques including **naked pairs**, **hidden singles**, and the **preemptive set (occupancy) theorem**.

![Python](https://img.shields.io/badge/Python-3.7+-3776ab?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=flat-square)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-blue?style=flat-square)

---

## ✨ Features

- **Markup/Candidate System** – Identifies possible values for each empty cell
- **Naked Singles** – Fills cells with only one possible candidate
- **Hidden Singles** – Finds values that can only go in one place within a row, column, or box
- **Naked Pairs/Triples** – Detects and eliminates candidates using set theory
- **Preemptive Sets** – Advanced constraint propagation using the occupancy theorem

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/sudoku-solver.git
   cd sudoku-solver
   ```

2. **Run the solver**
   ```bash
   python sudoku_solver.py
   ```

---

## 📥 Input Methods

The solver supports **three ways** to input puzzles:

### 1️⃣ Default Puzzle
```bash
python sudoku_solver.py
```
Runs with a built-in sample puzzle.

### 2️⃣ Interactive Mode
```bash
python sudoku_solver.py -i
```
Enter your puzzle row by row:
```
🧩 Enter your Sudoku puzzle
   Use 0 for empty cells
   Enter 9 digits per row (spaces optional)

   Row 1: 003000001
   Row 2: 090035268
   ...
```

### 3️⃣ File Input (Text or JSON)
```bash
python sudoku_solver.py examples/easy.txt
python sudoku_solver.py examples/puzzle.json
```

**Text file format** (9 lines, 9 digits, `0` = empty):
```
003000001
090035268
000000000
070000186
130860725
286000943
041080300
050206010
000003070
```

**JSON file format**:
```json
{
  "puzzle": [
    [0, 0, 3, 0, 0, 0, 0, 0, 1],
    [0, 9, 0, 0, 3, 5, 2, 6, 8],
    ...
  ]
}
```

### Command-Line Options

| Option | Description |
|--------|-------------|
| `FILE` | Path to puzzle file (`.txt` or `.json`) |
| `-i, --interactive` | Enter puzzle interactively |
| `-v, --verbose` | Show detailed solving steps |
| `-h, --help` | Show help message |

> **Note:** Use `0` to represent empty cells in all formats.

---

## 🧠 How It Works

The solver mimics human problem-solving strategies:

| Technique | Description |
|-----------|-------------|
| **Markup** | For each empty cell, compute all valid candidates (1-9) based on row, column, and 3×3 box constraints |
| **Naked Single** | If a cell has only one candidate, fill it in |
| **Hidden Single** | If a number can only appear in one cell within a row/column/box, place it there |
| **Naked Pair** | If two cells in a unit share exactly two candidates, eliminate those from other cells |
| **Preemptive Set** | Generalized constraint propagation for pairs, triples, and quads |

---

## 🤝 Contributing

**Contributions are what make the open-source community amazing!** Whether you're fixing a bug, adding a feature, or improving documentation – every contribution is valued.

### Quick Start for Contributors

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 💡 Ideas for Contribution

- [ ] Add **backtracking** as a fallback for unsolvable-by-logic puzzles
- [ ] Add **puzzle difficulty rating**
- [ ] Implement **X-Wing** and **Swordfish** techniques
- [ ] Create a **web interface** using Flask or Streamlit
- [ ] Add **unit tests** with pytest
- [ ] Improve **code documentation** and type hints
- [ ] Add **puzzle generator** functionality
- [ ] Create **visualization** of the solving process
- [ ] Add **solution validation** to verify correctness

Please read our [Contributing Guidelines](CONTRIBUTING.md) before getting started.

---

## 📋 Project Roadmap

- [x] Basic constraint propagation
- [x] Naked singles and hidden singles
- [x] Naked pairs/triples detection
- [x] Command-line interface with multiple input methods
- [x] File input support (text and JSON)
- [ ] Complete backtracking implementation
- [ ] Web-based UI
- [ ] Comprehensive test suite

---

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgments

- Inspired by classic Sudoku solving algorithms
- Thanks to all contributors who help improve this project!

---

## 📬 Contact

Have questions or suggestions? Feel free to:
- Open an [Issue](../../issues)
- Start a [Discussion](../../discussions)
- Submit a [Pull Request](../../pulls)

---

<p align="center">
  <b>⭐ If you find this project useful, please consider giving it a star!</b>
</p>

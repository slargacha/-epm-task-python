# EPAM Python Task - Three Module Implementation

A comprehensive Python project implementing three distinct modules with full test coverage (>90%), integrated CI/CD pipeline, and automated deployment. This project is part of the EPAM professional development course.

## 📋 Project Overview

This repository contains three independent Python modules designed to demonstrate software engineering best practices:
- Unit testing with pytest
- Code coverage analysis (>90% required)
- GitHub Actions CI/CD automation
- SonarQube Cloud static code analysis
- Automated deployment to free cloud platform

## 🎯 Modules

### 1. Dictionary Class

A simple dictionary/vocabulary manager that stores word-definition pairs and provides lookup functionality.

**Features:**
- Add new word entries with definitions
- Look up definitions by word
- Graceful handling of missing entries

**Implementation:**
```python
from src.dictionary import Dictionary

d = Dictionary()
d.newentry('Apple', 'A fruit that grows on trees')
print(d.look('Apple'))  # Output: A fruit that grows on trees
print(d.look('Banana')) # Output: Can't find entry for Banana
```

**Files:**
- `src/dictionary.py` - Core implementation
- `tests/test_dictionary.py` - Unit tests

---

### 2. Shopping Cart Total Calculator

Calculates the total cost of items with tax application. Useful for e-commerce systems requiring dynamic tax calculation.

**Features:**
- Calculate sum of item prices from a product dictionary
- Apply tax rate (e.g., IVA)
- Ignore items not in the price catalog
- Return result rounded to 2 decimal places

**Example:**
```python
from src.shop import get_total

costs = {'socks': 5, 'shoes': 60, 'sweater': 30}
total = get_total(costs, ['socks', 'shoes'], 0.09)
# Calculation: 5 + 60 = 65
# With 9% tax: 65 * 1.09 = 70.85
print(total)  # Output: 70.85
```

**Files:**
- `src/shop.py` - Core implementation
- `tests/test_shop.py` - Unit tests

---

### 3. Nth Letter Concatenation

Extracts the nth letter from each word in an array, where n is the word's position in the list, and concatenates them into a new string.

**Features:**
- Extract character at position matching word index
- Concatenate characters into a single string
- Support for arrays of any valid length

**Example:**
```python
from src.nth_letter import nth_letter

result = nth_letter(["yoda", "best", "has"])
# y (index 0 from "yoda")
# e (index 1 from "best")
# s (index 2 from "has")
print(result)  # Output: "yes"
```

**Files:**
- `src/nth_letter.py` - Core implementation
- `tests/test_nth_letter.py` - Unit tests

---

## 📁 Project Structure

```
-epm-task-python/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── dictionary.py            # Module 1: Dictionary class
│   ├── shop.py                  # Module 2: Total calculator
│   └── nth_letter.py            # Module 3: Nth letter function
│
├── tests/
│   ├── __init__.py
│   ├── test_dictionary.py       # Tests for Dictionary
│   ├── test_shop.py             # Tests for get_total
│   └── test_nth_letter.py       # Tests for nth_letter
│
├── .github/workflows/
│   └── ci-cd.yml                # GitHub Actions CI/CD pipeline
│
├── copilot-instructions.md      # AI coding assistant guidelines
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── setup.py                     # Package metadata and configuration
├── pytest.ini                   # Pytest configuration
├── .coveragerc                  # Code coverage configuration
└── .gitignore                   # Git ignore rules

```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip or conda package manager
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd -epm-task-python
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🌐 Aplicación Web

Este proyecto ahora incluye un servicio web simple con Flask.

### Ejecutar localmente
```bash
python -m src.app
```

Luego abre en el navegador:
```bash
http://localhost:8000
```

### Endpoints disponibles
- `GET /` - Página de bienvenida con ejemplos
- `GET /dictionary/<palabra>` - Busca una definición
- `GET /shop/total?items=articulo1,articulo2&tax=0.09` - Calcula precio total con iva
- `GET /nth-letter?words=palabra1,palabra2,palabra3` - Devuelve concatenación de letras

### Ejemplos
- `http://localhost:8000/dictionary/apple`
- `http://localhost:8000/shop/total?items=socks,shoes&tax=0.09`
- `http://localhost:8000/nth-letter?words=yoda,best,has`

---

## 🐳 Despliegue Docker

Este proyecto incluye una imagen Docker lista para producción con Gunicorn.

### Construir localmente
```bash
docker build -t epam-python-task:latest .
```

### Ejecutar localmente
```bash
docker run --rm -p 8000:8000 epam-python-task:latest
```

### Registro de contenedores
El workflow de GitHub Actions construye y publica la imagen en
GitHub Container Registry como:
- `ghcr.io/<org>/epam-python-task:latest`
- `ghcr.io/<org>/epam-python-task:<commit-sha>`

---

## ✅ Testing & Quality Assurance

### Run All Tests
```bash
pytest tests/ -v
```

### Generate Coverage Report
```bash
pytest --cov=src --cov-report=term-missing --cov-report=html
```

The coverage report is generated with a **minimum threshold of 90%**. Failing this threshold will cause the CI pipeline to fail.

### View Coverage in HTML
```bash
# After running the command above
open htmlcov/index.html  # On macOS/Linux
start htmlcov\index.html # On Windows
```

---

## 🔄 CI/CD Pipeline

The project uses **GitHub Actions** for continuous integration and continuous deployment. The pipeline includes:

### Pipeline Stages

1. **Test Execution**
   - Runs pytest with coverage analysis
   - Fails if any test fails
   - Fails if coverage drops below 90%

2. **Code Quality Analysis**
   - Sends analysis to **SonarQube Cloud**
   - Performs static code scanning
   - Checks for code smells and vulnerabilities

3. **Deployment**
   - Deploys to free cloud platform on successful pipeline completion
   - Current platform: *To be configured*

### Workflow Configuration
See [.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml) for detailed pipeline configuration.

---

## 🌐 Deployment

The project is automatically deployed to a **free cloud platform** upon successful CI/CD pipeline completion.

### Deployment Platform: Render.com (Docker Deployment)

**Why Render with Docker?**
- **Consistency**: Uses the exact same image tested in CI.
- **Security**: Deploys the pre-built image from GHCR.
- **Professional Workflow**: Separation between Build and Deploy stages.
- **Free Tier**: Support for web services with custom images.

**Alternatives:**
- **Render.com** - Free tier with sleep mode
- **GitHub Pages** - For static documentation
- **Heroku alternatives** - Due to Heroku free tier discontinuation

### Deployment URL
https://epam-python-task.onrender.com

---

## 🔧 Development Workflow

### Creating a Feature

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes and write tests:**
   - Add your implementation in `src/`
   - Add comprehensive tests in `tests/`
   - Ensure >90% coverage

3. **Run tests locally:**
   ```bash
   pytest tests/ --cov=src --cov-report=term-missing
   ```

4. **Commit and push:**
   ```bash
   git add .
   git commit -m "feat: describe your changes"
   git push origin feature/my-feature
   ```

5. **Create a Pull Request**
   - The CI pipeline runs automatically
   - Merge only after all checks pass

---

## 📊 Code Coverage

The project maintains >90% code coverage across all modules:
- **Dictionary module**: Tests for all methods and edge cases
- **Shop module**: Tests for various price scenarios and tax rates
- **Nth Letter module**: Tests for different array lengths and edge cases

Generate a detailed coverage report:
```bash
pytest --cov=src --cov-report=html
```

---

## 🔍 Static Code Analysis

**SonarQube Cloud Integration:**
- Automatic analysis on every push
- Quality gate enforcement
- Issue tracking and reporting
- Security vulnerability scanning

Dashboard: *To be configured*

---

## 📚 Dependencies

### Main Dependencies
- Python 3.8+

### Development Dependencies
- `pytest` - Testing framework
- `pytest-cov` - Coverage plugin for pytest
- `coverage` - Code coverage analysis tool
- *Additional static analysis tools as needed*

Full dependency list: See [requirements.txt](requirements.txt)

---

## 🛠️ Configuration Files

### pytest.ini
Configures pytest behavior, test discovery, and coverage thresholds.

### .coveragerc
Configures code coverage reporting and branch coverage analysis.

### setup.py
Package metadata, version, and dependencies for distribution.

### .github/workflows/ci-cd.yml
GitHub Actions workflow orchestration for all CI/CD stages.

---

## 📝 Coding Standards

This project follows:
- **PEP 8** - Python style guide
- **Type hints** - Function parameter and return type annotations
- **Docstrings** - Comprehensive documentation for all public functions
- **DRY Principle** - Don't Repeat Yourself

Example:
```python
def get_total(prices: dict, items: list, tax_rate: float) -> float:
    """
    Calculate total cost of items with tax application.
    
    Args:
        prices: Dictionary mapping item names to prices
        items: List of item names to purchase
        tax_rate: Tax rate as decimal (e.g., 0.09 for 9%)
    
    Returns:
        Total cost rounded to 2 decimal places
    """
```

---

## 🐛 Troubleshooting

### Tests fail locally but pass in CI
- Ensure Python version matches CI environment (3.8+)
- Clear pytest cache: `pytest --cache-clear`
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

### Coverage below 90%
- Run: `pytest --cov=src --cov-report=term-missing`
- Identify uncovered lines
- Add tests for missing coverage

### Deployment failed
- Check GitHub Actions logs
- Verify environment variables are set correctly
- Ensure deployment credentials are valid

---

## 📄 License

Part of EPAM Professional Development Course. See repository for license details.

---

## 👥 Author

Developed as part of EPAM Python Course - May 2026

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Ensure >90% test coverage
4. Pass all CI/CD checks
5. Submit a pull request

---

## 📞 Support

For questions about:
- **Course content**: Contact EPAM course instructors
- **GitHub Actions**: See [GitHub Actions documentation](https://docs.github.com/en/actions)
- **SonarQube**: See [SonarQube Cloud documentation](https://docs.sonarcloud.io/)
- **Testing**: See [Pytest documentation](https://docs.pytest.org/)

---

**Last Updated:** May 13, 2026  
**Status:** Development in Progress
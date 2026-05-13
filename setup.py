"""
Setup configuration for EPAM Python Task package.

This module configures the package for distribution and installation.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="epam-python-task",
    version="1.0.0",
    author="EPAM Student",
    description="Three Python modules with comprehensive testing and CI/CD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/epam-task-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=["Flask>=2.3"],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "coverage>=6.0",
            "flake8>=4.0",
            "pylint>=2.12",
            "mypy>=0.930",
        ],
    },
)

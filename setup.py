"""
Setup script for NBA Fantasy Dashboard
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="nba-fantasy-dashboard",
    version="1.0.0",
    author="Ezra Dese",
    author_email="your-email@example.com",
    description="A comprehensive NBA Fantasy League Dashboard built with Streamlit and Plotly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ezra-dese/NBA_FantasyDashboard",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "nba-fantasy-dashboard=nba_fantasy_dashboard:main",
        ],
    },
)

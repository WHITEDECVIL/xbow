#!/usr/bin/env python3
"""
XBOW AI Penetration Testing Tool - Setup Configuration
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="xbow-pentest",
    version="1.0.0",
    author="Advanced Penetration Testing Team",
    description="Professional AI-powered penetration testing framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/xbow",
    packages=find_packages(include=["src", "src.*", "xbow", "xbow.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "xbow=xbow:main",
        ],
    },
    include_package_data=True,
)

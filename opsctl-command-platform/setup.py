"""Setup configuration for opsctl."""

from setuptools import setup, find_packages
from opsctl.version import __version__, __description__, __author__


setup(
    name="opsctl",
    version=__version__,
    description=__description__,
    author=__author__,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "opsctl=opsctl.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: System :: Systems Administration",
        "Programming Language :: Python :: 3",
    ],
)

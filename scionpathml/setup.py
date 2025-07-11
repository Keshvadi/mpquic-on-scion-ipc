from setuptools import setup, find_packages

setup(
    name="scionpathml",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "SCIONPathML=scionpathml.cli:main",
        ],
    },
    author="Your Name",
    description="CLI tool to manage SCION path data collection and cron",
)

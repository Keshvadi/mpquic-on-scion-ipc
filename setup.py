from setuptools import setup, find_packages

def print_welcome():
    print("Thank you for installing scionpathml!")
    print(" Run `scionpathml -h` for usage instructions.")

print_welcome()
setup(
    name="scionpathml",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "scionpathml=scionpathml.cli:main",
        ],
    },
    author="Your Name",
    description="CLI tool to manage SCION path data collection and cron",
)
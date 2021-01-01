import pathlib
from setuptools import setup, find_packages
VERSION = '1.0.10'
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="firebaseloginscreen",
    version=VERSION,
    description="Log in screen for Kivy applications using Google Firebase.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Dirk-Sandberg/firebaseloginscreen",
    author="Erik Sandberg",
    author_email="eriks@sandbergsoftware.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["kivymd>=0.104.1"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
    python_requires=">=3.6",
)
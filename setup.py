import io
import os
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup

# Package meta-data.
NAME = "benchmark_utils"
DESCRIPTION = "Utils for benchmark."
URL = "https://github.com/ayasyrev/benchmark_utils"
EMAIL = "a.yasyrev@gmail.com"
AUTHOR = "Andrei Yasyrev"
REQUIRES_PYTHON = ">=3.7.0"

here = os.path.abspath(os.path.dirname(__file__))

# What packages are required for this module to be executed?
try:
    with open(os.path.join(here, "requirements.txt"), encoding="utf-8") as f:
        REQUIRED = f.read().split("\n")
except FileNotFoundError:
    REQUIRED = []

# What packages are optional?
EXTRAS = {"test": ["pytest"]}

# Load the package's __version__ from __init__.py module as a dictionary.
about = {}
with open(os.path.join(here, NAME, "__init__.py")) as f:
    exec(f.read(), about)

VERSION = about['__version__']


def get_test_requirements():
    requirements = ["pytest"]
    if sys.version_info < (3, 3):
        requirements.append("mock")
    return requirements


def get_long_description():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    with io.open(os.path.join(base_dir, "README.md"), encoding="utf-8") as f:
        return f.read()


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Print things in bold."""
        print(s)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution...")
        os.system(f"{sys.executable} setup.py sdist bdist_wheel --universal")

        self.status("Uploading the package to PyPI via Twine...")
        os.system("twine upload dist/*")

        self.status("Pushing git tags...")
        os.system(f"git tag v{VERSION}")
        os.system("git push --tags")

        sys.exit()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    license="MIT",
    url=URL,
    packages=find_packages(exclude=["tests", "docs", "images"]),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    cmdclass={"upload": UploadCommand},
)

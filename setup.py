"""Package setup script.

This script handles everything about package publishing on PyPI.
"""

# Importing libraries
from setuptools import setup, find_packages

# Reading README.md for project description
with open("README.md", "r", encoding='utf-8') as f:
    __long_description__ = f.read()

# Setting up package information
setup(
    name='cloudgeass',
    version='2.0.1',
    author='Thiago Panini',
    author_email='panini.development@gmail.com',
    packages=find_packages(),
    install_requires=[
        "boto3",
        "Faker",
        "pyarrow"
    ],
    license='MIT',
    description="Making your life easier on doing simple tasks in AWS via "
                "boto3",
    long_description=__long_description__,
    long_description_content_type="text/markdown",
    url='https://github.com/ThiagoPanini/cloudgeass',
    keywords='Cloud, AWS, Python, boto3',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: Portuguese (Brazilian)",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires=">=3.0.0"
)

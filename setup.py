"""
MÓDULO: setup.py.

Arquivo de configuração da biblioteca.
"""
# Importando bibliotecas
from setuptools import setup, find_packages

# Lendo README.md
with open("README.md", "r", encoding='utf-8') as f:
    __long_description__ = f.read()

# Criando setup
setup(
    name='cloudgeass',
    version='1.1.0',
    author='Thiago Panini',
    author_email='panini.development@gmail.com',
    packages=find_packages(),
    install_requires=[
        "boto3",
        "pandas",
        "s3fs",
        "pyarrow"
    ],
    license='MIT',
    description='Operações úteis para o uso de serviços AWS',
    long_description=__long_description__,
    long_description_content_type="text/markdown",
    url='https://github.com/ThiagoPanini/cloudgeass',
    keywords='Cloud, AWS, Python',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
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

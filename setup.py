"""
SCRIPT: setup.py.

Arquivo de configuração da biblioteca como um todo
---------------------------------------------------
"""
# Importando bibliotecas
from setuptools import setup, find_packages

# Lendo README.md
with open("README.md", "r", encoding='utf-8') as f:
    __long_description__ = f.read()

# Criando setup
setup(
    name='cloudgeass',
    version='1.0.0',
    author='Thiago Panini',
    author_email='panini.development@gmail.com',
    packages=find_packages(),
    install_requires=[
        'boto3',
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
        "Environment :: Console",
        "Framework :: Jupyter",
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

# Hint: publicando Source Archive (tar.gz) e Built Distribution (.whl)
# python3 setup.py sdist bdist_wheel
# twine check dist/*
# python -m twine upload --skip-existing dist/*

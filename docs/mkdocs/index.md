# Do simple tasks in AWS as simple as possible

<div align="center">
    <br><img src="https://github.com/ThiagoPanini/cloudgeass/blob/main/docs/assets/gifs/logo-animated-intro.gif?raw=true" alt="cloudgeass-animated-intro" width="900" height="400">
</div>


## Overview

Ladies and gentlemen, meet *cloudgeass* as a helpful Python library that is able to improve the way how users run simple tasks in AWS using [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) client and resource.

Built as a boto3 wrapper, the *cloudgeass* package aims to put together some useful functions and methods for common tasks in AWS, such as:

- List all S3 buckets in an AWS account
- Get a report from all objects within a S3 bucket in a pandas DataFrame format
- Get the last date partition from a table stored in S3
- Get a secret string from Secrets Manager
- Launch an EC2 instance
- *and much more*

??? question "Where this name cloudgeass came from?"
    Ha! I though you would ask me that!
    
    The name *cloudgeass* was inspired by a renowned japanese anime called [Code Geass](https://en.wikipedia.org/wiki/Code_Geass). If you don't know this anime, it's a gold chance to watch it for the first time. It will surprise you, believe me!

    So, as a python package that has the purpose to put together some useful features and blocks of code to run in the cloud, *cloudgeass* just sound nice and fits perfectly.


## Quickstart

To start using the package, just install it using [pip](https://pypi.org/project/pip/) (or any other Python dependency management of your choose) as:

```python
pip install cloudgeass
```

You may want to install *cloudgeass* in a [Python virtual environment](https://docs.python.org/3/library/venv.html) to get a good control of your project or application dependencies. If you don't know what this is about, feel free to take a look at this excellent [article from Real Python](https://realpython.com/python-virtual-environments-a-primer/).


## What to find in this doc?

Well, the work is always been done. Until this moment, there are some pages to be highlighted in this doc, such as:

- The [package achitecture](architecture.md) and the [library structure](library-structure.md) pages
- The [official documentation page](./mkdocstrings/s3.md) built with [mkdcostrings](https://mkdocstrings.github.io/)
- The [library demos](./demos/about-demos.md) page with gifs showing some of the most stunning features


## Contact me

- :fontawesome-brands-github: [@ThiagoPanini](https://github.com/ThiagoPanini)
- :fontawesome-brands-linkedin: [Thiago Panini](https://www.linkedin.com/in/thiago-panini/)
- :fontawesome-brands-hashnode: [panini-tech-lab](https://panini.hashnode.dev/)
- :fontawesome-brands-dev: [thiagopanini](https://dev.to/thiagopanini)

import os
from setuptools import find_packages, setup

# Ustaw zmienną środowiskową na false
os.environ['INSTRUCTION_GLUER_ENABLED'] = 'false'

# Read the version from the version.py file
version = {}
with open(os.path.join("swarmcli", "version.py")) as fp:
    exec(fp.read(), version)

setup(
    name="swarmbase-cli",
    version=version["__version__"],
    packages=find_packages(),
    py_modules=['cli', 'migrator'],
    install_requires=[
        "click",
        "requests",
        "pydantic",
        "agency_swarm",
        "langchain_community"
    ],
    entry_points="""
        [console_scripts]
        swarm=cli:cli
    """,
    url="https://github.com/Go-Pomegranate/swarmbase-cli",
    author="swarmbase.ai",
    author_email="eryk.panter@swarmbase.ai",
    description="A CLI for interacting with the swarmbase.ai API",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)

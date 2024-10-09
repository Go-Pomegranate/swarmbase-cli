from setuptools import find_packages, setup

setup(
    name="swarmbase-cli",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "click",
        "requests",
        "pydantic",
    ],
    entry_points="""
        [console_scripts]
        swarm=swarmcli.utils:cli
    """,
    url="https://github.com/Go-Pomegranate/swarmbase-cli",  # Zaktualizuj ten URL
    author="swarmbase.ai",
    author_email="eryk.panter@swarmbase.ai",
    description="A CLI for interacting with the swarmbase.ai API",
    long_description=open('README.md').read(),  # Ensure this file exists and is correctly formatted
    long_description_content_type='text/markdown',  # Change to 'text/x-rst' if using reST
)

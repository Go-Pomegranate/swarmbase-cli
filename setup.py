from setuptools import find_packages, setup

setup(
    name="swarm",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "requests",
    ],
    entry_points="""
        [console_scripts]
        swarm=cli:cli
    """,
    url="https://github.com/yourusername/swarm-cli",  # Zaktualizuj ten URL
    author="swarmbase.ai",
    author_email="eryk.panter@swarmbase.ai",
    description="A CLI for interacting with the swarmbase.ai API",
)

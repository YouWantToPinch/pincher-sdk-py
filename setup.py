from setuptools import setup, find_packages

setup(
    name="pincher_sdk",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.28.1",
        "pyjwt>=2.12.1",
    ],
)

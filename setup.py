from setuptools import setup, find_packages

setup(
    name="compliance_advisor",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai",
        "pydantic",
        "pytest"
    ],
) 
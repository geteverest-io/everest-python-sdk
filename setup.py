from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="everest-api-client",
    version="1.0.0",
    author="Everest",
    author_email="contact@everst.io",
    description="Simple Python client for Everest Logistics API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/everest/everest-python-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    keywords="everest api logistics delivery",
    project_urls={
        "Bug Reports": "https://github.com/everest/everest-python-sdk/issues",
        "Source": "https://github.com/everest/everest-python-sdk",
    },
)

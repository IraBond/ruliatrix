from setuptools import setup, find_packages

setup(
    name="ruliatrix",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "sympy>=1.8",
        "matplotlib>=3.4.0",
        "networkx>=2.6.0",
        "plotly>=5.3.0",
    ],
    author="Ruliatrix Contributors",
    author_email="info@ruliatrix.org",
    description="A symbolic computation framework based on PEGFRA",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ruliatrix/ruliatrix",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.8",
)

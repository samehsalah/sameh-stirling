from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="sameh-stirling",
    version="0.0.6",  
    author="Sameh Salah",
    author_email="samehsalah83@gmail.com",
    description="A library for creating Dash interactive charts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samehsalah/sameh-stirling",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "dash",
        "dash_bootstrap_components",
        "pandas",
        "plotly",
        "matplotlib"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
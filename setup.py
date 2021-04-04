import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="delta-dx",
    version="0.0.1",
    author="MrRhuezzler",
    author_email="anonymouspyro369@gmail.com",
    description="A Python Symbolic Differentiation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MrRhuezzler/delta",
    project_urls={
        "Bug Tracker": "https://github.com/MrRhuezzler/delta/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)
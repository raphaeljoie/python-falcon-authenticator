import setuptools

with open("README.md", "r") as fh:
    description = fh.readline()
    long_description = description + fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="python_falcon_authenticator",
    version="0.1.3",
    author="Raphaël Joie",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raphaeljoie/python-falcon-authenticator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
)

# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/kivi.py
# License: MIT License

import os, json
from setuptools import setup, find_packages


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Readme & Reqs
reques = (
    [r.strip() for r in open("requirements.txt", encoding="utf-8").readlines()]
    if os.path.isfile("requirements.txt")
    else ["python-dateutil"]
)

# Description
if os.path.isfile("README.md"):
    with open(("README.md"), encoding="utf-8") as readmeh:
        lg_desc = readmeh.read()
else:
    lg_desc = "A simple key-value database that uses json files to store data."


# kivi.py version
def get_version():
    with open("assests/version.json", "r", encoding="utf-8") as jsn_f:
        ver = json.load(jsn_f)
        return ver["version"]


kversion = get_version()


setup(
    name="kivi.py",
    version=kversion,
    description="A simple key-value database",
    url="https://github.com/Itz-fork/kivi.py",
    author="Itz-fork",
    author_email="git.itzfork@gmail.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    download_url=f"https://github.com/Itz-fork/kivi.py/releases/tag/kivi.py-pypi-{kversion}",
    keywords=["databse", "key-value", "key-value database", "kivi.py"],
    long_description=lg_desc,
    long_description_content_type="text/markdown",
    install_requires=reques,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

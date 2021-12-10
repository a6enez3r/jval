"""
jval
-------------

validate a JSON object against a schema
"""
from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="jval",
    version="0.0.1",
    description="validate a JSON object against a schema",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/abmamo/jval",
    author="Abenezer Mamo",
    author_email="contact@abmamo.com",
    license="MIT",
    packages=find_packages(exclude=("tests",)),
    zip_safe=False,
)

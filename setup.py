from setuptools import setup, find_packages

# read the contents of README file
from os import path
# get current file directory
this_directory = path.abspath(path.dirname(__file__))
# open README with UTF-8 encoding
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    # read README
    long_description = f.read()

setup(
      name='validateJSON',
      version='0.0.5',
      description='recursively validate a given JSON object against a schema',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/abmamo/validateJSON',
      author='Abenezer Mamo',
      author_email='contact@abmamo.com',
      license='MIT',
      packages=find_packages(exclude=("tests",)),
      install_requires=["setuptools==50.3.2"],
      zip_safe=False
)

from setuptools import setup, find_packages

setup(
      name='validateJSON',
      version='0.0.1',
      description='recursively validate a given JSON object contains expected keys & types',
      url='http://github.com/abmamo/validateJSON',
      author='Abenezer Mamo',
      author_email='contact@abmamo.com',
      license='MIT',
      packages=find_packages(exclude=("tests",)),
      install_requires=["setuptools==50.3.2"],
      zip_safe=False
)
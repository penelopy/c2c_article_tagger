# setup.py
from setuptools import setup, find_packages

version = '0.0.1'

setup(name='article_tagger',
      version=version,
      description='article_tagger_app',
      install_requires=['routes', 'sqlalchemy', 'mysql-python', 'flask'],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
)
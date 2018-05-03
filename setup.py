from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'dependencies.txt')) as f:
    dependencies = f.readlines()

setup(name='forecast',
      version='0.1',
      description='high level forecast library for python',
      url='http://github.com/DavisTownsend/forecastt',
      author='Davis Townsend',
      author_email='dtownsend@ea.com',
      license='MIT',
      packages=['forecast'],
      install_requires=dependencies,
      zip_safe=False)

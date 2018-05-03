from setuptools import setup

setup(name='forecast',
      version='0.1',
      description='high level forecast library for python',
      url='http://github.com/DavisTownsend/forecastt',
      author='Davis Townsend',
      author_email='dtownsend@ea.com',
      license='MIT',
      packages=['forecast'],
      install_requires=['dask','distributed','rpy2','pystan','fbprophet','plotly']
      ,
      zip_safe=False)

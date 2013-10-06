from setuptools import setup, find_packages

setup(name='orangery',
      version='0.1',
      description='Surveyed cross-section analysis',
      url='http://github.com/mrahnis/orangery',
      license='BSD',
      packages=find_packages(),
      install_requires=[
          'numpy','pandas','matplotlib','shapely'
      ],
      zip_safe=False)
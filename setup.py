from os import path
from setuptools import setup, find_packages


for line in open('orangery/__init__.py', 'r'):
    if line.find("__version__") >= 0:
        version = line.split("=")[1].strip()
        version = version.strip('"')
        version = version.strip("'")
        continue

with open('VERSION.txt', 'w') as fp:
    fp.write(version)

current_directory = path.abspath(path.dirname(__file__))
with open(path.join(current_directory, 'README.rst'), 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(name='orangery',
      version=version,
      author='Michael Rahnis',
      author_email='mike@topomatrix.com',
      description='Python library to support analysis of topographic cross-sections',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      url='http://github.com/mrahnis/orangery',
      license='BSD',
      packages=find_packages(),
      install_requires=[
          'numpy','pandas','matplotlib','shapely','click', 'opusxml'
      ],
      entry_points='''
          [console_scripts]
          orangery=orangery.cli.orangery:cli

          [orangery.subcommands]
          adjust=orangery.cli.adjust:adjust
          geodetic=orangery.cli.geodetic:geodetic
          section=orangery.cli.section:section
          cutfill=orangery.cli.cutfill:cutfill
          segment=orangery.cli.segment:segment
          info=orangery.cli.info:info
      ''',
      keywords='cross-section, topography, survey, plotting',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering :: GIS'
      ])

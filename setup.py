from setuptools import setup, find_packages
import versioneer


with open('README.rst', 'r', encoding='utf-8') as f:
    long_description = f.read()
with open("requirements.txt", "r") as f:
    requirements = [line.strip() for line in f]

setup(name='orangery',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      author='Michael Rahnis',
      author_email='mike@topomatrix.com',
      description='Python library to support analysis of topographic cross-sections',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      url='http://github.com/mrahnis/orangery',
      license='BSD',
      packages=find_packages(),
      install_requires=requirements,
      entry_points='''
          [console_scripts]
          orangery=orangery.cli.orangery:cli

          [orangery.subcommands]
          adjust=orangery.cli.adjust:adjust
          cutfill=orangery.cli.cutfill:cutfill
          geodetic=orangery.cli.geodetic:geodetic
          info=orangery.cli.info:info
          section=orangery.cli.section:section
          segment=orangery.cli.segment:segment
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

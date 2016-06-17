from setuptools import setup, find_packages


# Parse the version from the shapely module
for line in open('orangery/__init__.py', 'r'):
    if line.find("__version__") >= 0:
        version = line.split("=")[1].strip()
        version = version.strip('"')
        version = version.strip("'")
        continue

#open('VERSION.txt', 'wb').write(bytes(version, 'UTF-8'))
with open('VERSION.txt', 'w') as fp:
    fp.write(version)


setup(name='orangery',
	version=version,
	author='Michael Rahnis',
	author_email='michael.rahnis@fandm.edu',
	description='Python library to support analysis of topographic cross-sections',
	url='http://github.com/mrahnis/orangery',
	license='BSD',
	packages=find_packages(),
	install_requires=[
		'numpy','pandas','matplotlib','shapely','click', 'opusxml'
	],
	entry_points='''
		[console_scripts]
		adjust=orangery.cli.adjust:cli
		geodetic=orangery.cli.geodetic:cli
		cutfill=orangery.cli.cutfill:cli
	''',
	keywords='cross-section, topography, survey, plotting',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'License :: OSI Approved :: BSD License',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Topic :: Scientific/Engineering :: GIS'
	]
)


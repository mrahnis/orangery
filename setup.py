from setuptools import setup, find_packages

setup(name='orangery',
	version='0.2.0',
	author='Michael Rahnis',
	author_email='michael.rahnis@fandm.edu',
	description='Python library to support analysis of topographic cross-sections',
	url='http://github.com/mrahnis/orangery',
	license='BSD',
	packages=find_packages(),
	install_requires=[
		'numpy','pandas','matplotlib','shapely'
	],
	keywords='cross-section, topography, survey, plotting',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'License :: OSI Approved :: BSD License',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.7',
		'Topic :: Scientific/Engineering :: GIS'
	]
)


========
Orangery
========

Orangery is a Python library to support analysis of topographic cross-sections, particularly on stream channels. The intent is to enable the user to write simple scripts that operate on CSV data exported from a survey data collector.

.. image:: https://travis-ci.org/mrahnis/orangery.svg?branch=master
    :target: https://travis-ci.org/mrahnis/orangery

.. image:: https://ci.appveyor.com/api/projects/status/github/mrahnis/orangery?svg=true
	:target: https://ci.appveyor.com/api/projects/status/github/mrahnis/orangery?svg=true

.. image:: https://readthedocs.org/projects/orangery/badge/?version=latest
	:target: http://orangery.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Status

Orangery was initially a single script that allowed me to segregate, by grain size, changed areas on repeat topographic cross-sections. It can produce output plots like the one below.

.. image:: https://lh3.googleusercontent.com/-3BBypwcOuqQ/U2GP63BYFII/AAAAAAAABNs/ubaKDHXSqjQ/w800-h344-no/figure_1.png
	:width: 800
	:height: 344

Dependencies
============

Orangery 0.4.1 depends on:

* `Python 2.7 or 3.x`_
* NumPy_
* pandas_
* matplotlib_
* Shapely_

Installation
============

To install from the Python Package Index:

	$pip install orangery

To install from the source distribution execute the setup script in the orangery directory:

	$python setup.py install

Windows users just getting started may choose to install a Python distribution to obtain the requirements:

* Install Anaconda from `Continuum Analytics`_ or Canopy from `Enthought`_
* Install the appropriate `Shapely binary`_
* Install Orangery as shown above, or install the .msi installer from the GitHub project `release page`_

Examples
========

The example scripts may be run like so:

	$python plots.py

License
=======

BSD

Documentation
=============

Latest `html`_

.. _`Python 2.7 or 3.x`: http://www.python.org
.. _NumPy: http://www.numpy.org
.. _pandas: http://pandas.pydata.org
.. _matplotlib: http://matplotlib.org
.. _Shapely: https://github.com/Toblerity/Shapely

.. _Continuum Analytics: http://continuum.io/
.. _Enthought: http://www.enthought.com
.. _Shapely binary: https://pypi.python.org/pypi/Shapely
.. _release page: https://github.com/mrahnis/orangery/releases

.. _html: http://orangery.readthedocs.org/en/latest/
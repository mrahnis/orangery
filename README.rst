========
Orangery
========

Orangery is a Python library to support analysis of topographic cross-sections, particularly on stream channels. The intent is to enable the user to write simple scripts that operate on CSV data exported from a survey data collector.

.. image:: https://github.com/mrahnis/orangery/workflows/Python%20package/badge.svg
    :target: https://github.com/mrahnis/orangery/actions?query=workflow%3A%22Python+package%22
    :alt: Python Package

.. image:: https://github.com/mrahnis/orangery/workflows/Conda%20package/badge.svg
    :target: https://github.com/mrahnis/orangery/actions?query=workflow%3A%22Conda+package%22
    :alt: Conda Package

.. image:: https://readthedocs.org/projects/orangery/badge/?version=latest
    :target: http://orangery.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Orangery was initially a single script that allowed me to segregate, by grain size, changed areas on repeat topographic cross-sections. It can produce output plots like the one below.

.. image:: https://lh3.googleusercontent.com/-3BBypwcOuqQ/U2GP63BYFII/AAAAAAAABNs/ubaKDHXSqjQ/w800-h344-no/figure_1.png
    :width: 800
    :height: 344

Installation
============

.. image:: https://img.shields.io/pypi/v/orangery.svg
    :target: https://pypi.org/project/orangery/

.. image:: https://anaconda.org/mrahnis/orangery/badges/version.svg
    :target: https://anaconda.org/mrahnis/orangery

To install from the Python Package Index:

.. code:: console

    $pip install orangery

To install from the source distribution execute the setup script in the orangery directory:

.. code:: console

    $python setup.py install

To install from Anaconda Cloud:

If you are starting from scratch the first thing to do is install the Anaconda Python distribution, add the necessary channels to obtain the dependencies and install orangery.

.. code:: console

    $conda config --append channels conda-forge
    $conda config --append channels mrahnis
    $conda install orangery

To install from the source distribution:

Execute the setup script in the orangery directory:

.. code:: console

    $python setup.py install

Examples
========

The example scripts may be run like so:

.. code:: console

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
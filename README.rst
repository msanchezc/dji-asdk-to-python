=========================
DJI Android SDK to Python
=========================


.. image:: https://img.shields.io/pypi/v/dji_asdk_to_python.svg
        :target: https://pypi.python.org/pypi/dji_asdk_to_python

.. image:: https://img.shields.io/travis/PSBPOSAS/dji-asdk-to-python.svg
        :target: https://travis-ci.org/PSBPOSAS/dji-asdk-to-python

.. image:: https://readthedocs.org/projects/dji-asdk-to-python/badge/?version=latest
        :target: https://dji-asdk-to-python.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/PSBPOSAS/dji-asdk-to-python/shield.svg
     :target: https://pyup.io/repos/github/PSBPOSAS/dji-asdk-to-python/
     :alt: Updates



Control your DJI drone compatible with DJI Android SDK through Python


* Free software: BSD license
* Documentation: https://dji-asdk-to-python.readthedocs.io.


Features
--------

* Control your aircraft with virtual sticks
* Perform waypoint missions
* Get real time aircraft video streaming using OpenCV and GStreamer
* Precision landing using Aruco markers


Dependencies
------------

Gstreamer
~~~~~~~~~
* https://pygobject.readthedocs.io/en/latest/getting_started.html#ubuntu-logo-ubuntu-debian-logo-debian
* https://gstreamer.freedesktop.org/documentation/installing/on-linux.html?gi-language=c#install-gstreamer-on-fedora

.. code:: bash

    $ sudo apt-get update
    $ sudo apt install -y libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev python3.8-dev gir1.2-gtk-3.0 
    $ sudo apt-get install -y libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio

Install
-------

Install PyPI
~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ pip install dji-asdk-to-python


Install from master
~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ pip install git+https://github.com/PSBPOSAS/dji-asdk-to-python.git

Install specific release example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ pip install git+https://github.com/PSBPOSAS/dji-asdk-to-python.git@v0.1.0

Uninstall
---------

.. code:: bash

    $ pip uninstall dji-asdk-to-python

Usage example
-------------

.. code:: python

    import time
    from dji_asdk_to_python.products.aircraft import Aircraft
    drone = Aircraft("android_device_ip")
    fc = drone.getFlightController()
    fc.startTakeoff()
    time.sleep(10)
    fc.startLanding()

Generate Documentation
----------------------

This wil generate a HTML version of your ``docs/`` and open it in a
browser.

.. code:: bash

    $ make docs



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

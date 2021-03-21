Introduction
============

This module can be used to solve optimization tasks.
For instance, you could use this module to tune the hyper-parameters of a neural
network or a decision tree.

Getting started
---------------

Installation
^^^^^^^^^^^^

.. highlight:: shell

To install the package, simply run::

   git clone https://github.com/Pear-Bio/Evolutionary_Algorithm
   cd Evolutionary_Algorithm

Then, set up a virtual environment like so::

   python3 -m venv ./venv

Activate your virtual environment::

   source venv/bin/activate

And install the dependencies::

   pip3 install -r requirements.txt

Using the package
^^^^^^^^^^^^^^^^^

First go to the right directory::

   cd Evolutionary_Algorithm/src

Then, run the code over a z-stack folder as follows::

   python3 train_ea.py

You can change the parameters of the optimization task easily by making the
changes in the config.py file.

*This section is incomplete*

Documentation
-------------

You can consult our documentation *UPDATE* `here <https://automatic-doodle-3d4f5025.pages.github.io/>`_.

Our documentation is automatically generated using sphinx-autodoc. This means that **all modifications** to the code must follow `google-style docstring syntax <https://google.github.io/styleguide/pyguide.html>`_.

Before pushing anything to this repository, please complete the following checks:


* Go to the root of the repository
* Run the following command: ``run_tests.sh Evolutionary_Algorithm``
* Inspect the generated reports in ``Evolutionary_Algorithm/tests``
* Solve all errors and warning in accordance to the google-style documentation referenced above.
* Additionally, please ensure the doctests run correctly with no error.

The above steps perform some syntax checks using PyLint, as well as some type checks using PyType. These tests are important to generate a clean documentation and to keep maintainable code, so make sure your code passes all tests.
Once this is done, you can push your changes to this repository and the documentation will be automatically modified (for early versions, don't forget to add the new .rst files).

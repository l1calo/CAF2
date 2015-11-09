.. CAF documentation master file, created by
   sphinx-quickstart on Mon Nov  9 08:39:08 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to L1Calo CAF's documentation!
===============================

Standalone tools
----------------

Tools that don't use database for storing results, can be run  from the command line or from
other python script.

.. toctree::
  :maxdepth: 2

  api/caf_find.rst
  api/caf_files.rst
  api/caf_prepare.rst
  api/caf_submit.rst

Database tools
--------------

Tools that use database to save  runs information and jobs results. These tools
are based on the `Standalone tools` mentioned above

.. toctree::
  :maxdepth: 2

  api/settings.rst
  api/models.rst
  api/caf_db_find.rst
  api/caf_db_prepare.rst
  api/caf_db_submit.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

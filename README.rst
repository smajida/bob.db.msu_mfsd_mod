.. vim: set fileencoding=utf-8 :
.. Ivana Chingovska <ivana.chingovska@idiap.ch>
.. Thu  9 Apr 12:24:28 CEST 2015

.. image:: http://img.shields.io/badge/docs-stable-yellow.png
   :target: http://pythonhosted.org/bob.db.msu_mfsd_mod/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.png
   :target: https://www.idiap.ch/software/bob/docs/latest/bioidiap/bob.db.msu_mfsd_mod/master/index.html
.. image:: https://travis-ci.org/bioidiap/bob.db.msu_mfsd_mod.svg?branch=master
   :target: https://travis-ci.org/bioidiap/bob.db.msu_mfsd_mod
.. image:: https://coveralls.io/repos/bioidiap/bob.db.msu_mfsd_mod/badge.svg?branch=master
   :target: https://coveralls.io/r/bioidiap/bob.db.msu_mfsd_mod
.. image:: https://img.shields.io/badge/github-master-0000c0.png
   :target: https://github.com/bioidiap/bob.db.msu_mfsd_mod/tree/master
.. image:: http://img.shields.io/pypi/v/bob.db.msu_mfsd_mod.png
   :target: https://pypi.python.org/pypi/bob.db.msu_mfsd_mod
.. image:: http://img.shields.io/pypi/dm/bob.db.msu_mfsd_mod.png
   :target: https://pypi.python.org/pypi/bob.db.msu_mfsd_mod

====================================================
 MSU Mobile Face Spoofing Database Interface for Bob
====================================================

The MSU-MFSD database is a spoofing attack database which consists of printed attacks, as well as replay attacks recorded with mobile phone and tablet. The acquisition devices are lap-top and Android phone.

This package contains the Bob_ accessor methods to use the DB directly from python. When querying the database, if you specify fold=0 in the Database.objects() method, the files will be returned using the original protocol provided with the database. Note that this protocol does not contain development set.

To compensate for the absense of development data, we created a custom protocol, consisting of 5 folds for 5-fold cross validation. The folds are created by randomly selecting identities to belong to the training and development set. Note that the clients that belong in the test set in the custom protocol are the same for all the 5 folds, but are different from the original protocol. If you want to work with this custom protocol, specify 0 < fold <= 5 in the Database.objects() method.

The actual raw data for `MSU MFSD`_ database should be downloaded from the original URL.

Reference::

  D. Wen, A. K. Jain and H. Han: "Face Spoof Detection with Image Distortion Analysis", In  IEEE Trans. Information Forensic and Security, 2015.


Installation
------------

To install this package -- alone or together with other `Packages of Bob <https://github.com/idiap/bob/wiki/Packages>`_ -- please read the `Installation Instructions <https://github.com/idiap/bob/wiki/Installation>`_.
For Bob_ to be able to work properly, some dependent packages are required to be installed.
Please make sure that you have read the `Dependencies <https://github.com/idiap/bob/wiki/Dependencies>`_ for your operating system.


Using the package
-----------------

After instalation of the package, go to the console and type::

  $ ./bin/sphinx-build doc sphinx

Now, the full documentation of the package, including a User Guide, will be availabe in ``sphinx/index.html``.

Problems
--------

In case of problems, please contact ivana.chingovska@idiap.ch


.. _bob: https://www.idiap.ch/software/bob
.. _msu mfsd: http://www.cse.msu.edu/rgroups/biometrics/Publications/Databases/MSUMobileFaceSpoofing/index.htm


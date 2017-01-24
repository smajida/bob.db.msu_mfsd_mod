.. vim: set fileencoding=utf-8 :
.. @author: Manuel Guenther <Manuel.Guenther@idiap.ch>
.. @date:   Thu Dec  6 12:28:25 CET 2012

==============
 User's Guide
==============

This package contains the Bob_ accessor methods for using the database directly
from python. When querying the database, if you specify ``fold=0`` in the
:py:meth:`~bob.db.msu_mfsd_mod.Database.objects` method, the files will be
returned using the original protocol provided with the database. Note that this
protocol does not contain development set.

To compensate for the absence of development data, we created a custom protocol,
consisting of 5 folds for 5-fold cross validation. The folds are created by
randomly selecting identities to belong to the training and development set.
Note that the clients that belong in the test set in the custom protocol are the
same for all the 5 folds, but are different from the original protocol. If you
want to work with this custom protocol, specify 0 < fold <= 5 in the
:py:meth:`~bob.db.msu_mfsd_mod.Database.objects` method.

.. _bob: https://www.idiap.ch/software/bob

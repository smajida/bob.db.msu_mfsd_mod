#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.dos.anjos@gmail.com>
# Tue 17 May 13:58:09 2011

"""This module provides the Dataset interface allowing the user to query the
replay attack database in the most obvious ways.
"""

import os
from bob.db.base import utils, Database
from .models import *
from .driver import Interface
from six import string_types


INFO = Interface()

SQLITE_FILE = INFO.files()[0]


class Database(Database):
  """The dataset class opens and maintains a connection opened to the Database.

  It provides many different ways to probe for the characteristics of the data
  and for the data itself inside the database.
  """

  def __init__(self):
    # opens a session to the database - keep it open until the end
    self.connect()
    super(Database, self).__init__()

  def __del__(self):
    """Releases the opened file descriptor"""
    if self.session:
      try:
        # Since the dispose function re-creates a pool
        #   which might fail in some conditions, e.g., when this destructor is called during the exit of the python interpreter
        self.session.close()
        self.session.bind.dispose()
      except TypeError:
        # ... I can just ignore the according exception...
        pass
      except AttributeError:
        pass

  def connect(self):
    """Tries connecting or re-connecting to the database"""
    
    #print(SQLITE_FILE)
    
    if not os.path.exists(SQLITE_FILE):
      self.session = None

    else:
      self.session = utils.session_try_readonly(INFO.type(), SQLITE_FILE)

  def is_valid(self):
    """Returns if a valid session has been opened for reading the database"""

    return self.session is not None

  def assert_validity(self):
    """Raise a RuntimeError if the database backend is not available"""

    if not self.is_valid():
      raise RuntimeError("Database '%s' cannot be found at expected location '%s'. Create it and then try re-connecting using Database.connect()" % (INFO.name(), SQLITE_FILE))



  def objects(self, quality=File.quality_choices, 
                    instrument=File.instrument_choices,
#                    protocol='grandtest', 
                    fold='fold1', 
                    group=Client.group_choices, 
                    cls= File.presentation_choices):
    """Returns a list of unique :py:class:`.File` objects for the specific query by the user.

    Keyword parameters:

    quality
      One of the valid support types as returned by file_qualities() or all,
      as a tuple.  If you set this parameter to an empty string or the value
      None, we use reset it to the default, which is to get all.

    instrument
      Specify the attack-instruments of interest ('video_hd', 'video_mobile', 'print').
      Several instruments may be specified together, as a tuple.
      If the parameter is not specified, or is specified as an empty string or as the
      value None, then the parameter value is considered to be the set of all instruments.

    group
      One of the subgroups of data ('train', 'devel', 'test') as returned by groups() 
      or any combination of them in a tuple. If set to an empty string or the value None, 
      it is reset to the default which is to get all subgroups.

    cls
      Either "attack", or "real", or both (in a tuple). Defines the presentation
      of the data to be retrieved.  If parameter is set to an empty string or 
      the value None, the value is reset to the default: ("real", "attack").

    fold:
      One of 5 folds supported ('fold1', 'fold2', 'fold3', 'fold4', 'fold5').
      If not specified, 'fold1' is the default value used. If the parameter is
      set to empty string, of the value None, its value is reset to the default.
      If desired, several folds may be specified together, as a tuple.


#    protocol --NOT USED FOR NOW. THIS COMMENT WILL BE REMOVED.
#      The protocol for the attack. One of the ones returned by protocols(). If
#      you set this parameter to an empty string or the value None, we use reset
#      it to the default, "grandtest".

    Returns: A list of :py:class:`.File` objects.
    """

    self.assert_validity()

    def check_validity(l, paramType, valid, default):
      """Checks validity of user input data against a set of valid values"""
      if not l:
        return default
      elif not isinstance(l, (tuple, list)):
        return check_validity((l,), paramType, valid, default)
      for k in l:
        if k not in valid:
          raise RuntimeError('Invalid %s "%s". Valid values are %s, or lists/tuples of those' % (paramType, k, valid))
      return l

    def check_fold_validity(f, valid, default):
      """Checks validity of user input parameter 'fold' against a set of valid values"""
      if not f:
        return default
      elif isinstance(f, string_types):
        if f not in valid:
          raise RuntimeError('Invalid fold-parameter: "%s". Valid values are *exactly one* of the strings: %s' % (f, valid))
      else:
        raise RuntimeError('Invalid type for fold-parameter: "%s". It should be a single string from the set: %s.' % (f, valid))

      return f


    # checks if 'quality' param is valid
    VALID_QUALITIES = self.qualities()
    quality = check_validity(quality, "quality", VALID_QUALITIES, VALID_QUALITIES)

    # check if 'instrument' set are valid
    VALID_INSTRUMENTS = self.attack_instruments()
    instrument = check_validity(instrument, "attack_instrument", VALID_INSTRUMENTS, VALID_INSTRUMENTS)

    # checks if the 'fold' param. is valid
    VALID_FOLDS = self.folds()
    fold = check_fold_validity(fold, VALID_FOLDS, 'fold1')

    # check if groups set are valid
    VALID_GROUPS = self.groups()
    group = check_validity(group, "group", VALID_GROUPS, VALID_GROUPS)

    # by default, do NOT grab enrollment data from the database
    VALID_PRESENTATIONS = self.presentation_classes() #('real', 'attack')
    cls = check_validity(cls, "presentation", VALID_PRESENTATIONS, ('real', 'attack'))


#    # check protocol validity
#    if not protocol:
#      protocol = 'grandtest'  # default
#    VALID_PROTOCOLS = [k.name for k in self.protocols()]
#    protocol = check_validity(protocol, "protocol", VALID_PROTOCOLS, ('grandtest',))
#    # checks client identity validity
#    VALID_CLIENTS = [k.id for k in self.clients()]
#    clients = check_validity(clients, "client", VALID_CLIENTS, None)


    # now query the database
    retval = []

#    q = self.session.query(File, Client.id, Client.client_fold1).join(Client)
    q = self.session.query(File, Client).join(Client)

    if cls: #presentation: real or attack
      q = q.filter(File.cls.in_(cls))

    if fold=='fold1':

      q = q.filter(Client.client_fold1.in_(group))
    elif fold=='fold2':
      q = q.filter(Client.client_fold2.in_(group))
    elif fold=='fold3':
      q = q.filter(Client.client_fold3.in_(group))
    elif fold=='fold4':
      q = q.filter(Client.client_fold4.in_(group))
    elif fold=='fold5':
      q = q.filter(Client.client_fold5.in_(group))
    else:
      raise RuntimeError('Invalid Fold: "%s". Valid values are one string of %s' % (fold, VALID_FOLDS))

    if quality:
      q = q.filter(File.quality.in_(quality))

#    q = q.filter(Protocol.name.in_(protocol))
    q = q.order_by(File.cls.desc()).order_by(Client.id) # first order by 'real' or 'attack' (desc() puts the 'reals' first), 
							# and within each presentation, order by client-Id.
    retval = list(q)

    files = []
    for r in retval:
        f = r[0]
        c = r[1]

        f.client_id = c.id
        f.client_fold = c.client_fold1
        files.append(f)

    return files

#  def files(self, directory=None, extension=None, **object_query):
#    """Returns a set of filenames for the specific query by the user.
#
#    .. deprecated:: 1.1.0
#
#      This function is *deprecated*, use :py:meth:`.Database.objects` instead.
#
#    Keyword Parameters:
#
#    directory
#      A directory name that will be prepended to the final filepath returned
#
#    extension
#      A filename extension that will be appended to the final filepath returned
#
#    object_query
#      All remaining arguments are passed to :py:meth:`.Database.objects`
#      untouched. Please check the documentation for such method for more
#      details.
#
#    Returns: A dictionary containing the resolved filenames considering all
#    the filtering criteria. The keys of the dictionary are unique identities
#    for each file in the replay attack database. Conserve these numbers if you
#    wish to save processing results later on.
#    """
#
#    import warnings
#    warnings.warn("The method Database.files() is deprecated, use Database.objects() for more powerful object retrieval", DeprecationWarning)
#
#    return dict([(k.id, k.make_path(directory, extension)) for k in self.objects(**object_query)])

#  def clients(self):
#    """Returns an iterable with all known clients"""
#
#    self.assert_validity()
#    return list(self.session.query(Client))

#  def has_client_id(self, id):
#    """Returns True if we have a client with a certain integer identifier"""
#
#    self.assert_validity()
#    return self.session.query(Client).filter(Client.id == id).count() != 0

#  def protocols(self):
#    """Returns all protocol objects.
#    """
#
#    self.assert_validity()
#    return list(self.session.query(Protocol))

#  def has_protocol(self, name):
#    """Tells if a certain protocol is available"""
#
#    self.assert_validity()
#    return self.session.query(Protocol).filter(Protocol.name == name).count() != 0


#  def protocol(self, name):
#    """Returns the protocol object in the database given a certain name. Raises
#    an error if that does not exist."""
#
#    self.assert_validity()
#    return self.session.query(Protocol).filter(Protocol.name == name).one()


  def groups(self):
    """Returns the names of all registered groups"""
    return Client.group_choices

  def folds(self):
    """Returns list of supported folds in the database"""
    return Client.fold_choices

  def qualities(self):
    """Returns the available video-qualities (of sampling devices) in the database"""
    return File.quality_choices

  def attack_instruments(self):
    """Returns attack devices available in the database"""
    return File.instrument_choices

  def presentation_classes(self):
    """Returns the kinds of presentation (real or attack) available in the database"""
    return File.presentation_choices



  def paths(self, ids, prefix='', suffix=''):
    """Returns a full file paths considering particular file ids, a given
    directory and an extension

    Keyword Parameters:

    id
      The ids of the object in the database table "file". This object should be
      a python iterable (such as a tuple or list).

    prefix
      The bit of path to be prepended to the filename stem

    suffix
      The extension determines the suffix that will be appended to the filename
      stem.

    Returns a list (that may be empty) of the fully constructed paths given the
    file ids.
    """

    self.assert_validity()

    fobj = self.session.query(File).filter(File.id.in_(ids))
    retval = []
    for p in ids:
      retval.extend([k.make_path(prefix, suffix) for k in fobj if k.id == p])
    return retval

#  def reverse(self, paths):
#    """Reverses the lookup: from certain stems, returning file ids
#
#    Keyword Parameters:
#
#    paths
#      The filename stems I'll query for. This object should be a python
#      iterable (such as a tuple or list)
#
#    Returns a list (that may be empty).
#    """
#
#    self.assert_validity()
#
#    fobj = self.session.query(File).filter(File.path.in_(paths))
#    for p in paths:
#      retval.extend([k.id for k in fobj if k.path == p])
#    return retval

#  def save_one(self, id, obj, directory, extension):
#    """Saves a single object supporting the bob save() protocol.
#
#    .. deprecated:: 1.1.0
#
#      This function is *deprecated*, use :py:meth:`.File.save()` instead.
#
#    This method will call save() on the the given object using the correct
#    database filename stem for the given id.
#
#    Keyword Parameters:
#
#    id
#      The id of the object in the database table "file".
#
#    obj
#      The object that needs to be saved, respecting the bob save() protocol.
#
#    directory
#      This is the base directory to which you want to save the data. The
#      directory is tested for existence and created if it is not there with
#      os.makedirs()
#
#    extension
#      The extension determines the way each of the arrays will be saved.
#    """
#
#    import warnings
#    warnings.warn("The method Database.save_one() is deprecated, use the File object directly as returned by Database.objects() for more powerful object manipulation.", DeprecationWarning)
#
#    self.assert_validity()
#
#    fobj = self.session.query(File).filter_by(id=id).one()
#
#    fullpath = os.path.join(directory, str(fobj.path) + extension)
#    fulldir = os.path.dirname(fullpath)
#    utils.makedirs_safe(fulldir)
#
#    from bob.io.base import save
#
#    save(obj, fullpath)

#  def save(self, data, directory, extension):
#    """This method takes a dictionary of blitz arrays or bob.database.Array's
#    and saves the data respecting the original arrangement as returned by
#    files().
#
#    .. deprecated:: 1.1.0
#
#      This function is *deprecated*, use :py:meth:`.File.save()` instead.
#
#    Keyword Parameters:
#
#    data
#      A dictionary with two keys 'real' and 'attack', each containing a
#      dictionary mapping file ids from the original database to an object that
#      supports the bob "save()" protocol.
#
#    directory
#      This is the base directory to which you want to save the data. The
#      directory is tested for existence and created if it is not there with
#      os.makedirs()
#
#    extension
#      The extension determines the way each of the arrays will be saved.
#    """
#
#    import warnings
#    warnings.warn("The method Database.save() is deprecated, use the File object directly as returned by Database.objects() for more powerful object manipulation.", DeprecationWarning)
#
#    for key, value in data:
#      self.save_one(key, value, directory, extension)

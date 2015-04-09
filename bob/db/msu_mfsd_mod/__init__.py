#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Ivana Chingovska <ivana.chingovska@idiap.ch>
# Tue 10 Mar 16:37:29 CET 2015

"""
The MSU Mobile Face Spoofing Database is a spoofing attack database which consists of real accesses and attacks taken with two different devices: lap-top and smartphone. There are three types of attacks: HD video replay, mobile video replay and print attacks.

When querying the database, if you specify fold=0 in the Database.objects() method, the files will be returned using the original protocol provided with the database. Note that this protocol does not contain development set.

To compensate for the absense of development data, we created a custom protocol, consisting of 5 folds for 5-fold cross validation. The folds are created by randomly selecting identities to belong to the training and development set. Note that the clients that belong in the test set in the custom protocol are the same for all the 5 folds, but are different from the original protocol. If you want to work with this custom protocol, specify 0 < fold <= 5 in the Database.objects() method.

References:

  1. D. Wen, H. Han, A. K. Jain: "Face Spoof Detection with Image Distortion Analysis", In Transactions of Information Forensics and Security, 2015."""

import os
import six
import numpy
from bob.db.base import utils
from .models import *

class Database(object):

  def __init__(self, foldsdir=None):

    from .driver import Interface
    self.info = Interface()
    self.groups = ('train', 'devel', 'test')
    self.classes = ('attack', 'real')
    self.qualities = ('laptop', 'mobile') # the capturing device
    self.types = ('video_hd', 'video_mobile', 'print') # the type of attack
    self.ids = ['01', '02', '03', '05', '06', '07', '08', '09', '11', '12', '13', '14', '21', '22', '23', '24', '26', '28', '29', '30', '32', '33', '34', '35', '36', '37', '39', '42', '48', '49', '50', '51', '53', '54', '55'] # all the client IDs
    package_directory = os.path.dirname(os.path.abspath(__file__))
    if foldsdir == None:
      self.foldsdir = os.path.join(package_directory, 'folds')
    else:
      self.foldsdir = foldsdir

  def set_foldsdir(self, foldsdir):
    """Sets the directory holding the cross validation protocol of the database"""
    self.foldsdir = foldsdir

  def check_validity(self, l, obj, valid, default):
      """Checks validity of user input data against a set of valid values"""
      if not l: return default
      elif isinstance(l, six.string_types) or isinstance(l, six.integer_types): return self.check_validity((l,), obj, valid, default)
      for k in l:
        if k not in valid:
          raise RuntimeError('Invalid %s "%s". Valid values are %s, or lists/tuples of those' % (obj, k, valid))
      return l

  def get_file(self, pc):
    '''Returns the full file path given the path components pc'''
    from pkg_resources import resource_filename
    if os.path.isabs(pc):
      return pc
    return resource_filename(__name__, os.path.join(pc))


  def objects(self, ids=[], groups=None, cls=None, qualities=None, types=None, fold_no=0):
    """Returns a list of unique :py:class:`.File` objects for the specific query by the user.

    Keyword Parameters:

    ids
      The id of the client whose videos need to be retrieved. Should be an integer number belonging this list: ['01', '02', '03', '05', '06', '07', '08', '09', '11', '12', '13', '14', '21', '22', '23', '24', '26', '28', '29', '30', '32', '33', '34', '35', '36', '37', '39', '42', '48', '49', '50', '51', '53]

    groups
      One of the protocolar subgroups of data as specified in the tuple groups, or a
      tuple with several of them.  If you set this parameter to an empty string
      or the value None, we use reset it to the default which is to get all.

    cls
      Either "attack", "real" or a combination of those (in a
      tuple). Defines the class of data to be retrieved.  If you set this
      parameter to an empty string or the value None, it will be set to the tuple ("real", "attack").

    qualities
      Either "laptop" or "mobile" or a combination of those (in a
      tuple). Defines the qualities of the videos in the database that are going to be used. If you set this
      parameter to the value None, the videos of all qualities are returned ("laptop", "mobile").

    types
      Either "video_hd", "video_mobile" or "print" or any combination of those (in a
      tuple). Defines the types of attack videos in the database that are going to be used. If you set this
      parameter to the value None, the videos of all the attack types are returned ("video_hd", "video_mobile", "print").

    fold_no
      If 0, the original protocol published with this database will be used. Note that the original protocol does not contain development set. If bigger then zero (can be 1,2,3,4 or 5), then the protocol specified in the one of the cross-validation files will be used.

    Returns: A list of :py:class:`.File` objects.
    """

    # check if groups set are valid
    VALID_GROUPS = self.groups
    groups = self.check_validity(groups, "group", VALID_GROUPS, VALID_GROUPS)

    # by default, do NOT grab enrollment data from the database
    VALID_CLASSES = self.classes
    VALID_TYPES = self.types
    if cls == None and types != None: # types are strictly specified which means we don't need the calss of real accesses
      cls = ('attack',)
    else:
      cls = self.check_validity(cls, "class", VALID_CLASSES, ('real', 'attack'))

    # check if video quality types are valid
    VALID_QUALITIES = self.qualities
    qualities = self.check_validity(qualities, "quality", VALID_QUALITIES, VALID_QUALITIES)

    # check if attack types are valid

    if cls != ('real',): # if the class is 'real' only, then there is no need for types to be reset to the default (real accesses have no types)
      types = self.check_validity(types, "type", VALID_TYPES, VALID_TYPES)

    VALID_IDS = self.ids
    ids = self.check_validity(ids, "id", VALID_IDS, VALID_IDS)

    # from all the IDs, now filter just the ids that are needed depending on the group
    all_ids = {'train':[], 'test':[], 'devel':[]} 
    if fold_no == 0:
      if 'train' in groups:
        infilename = self.get_file(os.path.join(self.foldsdir, 'train_sub_list.txt'))
        f = open(infilename)
        in_ids = f.readlines(); in_ids = [x[:2] for x in in_ids] # removing the newline chars from the read lines
        all_ids['train'] = [x for x in ids if x in in_ids]
      if 'test' in groups:
        infilename = self.get_file(os.path.join(self.foldsdir, 'test_sub_list.txt'))
        f = open(infilename)
        in_ids = f.readlines(); in_ids = [x[:2] for x in in_ids] # removing the newline chars from the read lines
        all_ids['test'] = [x for x in ids if x in in_ids]

    else:
      if 'train' in groups or 'devel' in groups:    
        infilename = self.get_file(os.path.join(self.foldsdir, 'train_clients_%d.txt' % fold_no))
        f = open(infilename)
        for l in f.readlines():
          words = l.split()
          if words[1] == 't' and 'train' in groups:
            all_ids['train'].append(words[0])
          elif words[1] == 'd' and 'devel' in groups: 
            all_ids['devel'].append(words[0])
        if 'train' in groups:
          all_ids['train'] = [x for x in ids if x in all_ids['train']]
        if 'devel' in groups:
          all_ids['devel'] = [x for x in ids if x in all_ids['devel']]      

      if 'test' in groups:
        infilename = self.get_file(os.path.join(self.foldsdir, 'test_clients.txt'))
        f = open(infilename)
        in_ids = f.readlines(); in_ids = [x[:2] for x in in_ids] # removing the newline chars from the read lines
        all_ids['test'] = [x for x in ids if x in in_ids]

    retval = []

    quality_naming = {'laptop':'laptop', 'mobile':'android'}
    if 'real' in cls:
      for q in qualities:
        for group in groups:
          for client in all_ids[group]:
            filename = os.path.join('real', 'real_client0%s_%s_SD_scene01' % (client, quality_naming[q]))
            retval.append(File(filename, 'real', group))

    attack_naming = {'video_hd':'ipad_video', 'video_mobile':'iphone_video', 'print':'printed_photo'}
    if 'attack' in cls:
      for q in qualities:
        for t in types:
          for group in groups:
            for client in all_ids[group]:
              filename = os.path.join('attack', 'attack_client0%s_%s_SD_%s_scene01' % (client, quality_naming[q], attack_naming[t]))
              retval.append(File(filename, 'attack', group))
          
    return retval    
      
  
  def cross_valid_foldobjects(self, cls, types=None, qualities=None, fold_no=0):
    """ Returns two dictionaries: one with the files of the validation subset in one fold, and one with the files in the training subset of that fold. The number of the cross_validation fold is given as a parameter.

    Keyword parameters:

    cls
      The class of the samples: 'real' or 'attack'

    types
      Type of the database that is going to be used: 'warped', 'cut' or 'video' or a tuple of these

    qualities
      Either "low", "normal" or "high" or any combination of those (in a
      tuple). Defines the qualities of the videos in the database that are going to be used. If you set this
      parameter to the value None, the videos of all qualities are returned ("low", "normal", "high").

    fold_no
      Number of the fold
  """

    obj_devel = self.objects(groups='devel', cls=cls, qualities=qualities, types=types, fold_no=fold_no)
    obj_train = self.objects(groups='train', cls=cls, qualities=qualities, types=types, fold_no=fold_no)
    #files_devel = [o.make_path() for o in obj_devel]
    #files_train = [o.make_path() for o in obj_train]

    return obj_devel, obj_train

def get_config():
  """Returns a string containing the configuration information.
  """

  import pkg_resources

  packages = pkg_resources.require(__name__)
  this = packages[0]
  deps = packages[1:]

  retval =  "%s: %s (%s)\n" % (this.key, this.version, this.location)
  retval += "  - python dependencies:\n"
  for d in deps: retval += "    - %s: %s (%s)\n" % (d.key, d.version, d.location)

  return retval.strip()

# gets sphinx autodoc done right - don't remove it
__all__ = [_ for _ in dir() if not _.startswith('_')]


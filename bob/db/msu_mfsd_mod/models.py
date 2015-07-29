#!/usr/bin/env python
#Ivana Chingovska <ivana.chingovska@idiap.ch>
#Mon 16 Mar 12:49:23 CET 2015

import os
import bob.io.base
import bob.db.base
import numpy

class File(object):
  """ Generic file container """

  def __init__(self, filename, cls, group):

    self.filename = filename
    self.cls = cls # 'attack' or 'real'
    self.group = group # 'train' or 'test'
    
  def __repr__(self):
    return "File('%s')" % self.filename

  def get_file(self, pc):
    '''Returns the full file path given the path components pc'''
    from pkg_resources import resource_filename
    return resource_filename(__name__, os.path.join(pc))

  def make_path(self, directory=None, extension=None):
    """Wraps this files' filename so that a complete path is formed

    Keyword parameters:

    directory
      An optional directory name that will be prefixed to the returned result.

    extension
      An optional extension that will be suffixed to the returned filename. The
      extension normally includes the leading ``.`` character as in ``.jpg`` or
      ``.hdf5``.

    Returns a string containing the newly generated file path.
    """

    if not directory: directory = ''
    if not extension: extension = ''
    return os.path.join(directory, self.filename + extension)

  def is_real(self):
    """True if the file belongs to a real access, False otherwise """

    return bool(self.cls == 'real')

  def is_rotated(self):
    """True if the video file is originally recorded rotated by 180 degrees, False otherwise """

    infilename = self.get_file(os.path.join('rotated_videos', 'rotated_videos.txt'))
    f = open(infilename)
    rotated_videos = f.readlines(); 
    rotated_videos = [x[:-1] for x in rotated_videos] # removing the newline chars from the read lines
    return bool(self.make_path() in rotated_videos)
      
    
  def get_client_id(self):
    """The ID of the client. Value from 1 to 50. Clients in the train and devel set may have IDs from 1 to 20; clients in the test set have IDs from 21 to 50."""

    stem_file = self.filename.split('/')[1] # the file stem of the filename
    stem_client = self.filename.split('_')[1] # the client stem of the filename
    return stem_client[-2:]


  def get_type(self):
    """The type of attack, if it is an attack. Possible values: 'warped', 'cut' and 'video'. Returns None for real accesses"""
    
    if 'ipad_video' in self.filename:
      return 'video_hd'
    elif 'iphone_video' in self.filename:
      return 'video_mobile'
    elif 'printed_photo' in self.filename:
      return 'print'
    else:
      return None


  def get_quality(self):
    """The quality of the video file. Possible value: 'normal', 'low' and 'high'."""    
      
    if 'laptop' in self.filename:
      return 'laptop'
    else: #'android' in self.filename:
      return 'mobile'


  def facefile(self, directory=''):
    """Returns the path to the companion face bounding-box file

    Keyword parameters:

    directory
      An optional directory name that will be prefixed to the returned result.

    Returns a string containing the face file path.
    """
    if not directory: 
      directory = self.get_file('face-locations') # 'face-locations'
    return self.make_path(directory, '.face')


  def videofile(self, directory=None):
    """Returns the path to the database video file for this object

    Keyword parameters:

    directory
      An optional directory name that will be prefixed to the returned result.

    Returns a string containing the video file path.
    """

    if self.get_quality() == 'laptop':
      return self.make_path(directory, '.mov')
    else:  
      return self.make_path(directory, '.mp4')


  def bbx(self, directory=None):
    """Reads the file containing the face locations for the frames in the
    current video

    Keyword parameters:

    directory
      A directory name that will be prepended to the final filepaths where the
      face bounding boxes are located, if not on the current directory.

    Returns:
      A :py:class:`numpy.ndarray` containing information about the located
      faces in the videos. Each row of the :py:class:`numpy.ndarray`
      corresponds for one frame. The five columns of the
      :py:class:`numpy.ndarray` are (all integers):

      * Frame number (int)
      * Bounding box top-left X coordinate (int)
      * Bounding box top-left Y coordinate (int)
      * Bounding box width (int)
      * Bounding box height (int)

      Note that **not** all the frames may contain detected faces.
    """

    coords = numpy.loadtxt(self.facefile(directory), dtype=int, delimiter=',', usecols=range(0,5)) # reads all the locations as integers
    for i in range(0,coords.shape[0]):
      coords[i,3] = coords[i,3] - coords[i,1]
      coords[i,4] = coords[i,4] - coords[i,2]

    return coords
 

  def load(self, directory=None, extension='.hdf5'):
    """Loads the data at the specified location and using the given extension.

    Keyword parameters:

    data
      The data blob to be saved (normally a :py:class:`numpy.ndarray`).

    directory
      [optional] If not empty or None, this directory is prefixed to the final
      file destination

    extension
      [optional] The extension of the filename - this will control the type of
      output and the codec for saving the input blob.
    """
    return bob.io.base.load(self.make_path(directory, extension))


  def save(self, data, directory=None, extension='.hdf5'):
    """Saves the input data at the specified location and using the given
    extension.

    Keyword parameters:

    data
      The data blob to be saved (normally a :py:class:`numpy.ndarray`).

    directory
      If not empty or None, this directory is prefixed to the final file
      destination

    extension
      The extension of the filename - this will control the type of output and
      the codec for saving the input blob.
    """

    path = self.make_path(directory, extension)
    bob.io.base.create_directories_safe(os.path.dirname(path))
    bob.io.base.save(data, path)




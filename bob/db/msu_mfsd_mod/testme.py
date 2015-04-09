#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Ivana Chingovska <ivana.chingovska@idiap.ch>
#Mon 16 Mar 15:27:28 CET 2015
#
# Copyright (C) 2011-2012 Idiap Research Institute, Martigny, Switzerland
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""A few checks at the MSU MFSD database.
"""

import os, sys
import unittest
from . import Database, File
#from nose.plugins.skip import SkipTest


def main():
    db = Database()
    
    import ipdb; ipdb.set_trace()
    #fobj = db.objects() #280
    #fobj = db.objects(groups='train', ids=['01']) #0
    #fobj = db.objects(groups='devel', ids=['55'], fold_no=1)
    #print len(fobj)
    
    filename = os.path.join('real', 'real_client003_android_SD_scene01')
    thisobj = File(filename, 'real', 'test')
    print thisobj.is_rotated()
    #self.assertTrue(thisobj[0].is_rotated())

    filename = os.path.join('attack', 'attack_client003_laptop_SD_ipad_video_scene01')
    thisobj = File(filename, 'attack', 'test')
    print thisobj.is_rotated()
    #self.assertFalse(thisobj[0].is_rotated())


    '''

    fobj = db.objects(groups='devel', ids=['01'], fold_no=1)
    self.assertEqual(len(fobj), 8) # number of train videos for client '01' (fold 1)
     
    fobj = db.objects(groups='devel', ids=['55'], fold_no=1)
    self.assertEqual(len(fobj), 8) # number of train videos for client '01' (fold 1)
    
    fobj = db.objects(groups='train', fold_no=1, cls='real')
    self.assertEqual(len(fobj), 20) # number of real train videos

    fobj = db.objects(groups='devel', fold_no=1, cls='attack')
    self.assertEqual(len(fobj), 60) # number of attack devel videos

    fobj = db.objects(groups='train', fold_no=1, cls='attack', type='video_mobile')
    self.assertEqual(len(fobj), 20) # number of video_mobile attack devel videos

    fobj = db.objects(groups='test', fold_no=1, cls='attack', type='print', quality='mobile')
    self.assertEqual(len(fobj), 15) # number of print attack test videos recorded with mobile

    fobj = db.objects(groups='train', fold_no=1, cls='real', type='video_mobile')
    self.assertEqual(len(fobj), 0) # number of video_mobile real train videos

    filename = os.path.join('real', 'real_client001_android_SD_scene01')
    thisobj = File(filename, 'real', 'test')
    self.assertEqual(thisobj.get_clientid(), '01')
    self.assertEqual(thisobj.get_type(), None)
    self.assertEqual(thisobj.get_quality(), 'mobile')

    self.assertEqual(thisobj.video_file('xxx'), 'xxx/real/real_client001_android_SD_scene01.mp4')
    self.assertTrue(thisobj[0].is_real())

    filename = os.path.join('attack', 'attack_client003_laptop_SD_ipad_video_scene01')
    thisobj = File(filename, 'attack', 'test')
    self.assertEqual(thisobj.get_clientid(), '03')
    self.assertEqual(thisobj.get_type(), 'video_hd')
    self.assertEqual(thisobj.get_quality(), 'laptop')

    self.assertEqual(thisobj.make_path('xxx','.mov'), 'xxx/attack/attack_client003_laptop_SD_ipad_video_scene01.mov')
    self.assertEqual(thisobj.video_file('xxx'), 'xxx/attack/attack_client003_laptop_SD_ipad_video_scene01.mov')
    self.assertFalse(thisobj[0].is_real())
    '''    

if __name__ == '__main__':
  main()
    

#!/usr/bin/python3
# -*- coding: utf-8 -*-
# test_layout.py
import os
import sys
import unittest
import time
#import yaml

root_folder = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." ) 
yaml_file = os.path.join(root_folder, 'webapp', 'config.yaml')

sys.path.append(os.path.join(root_folder, 'webapp'))
import layout
yaml_data = layout.read_yaml(yaml_file) 
 
 
class TestLayout(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.yaml_data = ''
        

    
    def test_01_read_file(self):
        """
        read the yaml file - example for use is in comments below
        """
        self.assertEqual(len(yaml_data), 4)

    
    def test_02_screen(self):
        print('self.yaml_data[screen] = ', yaml_data['screen'])
    
    def test_03_widgets(self):
        print('self.yaml_data[widgets] = ', yaml_data['widgets'])
    
         
if __name__ == '__main__':
    unittest.main()

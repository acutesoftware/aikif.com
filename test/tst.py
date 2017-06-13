#!/usr/bin/python3
# -*- coding: utf-8 -*-
# test_transpose.py

import unittest
import sys
import os

class aikif_web_Test(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        
    def tearDown(self):
        unittest.TestCase.tearDown(self)
 
    def test_01_instantiate(self):

        self.assertEqual(5 , 5) 
        
if __name__ == '__main__':
    unittest.main()

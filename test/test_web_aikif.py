#!/usr/bin/python3
# -*- coding: utf-8 -*-
# test_transpose.py

import unittest
import sys
import os

root_folder = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." ) 
pth = root_folder + os.sep + 'webapp'

sys.path.append(pth)
import aikif_web

class aikif_web_Test(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        
    def tearDown(self):
        unittest.TestCase.tearDown(self)
 
    def test_02_page_home(self):
        import aikif_web
        res = aikif_web.page_home()
        print(res)

    def test_08_events(self):
        # locks, so dont do this - aikif_web.start_server()
        
        ev = aikif_web.get_events()
        print(ev)
        self.assertEqual(len(ev) , 2) 
    

        
if __name__ == '__main__':
    unittest.main()

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
 
    def test_03_search_post(self):
        res = aikif_web.search_post()
        print(res)
        self.assertEqual(res , 'todo') 

        
    def test_04_get_data_list(self):
        res = aikif_web.get_data_list()
        self.assertEqual(res , ['Character', 'Object', 'Location', 'Event', 'Process', 'Fact'])
    

    def test_05_get_agents(self):
        res = aikif_web.get_agents()
        print('agents = ', res)
        self.assertTrue('AgentInterfaceWindows:Windows Interface' in res)
        self.assertEqual(len(res) , 3)
    
        
    def test_08_events(self):
        # locks, so dont do this - aikif_web.start_server()
        
        ev = aikif_web.get_events()
        print(ev)
        self.assertEqual(len(ev) , 2) 
    

        
if __name__ == '__main__':
    unittest.main()

# Tianyi Lan #
# Challenge2: crime-data #

import unittest
import filter_data as filt
import fix_neighborhood as fn
import fix_type as ft

class FixNeighborhood(unittest.TestCase):
    # when name is a subtring of real neighborhood name
    def test_for_substr(self):
        result = fn.fix_neighborhood(['24845','OFFENSE 2.0','2701','Simple Assault.','2015-05-10T05:36:00','1700 block Belleau Dr','Squirrel Hill','1'])
        expected = 'Squirrel Hill North'
        self.assertEqual(expected, result)
    # when real neighborhood name is contained in name
    def test_for_contain(self):
        result = fn.fix_neighborhood(['24845','OFFENSE 2.0','2701','Simple Assault.','2015-05-10T05:36:00','1700 block Belleau Dr','Chateauu','1'])
        expected = 'Chateau'
        self.assertEqual(expected, result)
    # when no real neighborhood can be matched
    def test_for_no_match(self):
        result = fn.fix_neighborhood(['24845','OFFENSE 2.0','2701','Simple Assault.','2015-05-10T05:36:00','1700 block Belleau Dr','Golden Triangle','1'])
        expected = False
        self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main()                                     

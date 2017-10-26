from os.path import exists
from pathlib import Path
import unittest

from print_pwsafe import PrintPySafe

class TestPrintPysafe(unittest.TestCase):

    def test_basic(self):
        # Check test XML file exists
        test = Path('./test.xml')
        self.assertTrue(exists(str(test)))
        # create object
        pps = PrintPySafe(test)
        self.assertIsNone(print(pps),'Making sure can print results')



import io
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


    def test_file(self):
        test = Path('./test.xml')
        # create object
        pps = PrintPySafe(test)
        with io.open('test.markdown', 'w', encoding='utf8') as f:
                f.write(str(pps))


    def test_excel(self):
        test = Path('./test.xml')
        # create object
        pps = PrintPySafe(test)
        pps.to_excel('test.xlsx')

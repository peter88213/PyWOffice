"""Development test for the pyWriter project.

Test the Use Cases "manage the collection".

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import unittest

from pywoffice.model.collection import Collection
from pywoffice.html.bookdesc import BookDesc


DATA_PATH = '../data'
TEST_FILE = 'collection.pwc'

os.chdir('yw7')


def read_file(inputFile):
    with open(inputFile, 'r', encoding='utf-8') as f:
        return(f.read())


def copy_file(inputFile, outputFile):
    with open(inputFile, 'rb') as f:
        myData = f.read()
    with open(outputFile, 'wb') as f:
        f.write(myData)
    return()


def remove_all_testfiles():
    try:
        os.remove(TEST_FILE)
    except:
        pass


class devel(unittest.TestCase):

    def setUp(self):
        remove_all_testfiles()

        try:
            os.mkdir('yWriter Projects')
        except:
            pass
        try:
            os.mkdir('yWriter Projects/The Gravity Monster.yw')
        except:
            pass

        copy_file(DATA_PATH + '/yWriter Projects/The Gravity Monster.yw/The Gravity Monster.yw7',
                  'yWriter Projects/The Gravity Monster.yw/The Gravity Monster.yw7')
        try:
            os.mkdir('yWriter Projects/The Refugee Ship.yw')
        except:
            pass

        copy_file(DATA_PATH + '/yWriter Projects/The Refugee Ship.yw/The Refugee Ship.yw7',
                  'yWriter Projects/The Refugee Ship.yw/The Refugee Ship.yw7')

    def test_add_book(self):
        """Use Case: manage the collection/add a book to the collection."""
        copy_file(DATA_PATH + '/_collection/create_collection.xml', TEST_FILE)
        myCollection = Collection(TEST_FILE)

        self.assertEqual(myCollection.read(),
                         'SUCCESS: 0 Books found in "' + TEST_FILE + '".')

        self.assertEqual(myCollection.add_book(
            'yWriter Projects/The Gravity Monster.yw/The Gravity Monster.yw7'),
            'SUCCESS: "The Gravity Monster" added to the collection.')

        self.assertEqual(myCollection.write(),
                         'SUCCESS: Collection written to "' + TEST_FILE + '".')

        self.assertEqual(read_file(TEST_FILE),
                         read_file(DATA_PATH + '/_collection/add_first_book.xml'))

        self.assertEqual(myCollection.add_book(
            'yWriter Projects/The Refugee Ship.yw/The Refugee Ship.yw7'),
            'SUCCESS: "The Refugee Ship" added to the collection.')

        self.assertEqual(myCollection.write(),
                         'SUCCESS: Collection written to "' + TEST_FILE + '".')

        self.assertEqual(read_file(TEST_FILE),
                         read_file(DATA_PATH + '/_collection/add_second_book.xml'))


def main():
    unittest.main()


if __name__ == '__main__':
    main()

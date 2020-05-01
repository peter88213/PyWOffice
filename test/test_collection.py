"""Integration tests for the pyWriter project.

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


class NrmOpr(unittest.TestCase):
    """Test case: Normal operation
    """

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

    def test_read_write_configuration(self):
        """Read and write the configuration file. """
        copy_file(DATA_PATH + '/_collection/read_write.xml', TEST_FILE)
        myCollection = Collection(TEST_FILE)

        self.assertEqual(myCollection.read(),
                         'SUCCESS: 2 Books found in "' + TEST_FILE + '".')

        os.remove(TEST_FILE)

        self.assertEqual(myCollection.write(),
                         'SUCCESS: Collection written to "' + TEST_FILE + '".')

        self.assertEqual(read_file(TEST_FILE),
                         read_file(DATA_PATH + '/_collection/read_write.xml'))

    def test_create_collection(self):
        """Use Case: manage the collection/create the collection."""
        myCollection = Collection(TEST_FILE)

        self.assertEqual(myCollection.write(),
                         'SUCCESS: Collection written to "' + TEST_FILE + '".')

        self.assertEqual(read_file(TEST_FILE),
                         read_file(DATA_PATH + '/_collection/create_collection.xml'))

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

    def test_remove_book(self):
        """Use Case: manage the collection/remove a book from the collection."""
        copy_file(DATA_PATH + '/_collection/add_second_book.xml', TEST_FILE)
        myCollection = Collection(TEST_FILE)

        self.assertEqual(myCollection.read(),
                         'SUCCESS: 2 Books found in "' + TEST_FILE + '".')

        myCollection.remove_book('1')

        self.assertEqual(myCollection.write(),
                         'SUCCESS: Collection written to "' + TEST_FILE + '".')

        self.assertEqual(read_file(TEST_FILE),
                         read_file(DATA_PATH + '/_collection/remove_book.xml'))

        myCollection.remove_book('2')

        self.assertEqual(myCollection.write(),
                         'SUCCESS: Collection written to "' + TEST_FILE + '".')

        self.assertEqual(read_file(TEST_FILE),
                         read_file(DATA_PATH + '/_collection/create_collection.xml'))

    def test_create_series(self):
        """Use Case: manage book series/create a series."""
        copy_file(DATA_PATH + '/_collection/add_first_book.xml', TEST_FILE)
        myCollection = Collection(TEST_FILE)

        self.assertEqual(myCollection.read(),
                         'SUCCESS: 1 Books found in "' + TEST_FILE + '".')

        myCollection.add_series('Rick Starlift')

        self.assertEqual(myCollection.write(),
                         'SUCCESS: Collection written to "' + TEST_FILE + '".')

        self.assertEqual(read_file(TEST_FILE),
                         read_file(DATA_PATH + '/_collection/empty_series.xml'))

    def test_remove_series(self):
        """Use Case: manage book series/remove a series."""
        copy_file(DATA_PATH + '/_collection/empty_series.xml', TEST_FILE)
        myCollection = Collection(TEST_FILE)

        self.assertEqual(myCollection.read(),
                         'SUCCESS: 1 Books found in "' + TEST_FILE + '".')

        myCollection.remove_series('Rick Starlift')

        self.assertEqual(myCollection.write(),
                         'SUCCESS: Collection written to "' + TEST_FILE + '".')

        self.assertEqual(read_file(TEST_FILE),
                         read_file(DATA_PATH + '/_collection/add_first_book.xml'))

    def test_add_book_to_series(self):
        """Use Case: manage book series/add a book to a series."""
        copy_file(DATA_PATH + '/_collection/empty_series.xml', TEST_FILE)
        myCollection = Collection(TEST_FILE)

        self.assertEqual(myCollection.read(),
                         'SUCCESS: 1 Books found in "' + TEST_FILE + '".')

        for series in myCollection.srtSeries:

            if series.title == 'Rick Starlift':
                series.add_book('1')
                break

        self.assertEqual(myCollection.write(),
                         'SUCCESS: Collection written to "' + TEST_FILE + '".')

        self.assertEqual(read_file(TEST_FILE),
                         read_file(DATA_PATH + '/_collection/add_book_to_series.xml'))

    def test_remove_book_from_series(self):
        """Use Case: manage book series/remove a book from a series."""
        copy_file(DATA_PATH + '/_collection/add_book_to_series.xml', TEST_FILE)
        myCollection = Collection(TEST_FILE)

        self.assertEqual(myCollection.read(),
                         'SUCCESS: 1 Books found in "' + TEST_FILE + '".')

        for series in myCollection.srtSeries:

            if series.title == 'Rick Starlift':
                self.assertEqual(series.remove_book('1'), 'SUCCESS')
                break

        self.assertEqual(myCollection.write(),
                         'SUCCESS: Collection written to "' + TEST_FILE + '".')

        self.assertEqual(read_file(TEST_FILE),
                         read_file(DATA_PATH + '/_collection/empty_series.xml'))

    def test_write_descriptions(self):
        """Use Case: write series and book descriptions to a html file."""
        copy_file(DATA_PATH + '/_collection/two_in_series.xml', TEST_FILE)
        myCollection = Collection(TEST_FILE)

        self.assertEqual(myCollection.read(),
                         'SUCCESS: 2 Books found in "' + TEST_FILE + '".')

        myBookdesc = BookDesc('Rick Starlift_series.html')

        for series in myCollection.srtSeries:

            if series.title == 'Rick Starlift':
                self.assertEqual(myBookdesc.write(
                    series, myCollection), 'SUCCESS: "Rick Starlift_series.html" saved.')

        self.assertEqual(read_file('Rick Starlift_series.html'),
                         read_file(DATA_PATH + '/_collection/two_in_series.html'))

    def test_read_descriptions(self):
        """Use Case: read descriptions from a html file and write them to collection and yWriter project."""
        copy_file(DATA_PATH + '/_collection/without_desc.yw7',
                  'yWriter Projects/The Gravity Monster.yw/The Gravity Monster.yw7')
        copy_file(DATA_PATH + '/_collection/two_in_series.xml', TEST_FILE)
        copy_file(DATA_PATH + '/_collection/add_descriptions.html',
                  'Rick Starlift_series.html')
        myCollection = Collection(TEST_FILE)

        self.assertEqual(myCollection.read(),
                         'SUCCESS: 2 Books found in "' + TEST_FILE + '".')

        myBookdesc = BookDesc('Rick Starlift_series.html')

        for series in myCollection.srtSeries:

            if series.title == 'Rick Starlift':
                self.assertEqual(myBookdesc.read(
                    series, myCollection), 'SUCCESS')

        self.assertEqual(myCollection.write(),
                         'SUCCESS: Collection written to "' + TEST_FILE + '".')

        self.assertEqual(read_file(TEST_FILE),
                         read_file(DATA_PATH + '/_collection/add_descriptions.xml'))

        self.assertEqual(read_file('yWriter Projects/The Gravity Monster.yw/The Gravity Monster.yw7'),
                         read_file(DATA_PATH + '/_collection/with_desc.yw7'))


def main():
    unittest.main()


if __name__ == '__main__':
    main()

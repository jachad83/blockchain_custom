import unittest
from reader import file_capture


class FileReadTestCase(unittest.TestCase):
    """Tests for `reader.py`."""

    def test_is_list_returned(self):
        """Is a list returned?"""
        self.assertIs(type(file_capture(buffer=65536, limit=10, folder='data')), list,
                      msg="File reader does not return a list.")

    def test_list_is_strings(self):
        """Is the list comprised of strings?"""
        data = file_capture(buffer=65536, limit=10, folder='data')
        for _ in data:
            self.assertIs(type(_), str,
                          msg=f'Item at list index {data.index(_)} is not a string.')

    def test_list_is_correct_length(self):
        """Does the list length not exceed argument *limit*?"""
        list_length = 3
        data = file_capture(buffer=65536, limit=list_length, folder='data')
        self.assertLessEqual(len(data), list_length, msg='List length exceeds list limit variable.')


if __name__ == '__main__':
    unittest.main()

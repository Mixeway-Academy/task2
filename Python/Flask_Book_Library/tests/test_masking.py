import io
import unittest
from contextlib import redirect_stdout

from project.masking import mask
from project.customers.models import Customer


class MaskTest(unittest.TestCase):
    def test_same_length_asterisks(self):
        self.assertEqual(mask('123456890'), '*********')
        self.assertEqual(mask('ul. Polna 5'), '*' * 11)

    def test_non_string_and_none(self):
        self.assertEqual(mask(15), '**')
        self.assertIsNone(mask(None))
        self.assertEqual(mask(''), '')

    def test_customer_log_line_hides_pesel_and_address(self):
        out = io.StringIO()
        with redirect_stdout(out):  # __init__ prints the repr to logs
            Customer('Jan', 'Warszawa', 30, '90010112345', 'ul. Polna 5', '7A')
        line = out.getvalue()
        for secret in ('90010112345', 'Warszawa', 'ul. Polna 5', '7A'):
            self.assertNotIn(secret, line)
        self.assertIn('Pesel: ***********', line)
        self.assertIn('Name: Jan', line)


if __name__ == '__main__':
    unittest.main()

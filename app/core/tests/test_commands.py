"""
Test custom Django manaagement commands
"""

from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """ Test Commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for db if db is ready"""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""
        patched_check.side_effect = [Psycopg2Error]*2 \
            + [OperationalError]*3 + [True]
        # The mocking library will raise the exceptions that passed
        # First 2 times : it will raise Psycopg2Error
        # we can give what ever we want
        # patched_check.side_effect = [Psycopg2Error]*20 + [True]

        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])

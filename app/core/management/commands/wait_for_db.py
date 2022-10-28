"""
Djangho command to wait for database to be available
"""

import time

from psycopg2 import OperationalError as Psycopg2Error

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django commmanf to wait for database"""

    def handle(self, *args, **kwargs):
        "Entrypoint for command"
        self.stdout.write("Waiting for database...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('DB is unavailable, waiting for 1 Second')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database is ready'))

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import sqlite3

SERVER_DIR = 'src'

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', SERVER_DIR + '.config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # check for db.sqlite3 to see if first run
    db_path = SERVER_DIR + '/db.sqlite3'
    needs_setup = False

    # run setup if no db.sqlite3, this is pretty much copy of the course TMC code
    if os.path.exists(SERVER_DIR + '/db.sql') and not os.path.exists(db_path):
        needs_setup = True
        print("Found db.sql but not db.sqlite, recreating a database")
        dump = '\n'.join(open(SERVER_DIR + '/db.sql').readlines())
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.executescript(dump)
        conn.commit()

    # setup db
    if len(sys.argv) >= 2 and sys.argv[1] == 'runserver' and needs_setup:
        print("First run detected, setting up database")
        print("Running migrations")
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
        print("Setting up demo data")
        execute_from_command_line(['manage.py', 'setup_demo'])
        print("Setup complete, starting server\n")

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

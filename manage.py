#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gymInsight.settings')
    
    # Check if we are running the server
    if 'runserver' in sys.argv:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'makemigrations', 'userApis'])
        execute_from_command_line(['manage.py', 'makemigrations', 'adminMetaDataApis'])
        execute_from_command_line(['manage.py', 'makemigrations', 'userMetaDataApis'])
        execute_from_command_line(['manage.py', 'migrate'])
        execute_from_command_line(['manage.py', 'createSuperAdmin'])
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

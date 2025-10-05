"""
WSGI config for inventory_management project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')

application = get_wsgi_application()
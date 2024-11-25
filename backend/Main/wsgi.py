# Standard / external libraries
import os
import django.core.wsgi

# External modules

# Internal modules

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Main.settings')

application = django.core.wsgi.get_wsgi_application()
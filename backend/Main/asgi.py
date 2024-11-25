# Standard / external libraries
import os
import django.core.asgi

# External modules

# Internal modules

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Main.settings')

application = django.core.asgi.get_asgi_application()
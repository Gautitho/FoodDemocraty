# Standard / external libraries
import django

# External modules

# Internal modules
import FoodDemocraty.models

# Core code
django.contrib.admin.site.register(FoodDemocraty.models.Restaurant)
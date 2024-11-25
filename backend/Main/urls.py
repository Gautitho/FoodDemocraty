# Standard / external libraries
import django

# External modules

# Internal modules

# Core code

urlpatterns = [
    django.urls.path('admin/', django.contrib.admin.site.urls),
    django.urls.path('api-auth/', django.urls.include('rest_framework.urls', namespace='rest_framework')),
    django.urls.path('FoodDemocracy/', django.urls.include('FoodDemocraty.urls')),
]

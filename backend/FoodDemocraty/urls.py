# Standard / external libraries
import django
import rest_framework.routers

# External modules

# Internal modules
import FoodDemocraty.models
import FoodDemocraty.services

# Core code
router = rest_framework.routers.DefaultRouter()
router.register(r'restaurant_list', FoodDemocraty.models.RestaurantViewSet)

urlpatterns = [
    django.urls.path('', django.urls.include(router.urls)),
    django.urls.path('counting/', FoodDemocraty.services.CountingView.as_view(), name='counting'),
]

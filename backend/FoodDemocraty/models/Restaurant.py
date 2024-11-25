# Standard / external libraries
import django
import rest_framework
import rest_framework.viewsets
import rest_framework.decorators
import rest_framework.response

# External modules
import xpt_utils as xu

# Internal modules

# Core code
class Restaurant(django.db.models.Model):
    name            = django.db.models.CharField(max_length=100,    default="Default name")
    description     = django.db.models.TextField(default="Default description")
    selected        = django.db.models.BooleanField(default=True)
    website_link    = django.db.models.CharField(max_length=500,    default="Default website link")
    position_link   = django.db.models.CharField(max_length=500,    default="Default position link")
    max_table_size  = django.db.models.IntegerField(default=0)

    def __str__(self):
        return f"{self.to_dict(info_level=1)}"

    def to_dict(self, info_level=django.conf.settings.MODEL_DEFAULT_INFO_LEVEL, deep_info_level=1):
        dic = {}
        dic["id"]   = self.id
        if (info_level >= 1):
            dic["name"]             = self.name
        if (info_level >= 2):
            dic["description"]      = self.description
            dic["selected"]         = self.selected
        if (info_level >= 3):
            dic["website_link"]     = self.website_link
            dic["position_link"]    = self.position_link
            dic["max_table_size"]   = self.max_table_size
        if (info_level >= 5):
            dic["class"]            = self.__class__.__name__
        return dic


class RestaurantSerializer(rest_framework.serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["id", "name", "description", "selected", "website_link", "position_link", "max_table_size"]


class RestaurantViewSet(rest_framework.viewsets.ModelViewSet):
    queryset            = Restaurant.objects.all()
    serializer_class    = RestaurantSerializer

from rest_framework.serializers import ModelSerializer
from .models import Products, Logs

class ProductSerializer(ModelSerializer):
    class Meta:
        model=Products
        fields='__all__'

class LogsSerializer(ModelSerializer):
    class Meta:
        model=Logs
        fields='__all__'
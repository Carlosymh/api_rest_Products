from django.db import models

class Products(models.Model):
    id=models.AutoField(primary_key=True)
    sku=models.CharField(unique=True, max_length=255)
    ean=models.CharField(max_length=255)
    name=models.CharField(max_length=255)
    description=models.TextField(blank=True)
    brand=models.CharField(max_length=255)
    price=models.FloatField()
    quantity=models.IntegerField()

class Logs(models.Model):
    user_name=models.CharField(max_length=255)
    products=models.CharField(max_length=255)
    value=models.CharField(max_length=255)
    route=models.CharField(max_length=255)
    create_at=models.DateField(auto_now_add=True)




 
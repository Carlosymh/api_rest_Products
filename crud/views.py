from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from crud import serializers
from .models import Products, Logs
from .serializers import ProductSerializer, LogsSerializer
from django.contrib.auth.models import User

@api_view(['GET']) 
def getProduct(request,pk):
    
    product =  Products.objects.get(id=pk)
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    print(content)
    
    serializer=ProductSerializer(product, many=False)
    logs = Logs.objects.create(
        user_name=str(request.user),
        products=product.name,
        value='ID:{}'.format(pk),
        route='api/getProduct/{}'.format(pk)
    )
    
    serializerLogs=LogsSerializer(logs, many=False)
    return Response(serializer.data)

@api_view(['GET']) 
def searchProducts(request,value):
    
    products =  Products.objects.filter(Q(name__icontains=value) | Q(description__icontains=value))
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    print(content)
    serializer=ProductSerializer(products,many=True)
    
    logs = Logs.objects.create(
        user_name=str(request.user),
        products=value,
        value=value,
        route='api/searchProducts/{}'.format(value)
    )
    
    serializerLogs=LogsSerializer(logs, many=False)
    return Response(serializer.data)

@api_view(['GET']) 
def getProducts(request):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    print(content)
    
    logs = Logs.objects.create(
        user_name=str(request.user),
        products='All',
        value='All',
        route='api/getProducts'
    )
    
    serializer=LogsSerializer(logs, many=False)

    products=Products.objects.all()
    serializer=ProductSerializer(products,many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def postProducts(request):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    print(content)
    data = request.data
    product = Products.objects.create(
        sku=data['sku'],
        ean=data['ean'],
        name=data['name'],
        description=data['description'],
        brand=data['brand'],
        price=data['price'],
        quantity=data['quantity'],
    )
    serializer=ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def putProduct(request,pk):
    username=str(request.user)
    content = {
        'user': username,  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    print(content)
    data=request.data
    product =  Products.objects.get(id=pk)
    serializer = ProductSerializer(instance=product, data=data)
    if serializer.is_valid():
        serializer.save()
        email_List =  User.objects.exclude(username=username).values_list('email', flat=True)
        subject='Updated Product'
        message='the user {} updated the products with id {}'.format(username.capitalize(), pk)
        email_from= settings.EMAIL_HOST_USER
        recipient_list=list(email_List)
        print(subject, message, email_from, recipient_list)
        send_mail(subject, message, email_from, recipient_list)
        return Response(serializer.data,status=200)
    else:
        return Response({'message':'Product not found'},status=400)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def deleteProduct(request,pk):
    
    username=str(request.user)
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    print(content)
    product =  Products.objects.get(id=pk)
    product.delete()
    email_List =  User.objects.exclude(username=username).values_list('email', flat=True)
    subject='Deleted Product'
    message='the user {} deleted the products with id {}'.format(username, pk)
    email_from= settings.EMAIL_HOST_USER
    recipient_list=list(email_List)
    print(subject, message, email_from, recipient_list)
    send_mail(subject, message, email_from, recipient_list)
    return Response('Product Delected')

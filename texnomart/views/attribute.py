from rest_framework.generics import ListAPIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from texnomart.models import AttributeKey, AttributeValue, ProductAttribute
from texnomart.serializers import AttributeKeySerializer, AttributeValueSerializer, ProductAttributeSerializer


class AttributeKeyListApiView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = AttributeKeySerializer
    queryset = AttributeKey.objects.all()


class AttributeValueListApiView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = AttributeValueSerializer
    queryset = AttributeValue.objects.all()


class ProductAttributeListApiView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductAttributeSerializer
    queryset = ProductAttribute.objects.all()

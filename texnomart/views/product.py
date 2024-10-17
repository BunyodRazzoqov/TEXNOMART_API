from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache
from texnomart.models import Product
from texnomart.serializers import ProductSerializer


class AllProductsApiView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        cache_key = 'product_list'
        cached_data = cache.get(cache_key)
        if not cached_data:
            queryset = Product.objects.all().select_related('category')
            cache.set(cache_key, queryset, timeout=60 * 1)
            return queryset
        return cached_data


class ProductDetailApiView(RetrieveAPIView):
    authentication_classes = [AllowAny]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class ProductCreateApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# class ProductUpdateApiView(UpdateAPIView):
#     permission_classes = [AllowAny]
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = 'id'


class ProductUpdateApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response(data={'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDeleteApiView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response(data={'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response(data={'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(data={'success': 'Product successfully deleted'}, status=status.HTTP_204_NO_CONTENT)

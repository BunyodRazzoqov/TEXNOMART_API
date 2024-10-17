from django.shortcuts import render
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from texnomart.models import Category
from texnomart.serializers import CategorySerializer


class CategoriesApiView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        cache_key = 'category_list'
        cached_data = cache.get(cache_key)
        if not cached_data:
            queryset = Category.objects.all()
            cache.set(cache_key, queryset, timeout=60 * 1)
            return queryset
        return cached_data


class CategoryDetailApiView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class CategoryCreateApiView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryUpdateApiView(APIView):
    """Update using only patch"""
    permission_classes = [IsAuthenticated]

    def get_object(self, slug):
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return None

    def get(self, request, slug):
        category = self.get_object(slug)
        if category is None:
            return Response(data={'error': 'Category not found'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, slug):
        category = self.get_object(slug)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CategoryUpdateApiView(UpdateAPIView):
#     """"Update using put and patch methods"""
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [AllowAny]
#     lookup_field = 'slug'


class CategoryDeleteApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, slug):
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return None

    def get(self, request, slug):
        category = self.get_object(slug)
        if category is None:
            return Response(data={'error': 'Category not found'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def delete(self, request, slug):
        category = self.get_object(slug)
        if category is None:
            return Response(data={'error': 'Category not found'}, status=status.HTTP_400_BAD_REQUEST)

        category.delete()
        return Response(data={'status': 'success'}, status=status.HTTP_200_OK)

from django.urls import path
from texnomart.views import category, product, attribute

urlpatterns = [
    path('', product.AllProductsApiView.as_view()),
    # Category urls
    path('categories/', category.CategoriesApiView.as_view()),
    path('category/add-category/', category.CategoryCreateApiView.as_view()),
    path('category/<slug:slug>/', category.CategoryDetailApiView.as_view()),
    path('category/<slug:slug>/delete/', category.CategoryDeleteApiView.as_view()),
    path('category/<slug:slug>/edit/', category.CategoryUpdateApiView.as_view()),
    # Product urls
    path('product/<int:id>/detail/', product.ProductDetailApiView.as_view()),
    path('product/create/', product.ProductCreateApiView.as_view()),
    path('product/<int:pk>/edit/', product.ProductUpdateApiView.as_view()),
    path('product/<int:pk>/delete/', product.ProductDeleteApiView.as_view()),
    # Attribute urls
    path('attribute-key/', attribute.AttributeKeyListApiView.as_view()),
    path('attribute-value/', attribute.AttributeValueListApiView.as_view()),
    path('product-attribute/', attribute.ProductAttributeListApiView.as_view()),
]

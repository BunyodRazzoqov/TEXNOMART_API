from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from texnomart.models import Category, Product, Image, Comment, AttributeKey, AttributeValue, ProductAttribute
from users.models import User


# Register your models here.


class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'title', 'category_image')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('id', 'title',)
    list_filter = ('id', 'title',)

    def category_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 40px; height: auto;" />', obj.image.url)

    category_image.short_description = 'Image'


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'quantity', 'discount', 'user_like')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('id', 'name',)

    def user_like(self, obj):
        for user in User.objects.all():
            if user in obj.users_like.all():
                return True

        return False

    user_like.boolean = True
    user_like.short_description = 'User Like'


class ImageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'product', 'is_primary', 'images')
    search_fields = ('id', 'product')
    list_filter = ('id', 'product')

    def images(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 40px; height: auto;" />', obj.image.url)

    images.short_description = 'Image'


class CommentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'my_rating')
    search_fields = ('id', 'user', 'product')
    list_filter = ('id', 'user', 'rating')

    def my_rating(self, obj):
        if obj.rating:
            return format_html('<span style="color:green">{}</span>', obj.rating)

        else:
            return format_html('<span style="color:red">{}</span>', obj.rating)

    my_rating.short_description = 'Rating'


class AttributeKeyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'key_name')
    search_fields = ('id', 'key_name')
    list_filter = ('id', 'key_name')


class AttributeValueAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'value_name')
    search_fields = ('id', 'value_name')
    list_filter = ('id', 'value_name')


class ProductAttributeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'attribute', 'value', 'product')
    search_fields = ('id', 'attribute', 'value', 'product')
    list_filter = ('id', 'attribute', 'value')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(AttributeKey, AttributeKeyAdmin)
admin.site.register(AttributeValue, AttributeValueAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)

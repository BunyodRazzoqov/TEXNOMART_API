from rest_framework import serializers

from texnomart.models import Product, Category, Comment, AttributeKey, AttributeValue, ProductAttribute


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    users_like = serializers.SerializerMethodField(method_name='get_users_like')
    comments = CommentSerializer(many=True, read_only=True)
    users_comment = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField(method_name='get_comments_count')
    images = serializers.SerializerMethodField(method_name='get_images')
    category_name = serializers.CharField(source='category.title', read_only=True)

    def get_images(self, obj):
        request = self.context.get('request')
        images = [request.build_absolute_uri(image.image.url) for image in obj.images.all()]
        return images

    def get_users_like(self, product):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        if user in product.users_like.all():
            return True

        return False

    def get_users_comment(self, obj):
        comments = [comment.user.email for comment in obj.comments.all()]
        return comments

    def get_comments_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    all_products_count = serializers.SerializerMethodField(method_name='get_products')

    def get_products(self, obj):
        return obj.products.count()

    class Meta:
        model = Category
        fields = '__all__'


class AttributeKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeKey
        fields = '__all__'


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = '__all__'


class ProductAttributeSerializer(serializers.ModelSerializer):
    key_name = serializers.CharField(source='attribute.key_name', read_only=True)
    value_name = serializers.CharField(source='value.value_name', read_only=True)

    class Meta:
        model = ProductAttribute
        fields = '__all__'

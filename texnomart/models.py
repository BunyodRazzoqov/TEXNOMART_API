from django.db import models
from django.utils.text import slugify
from users.models import User


# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    title: str = models.CharField(max_length=255, unique=True)
    slug: str = models.SlugField(unique=True, null=True, blank=True)
    image: str = models.ImageField(upload_to='category/%Y/%m/%d/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Product(BaseModel):
    name: str = models.CharField(max_length=100)
    slug: str = models.SlugField(unique=True, null=True, blank=True)
    description: str = models.TextField(null=True, blank=True, default='good')
    price: float = models.FloatField(null=True, blank=True, default=0)
    discount: int = models.IntegerField(default=0, null=True, blank=True)
    quantity: int = models.PositiveIntegerField(default=0, null=True, blank=True)
    users_like: str = models.ManyToManyField(User, related_name='products', null=True, blank=True)
    category: str = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)

        return self.price

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'
        verbose_name_plural = 'products'


class Image(BaseModel):
    image: str = models.ImageField(upload_to='products/images/', null=True, blank=True)
    product: str = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    is_primary: bool = models.BooleanField(default=False)

    class Meta:
        db_table = 'image'

    @property
    def is_primary_image(self):
        if self.is_primary:
            return self.image

    def __str__(self):
        return str(self.id)


class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        ZERO = 0
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    message: str = models.TextField(null=True, blank=True)
    file: str = models.FileField(upload_to='comments/%Y/%m/%d/', null=True, blank=True)
    product: str = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user: str = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='comments')
    rating: int = models.PositiveSmallIntegerField(choices=RatingChoices.choices, default=RatingChoices.ZERO.value,
                                                   null=True)

    def __str__(self):
        return self.message


class AttributeKey(BaseModel):
    key_name: str = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.key_name

    class Meta:
        db_table = 'attributes'


class AttributeValue(BaseModel):
    value_name: str = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.value_name

    class Meta:
        db_table = 'attribute_values'


class ProductAttribute(BaseModel):
    attribute: str = models.ForeignKey(AttributeKey, on_delete=models.CASCADE)
    value: str = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    product: str = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_attributes'
        verbose_name_plural = 'product_attributes'

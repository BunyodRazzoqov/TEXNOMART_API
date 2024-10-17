import json
import mimetypes
import os
from datetime import datetime

from django.core.mail import send_mail, EmailMessage
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from config.settings import BASE_DIR
from texnomart.models import Category, Product
from users.models import User


@receiver(pre_delete, sender=Category)
def category_pre_delete(sender, instance, **kwargs):
    if instance.image:
        instance_data = {
            'id': instance.id,
            'title': instance.title,
            'slug': instance.slug,
            'image': instance.image.url,
            'deleted': str(datetime.now()),
        }
    else:
        instance_data = {
            'id': instance.id,
            'title': instance.title,
            'slug': instance.slug,
            'deleted': str(datetime.now()),
        }
    json_file_path = os.path.join(BASE_DIR, 'texnomart', 'deleted_data', 'deleted_categories.json')
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            try:
                data = json.load(f)

            except json.JSONDecodeError:
                data = []

    else:
        data = []

    data.append(instance_data)

    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)


@receiver(pre_delete, sender=Product)
def product_pre_delete(sender, instance, **kwargs):
    instance_data = {
        'id': instance.id,
        'name': instance.name,
        'slug': instance.slug,
        'description': instance.description,
        'price': instance.price,
        'discount': instance.discount,
        'quantity': instance.quantity,
        'users_like': str(instance.users_like),
        'category': str(instance.category),
        'deleted': str(datetime.now()),
    }
    json_file_path = os.path.join(BASE_DIR, 'texnomart', 'deleted_data', 'products.json')
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            try:
                data = json.load(f)

            except json.JSONDecodeError:
                data = []

    else:
        data = []

    data.append(instance_data)

    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)


@receiver(post_save, sender=Product)
def product_post_save(sender, instance, created, **kwargs):
    if created:
        subject: str = 'Product Created'
        message: str = f'Dear user {instance.name} was created.'
        from_email: str = 'razzoqovbunyod33@gmail.com'
        recipient_list: list = [user.email for user in User.objects.all()]

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False
        )


post_save.connect(product_post_save, sender=Product)


@receiver(post_save, sender=Category)
def category_post_save(sender, instance, created, **kwargs):
    """Bu yerda category modeliga object qoshganda barcha userlar emailiga qoshilganligi haqida xabar bilan qoshilgan category ni imageni yuboradi"""
    if created:
        subject: str = 'Category Created'
        message: str = f'Dear user {instance.title} was created.\n'
        from_email: str = 'razzoqovbunyod33@gmail.com'
        recipient_list: list = [user.email for user in User.objects.all()]
        email = EmailMessage(subject, message, from_email=from_email, to=recipient_list)
        if instance.image:
            with instance.image.open() as img_file:
                content_type, _ = mimetypes.guess_type(instance.image.name)
                email.attach(instance.image.name, img_file.read(), content_type)
        email.send()


post_save.connect(category_post_save, sender=Category)

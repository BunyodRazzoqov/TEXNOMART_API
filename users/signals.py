import json
import os
from django.db.models.signals import pre_delete
from users.models import User
from django.dispatch import receiver
from config.settings import BASE_DIR
from datetime import datetime


@receiver(pre_delete, sender=User)
def category_pre_delete(sender, instance, **kwargs):
    if instance.image:
        instance_data = {
            'id': instance.id,
            'email': instance.email,
            'username': instance.username,
            'image': instance.image.url,
            'date_of_birth': str(instance.date_of_birth),
            'deleted': str(datetime.now()),
        }
    else:
        instance_data = {
            'id': instance.id,
            'email': instance.email,
            'username': instance.username,
            'date_of_birth': str(instance.date_of_birth),
            'deleted': str(datetime.now()),
        }
    json_file_path = os.path.join(BASE_DIR, 'users', 'deleted_data', 'users.json')
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

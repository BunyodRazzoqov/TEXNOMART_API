from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from users.models import User


# Register your models here.


# @admin.register(User)
class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'admin_image', 'last_login', 'is_superuser', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('email', 'username')

    def admin_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 40px; height: auto;" />', obj.image.url)

    admin_image.short_description = 'Image'


admin.site.register(User, UserAdmin)

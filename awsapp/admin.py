from django.contrib import admin

# Register your models here.

from .models import Image,Instance

admin.site.register(Image)
admin.site.register(Instance)

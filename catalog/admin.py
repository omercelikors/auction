from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(Item)
admin.site.register(UserConfig)
admin.site.register(ItemUser)
from django.contrib import admin

# Register your models here.
from .models import MLModel

admin.site.register(MLModel)

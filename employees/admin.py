from django.contrib import admin
from django.contrib.admin import register
from .models import *
# Register your models here.

admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Employee)
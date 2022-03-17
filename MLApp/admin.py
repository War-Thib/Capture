from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import User,Labellized_Images, MLalgorithm

admin.site.register(User)
admin.site.register(Labellized_Images)
admin.site.register(MLalgorithm)
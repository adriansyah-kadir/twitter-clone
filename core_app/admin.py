from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Profile)
admin.site.register(models.Comment)
admin.site.register(models.Tweet)
admin.site.register(models.Media)
admin.site.register(models.Relation)

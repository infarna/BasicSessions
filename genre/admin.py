from django.contrib import admin
from . import models
class GenreFellowInline(admin.TabularInline):
    model = models.GenreFellow
admin.site.register(models.Genre)
#admin.site.register(models.GenreFellow)
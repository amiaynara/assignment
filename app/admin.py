from django.contrib import admin

# Register your models here.
from app.models import Analysis, File

admin.site.register(File)
admin.site.register(Analysis)
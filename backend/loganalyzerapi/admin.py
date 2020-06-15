from django.contrib import admin

# Register your models here.
from .models import LogMaster, LogFile, LogDetail
admin.site.register({LogMaster, LogFile, LogDetail})
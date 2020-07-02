from django.contrib import admin

# Register your models here.
from .models import LogMaster, LogFile, LogDetail, LogFormat, LogFormatString
admin.site.register({LogMaster, LogFile, LogDetail, LogFormat, LogFormatString})
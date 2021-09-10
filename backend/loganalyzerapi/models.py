import uuid
from datetime import datetime
from django.db import models
from postgres_copy import CopyManager

def upload_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<yymmdd>/<project_name>/<filename>
    return '{0}/{1}/{2}'.format(datetime.now().strftime('%Y%m%d'), instance.project, filename)

class LogMaster(models.Model):
    
    # PK
    project_id = models.UUIDField(verbose_name="pid",primary_key=True, default=uuid.uuid4, editable=False)
    project_name = models.CharField(max_length=50, null=False, blank=False)
    project_description = models.TextField(max_length=300)
    
    #file_format = models.CharField(max_length=100, null=False, blank=False)
    creator = models.CharField(max_length=50, null=False, blank=False)
    created = models.DateTimeField(auto_now=True, verbose_name="date create")
    
    def __str__(self):
        return self.project_name

    class Meta:
        ordering = ['created']
        
# 복수개의 파일이 존재한다.        
class LogFile(models.Model):
    
    # _id 자동으로 붙는다. -> PK를 생성한다.(logfile과 logdetail관계)
    # PK
    logfile_id = models.UUIDField(verbose_name="fid",primary_key=True, default=uuid.uuid4, editable=False)   
    project = models.ForeignKey(LogMaster, on_delete=models.CASCADE)    
    file_name = models.CharField(max_length=100, blank=True, default='')    
    file_object = models.FileField(upload_to=upload_directory_path)
    file_format = models.CharField(max_length=400, null=False, blank=False)
    
    format_kind = models.CharField(max_length=50, null=True, blank=False)
    format_name = models.CharField(max_length=50, null=True, blank=False)
    
    file_size = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now=True, verbose_name="date create")
    
    # multiple-instance
    server_name = models.CharField(max_length=50, null=True, blank=False)
    instance_name = models.CharField(max_length=50, null=True, blank=False)
    
    def __str__(self):
        return self.file_name

    class Meta:
        ordering = ['created']
        
class LogDetail(models.Model):
    
    # _id 자동으로 붙는다.
    # project = models.ForeignKey(LogMaster, on_delete=models.CASCADE)
    
    # PK
    logdetail_id = models.UUIDField(verbose_name="did",primary_key=True, default=uuid.uuid4, editable=False) 
    logfile = models.ForeignKey(LogFile, on_delete=models.CASCADE)
    log_line = models.CharField(max_length=1000, null=True, blank=True)
    
    # Filters
    fyear = models.CharField(max_length=4, null=True, blank=True)
    fmonth = models.CharField(max_length=2, null=True, blank=True)
    fday = models.CharField(max_length=2, null=True, blank=True)
    
    fhour = models.CharField(max_length=2, null=True, blank=True)
    fminute = models.CharField(max_length=2, null=True, blank=True)
    fsecond = models.CharField(max_length=2, null=True, blank=True)
    
    fdate = models.CharField(max_length=8, null=True, blank=True)
    ftime = models.CharField(max_length=6, null=True, blank=True)    
    fdatetime = models.CharField(max_length=14, null=True, blank=True)    
    
    frequest = models.CharField(max_length=500, null=True, blank=True)
    fip = models.CharField(max_length=40, null=True, blank=True)
    freferer = models.CharField(max_length=500, null=True, blank=True)
    fuser_agent = models.CharField(max_length=500, null=True, blank=True)
    fstatus = models.CharField(max_length=10, null=True, blank=True)
    ftime_taken = models.BigIntegerField(default=0)
    
    # Add Filters
    fbyte = models.IntegerField(default=0)
    fextension = models.CharField(max_length=10, null=True, blank=True)
    
    # Reservation Fields
    freserve1 = models.CharField(max_length=500, null=True, blank=True)
    freserve2 = models.CharField(max_length=500, null=True, blank=True)
    freserve3 = models.CharField(max_length=500, null=True, blank=True)
    
    created = models.DateTimeField(auto_now=True, verbose_name="date create")   
    
    # For Mass Insert Logs
    objects = CopyManager()
    
    def __str__(self):
        return str(self.project_id)

    class Meta:
        ordering = ['created']
    
class LogFormat(models.Model):
    # PK
    format_id = models.UUIDField(verbose_name="fid",primary_key=True, default=uuid.uuid4, editable=False)
    format_kind = models.CharField(max_length=50, null=False, blank=False)
    format_name = models.CharField(max_length=50, null=False, blank=False)
    format_strings = models.CharField(max_length=500, null=False, blank=False)
    creator = models.CharField(max_length=50, null=False, blank=False)
    created = models.DateTimeField(auto_now=True, verbose_name="date create")
    
    class Meta:
        ordering = ['created']

    def __str__(self): 
        return str(self.format_id   )

class LogFormatString(models.Model):
    # PK
    formatstring_id = models.UUIDField(verbose_name="fsid",primary_key=True, default=uuid.uuid4, editable=False)
    format_kind = models.CharField(max_length=50, null=False, blank=False)
    format_string = models.CharField(max_length=50, null=False, blank=False)
    format_definition = models.CharField(max_length=500, null=False, blank=False)
    created = models.DateTimeField(auto_now=True, verbose_name="date create")
    
    class Meta:
        ordering = ['created']

    def __str__(self): 
        return str(self.formatstring_id)


class Metrics(models.Model):
    # PK
    metric_id = models.UUIDField(verbose_name="mid",primary_key=True, default=uuid.uuid4, editable=False)
    metric_kind = models.CharField(max_length=10, null=False, blank=False)
    metric_type = models.CharField(max_length=10, null=False, blank=False, default='Info')
    metric_definition = models.CharField(max_length=500, null=False, blank=False)
    metric_filter = models.CharField(max_length=500, null=False, blank=False)
    metric_filter2 = models.CharField(max_length=10, null=False, blank=False, default='0')
    metric_unit = models.CharField(max_length=10, null=False, blank=False)
    metric_value1 = models.CharField(max_length=100, null=True, blank=True)
    metric_value2 = models.CharField(max_length=100, null=True, blank=True)
    metric_static = models.CharField(max_length=1, null=False, blank=False)
    creator = models.CharField(max_length=50, null=False, blank=False)
    created = models.DateTimeField(auto_now=True, verbose_name="date create")
    
    class Meta:
        ordering = ['created']

    def __str__(self): 
        return str(self.metric_id)


class LogMasterMetric(models.Model):
    # PK
    logmastermetric_id = models.UUIDField(verbose_name="lmid",primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(LogMaster, on_delete=models.CASCADE)
    metric = models.ForeignKey(Metrics, on_delete=models.CASCADE)
    creator = models.CharField(max_length=50, null=False, blank=False)
    created = models.DateTimeField(auto_now=True, verbose_name="date create")
    
    class Meta:
        unique_together = ('project', 'metric')
        ordering = ['created']

    def __str__(self): 
        return str(self.logmastermetric_id)
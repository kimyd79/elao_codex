import uuid
from datetime import datetime
from django.db import models
from postgres_copy import CopyManager

def upload_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<yymmdd>/<project_name>/<filename>
    return '{0}/{1}/{2}'.format(datetime.now().strftime('%Y%m%d'), instance.project_name, filename)

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
        
def upload_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<yymmdd>/<project_name>/<filename>
    return '{0}/{1}/{2}'.format(datetime.now().strftime('%Y%m%d'), instance.project, filename)        


# 복수개의 파일이 존재한다.        
class LogFile(models.Model):
    
    # _id 자동으로 붙는다. -> PK를 생성한다.(logfile과 logdetail관계)
    # PK
    logfile_id = models.UUIDField(verbose_name="fid",primary_key=True, default=uuid.uuid4, editable=False)   
    project = models.ForeignKey(LogMaster, on_delete=models.CASCADE)    
    file_name = models.CharField(max_length=100, blank=True, default='')    
    file_object = models.FileField(upload_to=upload_directory_path)
    file_format = models.CharField(max_length=100, null=False, blank=False)
    file_size = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now=True, verbose_name="date create")
    
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
    ftime_taken = models.SmallIntegerField(default=0)
    
    # Reservation Fields
    freserve1 = models.CharField(max_length=200, null=True, blank=True)
    freserve2 = models.CharField(max_length=200, null=True, blank=True)
    freserve3 = models.CharField(max_length=200, null=True, blank=True)
    
    created = models.DateTimeField(auto_now=True, verbose_name="date create")   
    
    # For Mass Insert Logs
    objects = CopyManager()
    
    def __str__(self):
        return self.project_id

    class Meta:
        ordering = ['created']
    
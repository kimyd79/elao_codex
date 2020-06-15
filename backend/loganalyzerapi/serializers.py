from rest_framework import serializers
from loganalyzerapi.models import LogMaster, LogFile, LogDetail

class LogMasterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LogMaster
        fields = '__all__'
        
class LogFileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LogFile
        fields = '__all__'
        
class LogDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LogDetail
        fields = '__all__' #('log_line','logfile')
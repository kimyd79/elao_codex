from rest_framework import serializers
from loganalyzerapi.models import LogMaster, LogFile, LogDetail, LogFormat, LogFormatString, Metrics, LogMasterMetric
from django.contrib.auth.models import User

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
        fields = '__all__'
        
class LogFormatSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LogFormat
        fields = '__all__'

class LogFormatStringSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LogFormatString
        fields = '__all__'  

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'   
        
class DynamicLogDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = None
        fields = '__all__' 

class MetricsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Metrics
        fields = '__all__' 

class LogMasterMetricSerializer(serializers.ModelSerializer):
    # project = LogMasterSerializer(read_only=True)
    
    class Meta:
        model = LogMasterMetric
        fields = '__all__' 

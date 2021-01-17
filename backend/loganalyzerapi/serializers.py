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

    # project = LogMasterSerializer(read_only=False)
    # project_name = serializers.RelatedField(source='logmaster.name', read_only=True)
    # project_name = serializers.ReadOnlyField(source='logmaster.project_name')
    # project_name = LogMasterSerializer(many=True,read_only=False)
    project_name = serializers.CharField(source='project.project_name', read_only=True)
    metric_kind = serializers.CharField(source='metric.metric_kind', read_only=True)
    metric_definition = serializers.CharField(source='metric.metric_definition', read_only=True)
    metric_filter = serializers.CharField(source='metric.metric_filter', read_only=True)
    metric_unit = serializers.CharField(source='metric.metric_unit', read_only=True)
    metric_min = serializers.CharField(source='metric.metric_min', read_only=True)
    metric_max = serializers.CharField(source='metric.metric_max', read_only=True)

    
    class Meta:
        model = LogMasterMetric
        # fields = '__all__' 
        fields = ['logmastermetric_id', 'metric', 'project', 'project_name', 'creator', 'created','metric_kind', 'metric_definition', 'metric_filter', 'metric_unit', 'metric_min', 'metric_max'] 


# class LogMasterMetricJoinSerializer(serializers.ModelSerializer):
#     project = LogMasterSerializer(read_only=True)
#     # project_name = serializers.ReadOnlyField(source='logmaster.project_name')
    
#     class Meta:
#         model = LogMasterMetric
#         fields = '__all__' 
#         # fields = ['logmastermetric_id', 'metric', 'project', 'project_name', 'creator', 'created']  

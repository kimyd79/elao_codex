from rest_framework import serializers
from loganalyzerapi.models import LogMaster, LogFile, LogDetail, LogDetailV2, LogFormat, LogFormatString, Metrics, LogMasterMetric, LogAnalysisJob
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


class LogAnalysisJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogAnalysisJob
        fields = '__all__'
        read_only_fields = (
            'job_id', 'status', 'source_count', 'parsed_count',
            'rejected_count', 'stored_count', 'error_message',
            'started', 'finished', 'created', 'updated',
            'run_id', 'phase', 'processed_units', 'total_units', 'progress_unit',
        )


class LogDetailV2Serializer(serializers.ModelSerializer):
    class Meta:
        model = LogDetailV2
        fields = '__all__'
        read_only_fields = ('log_id', 'created')
        
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
    project_name = serializers.CharField(source='project.project_name', read_only=True)
    metric_kind = serializers.CharField(source='metric.metric_kind', read_only=True)
    metric_definition = serializers.CharField(source='metric.metric_definition', read_only=True)
    metric_filter = serializers.CharField(source='metric.metric_filter', read_only=True)
    metric_unit = serializers.CharField(source='metric.metric_unit', read_only=True)
    metric_min = serializers.IntegerField(source='metric.metric_min', read_only=True)
    metric_max = serializers.IntegerField(source='metric.metric_max', read_only=True)
    metric_static = serializers.CharField(source='metric.metric_static', read_only=True)


    
    class Meta:
        model = LogMasterMetric
        # fields = '__all__' 
        fields = ['logmastermetric_id', 'metric', 'project', 'project_name', 'creator', 'created','metric_kind', 'metric_definition', 'metric_filter', 'metric_unit', 'metric_min', 'metric_max', 'metric_static'] 

from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import viewsets, status
from rest_framework.renderers import JSONRenderer
from loganalyzerapi.models import LogMaster, LogFile, LogDetail, LogFormat, LogFormatString, Metrics, LogMasterMetric
from loganalyzerapi.serializers import LogMasterSerializer, LogDetailSerializer, LogFileSerializer, LogFormatSerializer, LogFormatStringSerializer, UserSerializer, DynamicLogDetailSerializer, MetricsSerializer, LogMasterMetricSerializer
import time, uuid, re, csv, io

from datetime import datetime, timezone
from rest_framework.response import Response
from django.db import transaction
import pandas as pd
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum, Max, Min, Avg, F, Value
from django.db.models.functions import Concat, Coalesce, Substr, StrIndex, Length
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import QueryDict
import os
from postgres_copy import CopyManager
import copy
import numpy as np
from zipfile import ZipFile
import gzip
import math
import multiprocessing
import asyncio
from multiprocessing import Process, Queue
from threading import Thread

from dynamic_models.models import ModelSchema, FieldSchema
from django.apps import apps

from django.conf import settings
import logging
logger = logging.getLogger(__name__)
    
# 기본 CRUD생성
class LogMasterViewSet(viewsets.ModelViewSet):
    queryset = LogMaster.objects.all()
    serializer_class = LogMasterSerializer
    
    # 검색관련
    # filterset_fields 사용시 복합조건 쿼리 가능
    # filterset_fields = ['category', 'in_stock']
    # -> http://example.com/api/products?category=clothing&in_stock=True
    #
    # SearchFilter 는 simple single query paramete 만 가능
    # 복합쿼리 사용하지 않음
    # Multiple Search
    # http://127.0.0.1:8000/logmaster/?search=aa,22
    
    #filterset_fields = ['project_name', 'uploader']
    #filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['creator', 'project_name']
    search_fields = ['project_name']
    # Multiple Search
    # http://127.0.0.1:8000/logmaster/?search=aa,22
    #search_fields = ['project_name', 'project_description', 'creator']
    
    #ordering_fields = ['project_name', 'project_description', 'created']
    #ordering = ['created']
    
    # Multiple Order
    # http://127.0.0.1:8000/logmaster/?ordering=project_name,-created
    
    # search + pagination + ordering
    # http://127.0.0.1:8000/logmaster/?search=te&ordering=-created&limit=10&offset=1
    
    # Project 단위로 logdetail 테이블을 생성 : logdetail_"project_id"
    # http://127.0.0.1:8000/logmaster/create_dynamic_logdetail
    @action(methods=['post'], detail=False)
    def create_dynamic_logdetail(self, request, pk=None):
        
        try:
            project_id = request.data['project_id']
                    
            print('create_dynamic_logdetail project_id : ', project_id)
            
            # TODO: 동적테이블 생성
            model_name = "logdetail_"+project_id
            
            logdetail_schema = ModelSchema.objects.create(name=model_name)
            
            ########################################################################################
            # Field정의 start
            # PK
            # logdetail_id = models.UUIDField(verbose_name="did",primary_key=True, default=uuid.uuid4, editable=False) 
            # logfile = models.ForeignKey(LogFile, on_delete=models.CASCADE)
            # log_line = models.CharField(max_length=1000, null=True, blank=True)
            
            # id 필드로 대체 : logdetail_id
            # ForeignKey 제외 : logfile
            logfile_id = FieldSchema.objects.create(model_schema=logdetail_schema, name='logfile_id', data_type='character', max_length=64, null=True)
            log_line = FieldSchema.objects.create(model_schema=logdetail_schema, name='log_line', data_type='character', max_length=1000, null=True)
            
            # # Filters
            fyear = FieldSchema.objects.create(model_schema=logdetail_schema, name='fyear', data_type='character', max_length=4, null=True)
            fmonth = FieldSchema.objects.create(model_schema=logdetail_schema, name='fmonth', data_type='character', max_length=2, null=True)
            fday = FieldSchema.objects.create(model_schema=logdetail_schema, name='fday', data_type='character', max_length=2, null=True)
            
            fhour = FieldSchema.objects.create(model_schema=logdetail_schema, name='fhour', data_type='character', max_length=2, null=True)
            fminute = FieldSchema.objects.create(model_schema=logdetail_schema, name='fminute', data_type='character', max_length=2, null=True)
            fsecond = FieldSchema.objects.create(model_schema=logdetail_schema, name='fsecond', data_type='character', max_length=2, null=True)
            
            fdate = FieldSchema.objects.create(model_schema=logdetail_schema, name='fdate', data_type='character', max_length=8, null=True)
            ftime = FieldSchema.objects.create(model_schema=logdetail_schema, name='ftime', data_type='character', max_length=6, null=True)
            fdatetime = FieldSchema.objects.create(model_schema=logdetail_schema, name='fdatetime', data_type='character', max_length=14, null=True)
            
            frequest = FieldSchema.objects.create(model_schema=logdetail_schema, name='frequest', data_type='character', max_length=500, null=True)
            fip = FieldSchema.objects.create(model_schema=logdetail_schema, name='fip', data_type='character', max_length=40, null=True)
            freferer = FieldSchema.objects.create(model_schema=logdetail_schema, name='freferer', data_type='character', max_length=500, null=True)
            fuser_agent = FieldSchema.objects.create(model_schema=logdetail_schema, name='fuser_agent', data_type='character', max_length=500, null=True)
            fstatus = FieldSchema.objects.create(model_schema=logdetail_schema, name='fstatus', data_type='character', max_length=10, null=True)
            
            # ftime_taken = models.IntegerField(default=0)
            ftime_taken = FieldSchema.objects.create(model_schema=logdetail_schema, name='ftime_taken', data_type='float', null=True)
            
            fbyte = FieldSchema.objects.create(model_schema=logdetail_schema, name='fbyte', data_type='integer', null=True)
            fextension = FieldSchema.objects.create(model_schema=logdetail_schema, name='fextension', data_type='character', max_length=10, null=True)
            
            # # Reservation Fields
            freserve1 = FieldSchema.objects.create(model_schema=logdetail_schema, name='freserve1', data_type='character', max_length=200, null=True)
            freserve2 = FieldSchema.objects.create(model_schema=logdetail_schema, name='freserve2', data_type='character', max_length=200, null=True)
            freserve3 = FieldSchema.objects.create(model_schema=logdetail_schema, name='freserve3', data_type='character', max_length=200, null=True)
            
            # created = models.DateTimeField(auto_now=True, verbose_name="date create")
            created = FieldSchema.objects.create(model_schema=logdetail_schema, name='created', data_type='date', null=True) 
            
            # Field정의 end
            ########################################################################################            
            
            logdetail_dynamic = logdetail_schema.as_model() # LogDetail       
            logdetail_dynamic.objects.create()
            
            # For postgresql copy            
            # logdetail_dynamic.objects = CopyManager()                       
            
            response = {'message': 'Dynamic LogDetail created successfully', 'model_name': model_name}        
            return Response(response, status = status.HTTP_200_OK)
            
        except Exception as ex:
            print('Error Occured while creating Dynamic LogDetail...', ex)
                    
            response = {'message': 'Dynamic LogDetail creation failed.'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)  
        
    # Project 삭제시 detail 테이블도 삭제 : Logfile은 cascading 삭제
    # http://127.0.0.1:8000/logmaster/delete_dynamic_logdetail
    @action(methods=['post'], detail=False)
    def delete_dynamic_logdetail(self, request, pk=None):

        try:
            
            project_id = request.data['project_id']
            
            print('delete_logdetail project_id : %s' % project_id)            
            
            # Table Name : "loganalyzerapi_logdetail_"+ this.project.project_id.replace("-","_");
            # Ex : loganalyzerapi_logdetail_1218aca3_e9b4_4fea_be5d_38fb58421496
            
            if settings.DEBUG:
    	        logger.debug('delete_logdetail project_id : %s' % project_id)
                                   
            model_name = "logdetail_"+project_id

            # 삭제한다. 존재하는지 확인, 없으면 그냥 리턴
            try:
                ModelSchema.objects.get(name=model_name).delete()
                
            except Exception as ex:
                # detail이 존재하지 않을 경우 
                logger.error('There is no model named : '+model_name+' - %s' % ex)
            
            response = {'message': 'delete_logdetail returned successfully', 'result': 'true'}
            return Response(response, status = status.HTTP_200_OK)
            
        except Exception as ex:
            logger.error('Error Occured while deleting model_name : %s' % ex)
                    
            response = {'message': 'delete_logdetail deletion failed.', 'result': 'false'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)         

  
class LogFileViewSet(viewsets.ModelViewSet):
    queryset = LogFile.objects.all()
    serializer_class = LogFileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    
    search_fields = ['file_name']    
    filterset_fields = ['project']    
    
    '''
    '^' Starts-with search.
    '=' Exact matches.
    '@' Full-text search. (Currently only supported Django's PostgreSQL backend.)
    '$' Regex search. : default
    '''   

class LogFormatViewSet(viewsets.ModelViewSet):
    queryset = LogFormat.objects.all()
    serializer_class = LogFormatSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['format_kind']
    

class LogFormatStringViewSet(viewsets.ModelViewSet):
    queryset = LogFormatString.objects.all()
    serializer_class = LogFormatStringSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['format_kind']

    @action(methods=['get'], detail=False)
    def formatkind_list(self, request, pk=None):
        try:            
            formatkinds = LogFormatString.objects.values('format_kind').distinct().order_by('format_kind')
            list_format_kind = []
            
            for formatkind in formatkinds:
                list_format_kind.append(formatkind['format_kind'])
            
            response = {'message': 'list_format_kind returned successfully', 'list_format_kind': list_format_kind}        
            return Response(response, status = status.HTTP_200_OK)
            
        except Exception as ex:
            logger.error('Error Occured while processing list_format_kind : %s' % ex)
                    
            response = {'message': 'list_format_kind creation failed.'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]   

    @action(methods=['post'], detail=False)
    def active(self, request, pk=None):
        try:    
            username = request.data['username']       
            user = User.objects.get(username=username)

            user.is_active = False
            user.save()
           
            response = {'message': 'is_active is set to false successfully', 'username': user.username}        
            return Response(response, status = status.HTTP_200_OK)
            
        except Exception as ex:
            logger.error('Error Occured while processing is_active : %s' % ex)
                    
            response = {'message': 'is_active setting failed.'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)    

# Dynamic Model
class DynamicLogDetailViewSet(viewsets.ModelViewSet):
    
    # For GridTable
    def retrieve(self, request, *args, **kwargs):
        
        if settings.DEBUG:
        	logger.debug("DynamicLogDetailViewSet : %s !!" % "retrieve" )
         
        #print("== DynamicLogDetailViewSet retrieve!!")
        
        return super().retrieve(request, *args, **kwargs)
    
    def get_queryset(self):
        
        if settings.DEBUG:
           	logger.debug("DynamicLogDetailViewSet : %s !!" % "retrieve" )
          
        #print("== DynamicLogDetailViewSet get_queryset!!")
         
        # Request Method 확인
        method = ""
        for key in self.action_map:
            if self.action_map[key] == self.action:
                method = key
                break        
        
        dateFromValue = ""
        dateToValue = ""
        timeFromValue = ""
        timeToValue = ""
        ttFromValue = ""
        ttToValue = ""
        conditionValue = ""
        searchValue = ""
        project_id = ""
        
        #statistic detailpopup
        detailconditionValue = ""
        detailsearchValue = ""

        #findings detailpopup
        byteFromValue = ""
        byteToValue = ""
        staticValue = ""

        # 조건 적용(GET)
        if method == 'get' :

            orig_query = self.request.META['QUERY_STRING']
            if orig_query is not None:
                self.request.GET = QueryDict(orig_query.replace(";","%3B"))

            dateFromValue = self.request.query_params.get('dateFromValue', None)
            dateToValue = self.request.query_params.get('dateToValue', None)
            timeFromValue = self.request.query_params.get('timeFromValue', None)
            timeToValue = self.request.query_params.get('timeToValue', None)
            
            ttFromValue = self.request.query_params.get('ttFromValue', None)
            ttToValue = self.request.query_params.get('ttToValue', None)
            
            conditionValue = self.request.query_params.get('conditionValue', None)
            searchValue = self.request.query_params.get('searchValue', None)
            
            project_id = self.request.query_params.get('project_id', None)
            
            #statistic detailpopup
            detailconditionValue = self.request.query_params.get('detailconditionValue', None)
            detailsearchValue = self.request.GET.get('detailsearchValue', None)

            #findings detailpopup
            byteFromValue = self.request.query_params.get('byteFromValue', None)
            byteToValue = self.request.query_params.get('byteToValue', None)
            staticValue = self.request.query_params.get('staticValue', None)

        
        elif method == 'post':
            
            dateFromValue = self.request.data['filter']['dateFromValue'] if self.request.data['filter']['dateFromValue'] != '' else None
            dateToValue = self.request.data['filter']['dateToValue'] if self.request.data['filter']['dateToValue'] != '' else None
            timeFromValue = self.request.data['filter']['timeFromValue'] if self.request.data['filter']['timeFromValue'] != '' else None
            timeToValue = self.request.data['filter']['timeToValue'] if self.request.data['filter']['timeToValue'] != '' else None

            ttFromValue = self.request.data['filter']['ttFromValue'] if self.request.data['filter']['ttFromValue'] != '' else None
            ttToValue = self.request.data['filter']['ttToValue'] if self.request.data['filter']['ttToValue'] != '' else None

            conditionValue = self.request.data['filter']['conditionValue'] if self.request.data['filter']['conditionValue'] != '' else None
            searchValue = self.request.data['filter']['searchValue'] if self.request.data['filter']['searchValue'] != '' else None
            
            project_id = self.request.data['filter']['project_id'] if self.request.data['filter']['project_id'] != '' else None
    
        # Dynamic Model 처리    
        # project_id = self.request.data['project_id']
        model_name = "logdetail_"+project_id
         
        if settings.DEBUG:
            logger.debug("get_queryset model_name : %s !!" % model_name )
         
        LogDetail_dynamic = ModelSchema.objects.get(name=model_name).as_model()
        
        # Default : orderby id(PK)
        #queryset = LogDetail_dynamic.objects.all()
        queryset = LogDetail_dynamic.objects.order_by('id')
        
        timeTakenUnit = ""            
        # 관련 project만 가져온다. : multifile 처리
        if project_id is not None:        
            logfiles = LogFile.objects.filter(project_id=project_id).values('logfile_id')            
            list_logfile_id = []         
            
            # logfile id 가져오기
            for logfile in logfiles:
                list_logfile_id.append(str(logfile['logfile_id']))
                # timeTakenUnit 가져오기
                timeTakenUnit = self.getTimetakenUnit(str(logfile['logfile_id']))                
            
            queryset = queryset.filter(logfile_id__in=list_logfile_id)
        
        # Date, Time : Between
        if (dateFromValue is not None) and (dateToValue is not None) and (timeFromValue is not None) and (timeToValue is not None):
            start_datetime = dateFromValue + timeFromValue
            end_datetime = dateToValue + timeToValue
            queryset = queryset.filter(fdatetime__range=(start_datetime, end_datetime))
            
            if settings.DEBUG:
                logger.debug('Date and Time applied!')
        
        # Time-taken : Between
        if (ttFromValue is not None) and (ttToValue is not None):
            # Time Unit 구분 : %T -> ms / 1000, %D (micros) -> ms * 1000            
            if timeTakenUnit == 'D':        # microsecond
                ttFromValue = int(ttFromValue) * 1000
                ttToValue   = int(ttToValue) * 1000                 
            elif timeTakenUnit == 'T':      # second
                ttFromValue = int(ttFromValue) / 1000
                ttToValue = int(ttToValue) / 1000
            # IIS, Nginx : ms 단위이므로 환산이 불필요하다.
                    
            queryset = queryset.filter(ftime_taken__range=(ttFromValue, ttToValue))
            
            if settings.DEBUG:
                logger.debug('Time-taken applied!')
            
        # conditionValue : Contain
        if conditionValue is not None :
            
            if settings.DEBUG:                
                logger.debug('conditionValue applied! (conditionValue) : %s' % conditionValue)
                logger.debug('searchValue : %s' % searchValue)
                
            if conditionValue == 'I':
                queryset = queryset.filter(fip__icontains=searchValue)
            elif conditionValue == 'R':
                queryset = queryset.filter(frequest__icontains=searchValue)
            elif conditionValue == 'E':
                queryset = queryset.filter(freferer__icontains=searchValue)
            elif conditionValue == 'U':
                queryset = queryset.filter(fuser_agent__icontains=searchValue)
            elif conditionValue == 'S':
                queryset = queryset.filter(fstatus__icontains=searchValue)    
        
        # String 검색
        if conditionValue is None and searchValue is not None:
            
            if settings.DEBUG:                
                logger.debug('searchValue applied! (String Search) : %s' % searchValue)                
            
            queryset = queryset.filter(log_line__icontains=searchValue)        
                
        # conditionValue : statistic detailpopup
        if detailconditionValue is not None :
            
            if settings.DEBUG:                
                logger.debug('detailconditionValue applied! (detailconditionValue) : %s' % detailconditionValue)
                logger.debug('detailsearchValue : %s' % detailsearchValue)
            
            if detailconditionValue == 'I':
                queryset = queryset.filter(fip__icontains=detailsearchValue)
            elif detailconditionValue == 'R':
                queryset = queryset.filter(frequest__icontains=detailsearchValue)
            # 404 Requests URI (count)
            elif detailconditionValue == 'NFR':
                queryset = queryset.filter(fstatus__icontains='404')
                queryset = queryset.filter(frequest__icontains=detailsearchValue)
            elif detailconditionValue == 'E':
                queryset = queryset.filter(freferer__icontains=detailsearchValue)
            elif detailconditionValue == 'U':
                queryset = queryset.filter(fuser_agent__icontains=detailsearchValue)
            elif detailconditionValue == 'S':
                queryset = queryset.filter(fstatus__icontains=detailsearchValue)
            elif detailconditionValue == 'F':
                queryset = queryset.filter(fextension__icontains=detailsearchValue)
            elif detailconditionValue == 'V1':
                queryset = queryset.filter(freserve1__icontains=detailsearchValue)
            elif detailconditionValue == 'V2':
                queryset = queryset.filter(freserve2__icontains=detailsearchValue)
            # Findings detailpopup Staticfiles 
            # elif detailconditionValue == 'D':
            #     queryset = queryset.exclude(fextension='-')
                # queryset = queryset.filter(fextension__in=['js', 'html','ico','jpg','png','bmp','otf','css'])
                
        # staticfileconditionValue : Findings detailpopup Staticfiles 
        if staticValue is not None :
            
            if settings.DEBUG:                
                logger.debug('staticValue applied! (staticValue) : %s' % staticValue)
                logger.debug('staticValue : %s' % staticValue)
            
            if staticValue == 'T':
                queryset = queryset.exclude(fextension='-')

        # Findings detailpopup Staticfiles
        # response byte size : Between 
        # TODO: POST로 요청이 들어오면 "" 초기값 그대로 가지고 있음. 아래의 로직은 오류 발생함.(모든 차트와 통계값)
        # 원본 : if (byteFromValue is not None) and (byteToValue is not None):
        # 아래는 임시 수정이므로 전체 확인하여 처리요망
        if (byteFromValue is not None and byteFromValue != "" ) and (byteToValue is not None and byteToValue != ""):
            byteFromValue = int(byteFromValue)
            byteToValue   = int(byteToValue)
            queryset = queryset.filter(fbyte__range=(byteFromValue, byteToValue))

            if settings.DEBUG:
               logger.debug('byte between applied!')
       
        return queryset           

    def get_serializer_class(self):
        
        method = ""
        for key in self.action_map:
            if self.action_map[key] == self.action:
                method = key
                break        
         
        project_id = ""         
        if method == 'get' :            
            project_id = self.request.query_params.get('project_id', None)
        
        elif method == 'post':
            project_id = self.request.data['filter']['project_id'] if self.request.data['filter']['project_id'] != '' else None
         
        model_name = "logdetail_"+project_id
        
        if settings.DEBUG:
            logger.debug("get_serializer_class model_name : %s" % model_name)
                     
        LogDetail_dynamic = ModelSchema.objects.get(name=model_name).as_model()        
                         
        DynamicLogDetailSerializer.Meta.model = LogDetail_dynamic
        return DynamicLogDetailSerializer
     
    def getTimetakenUnit(self, logfile_id):
        file_format = LogFile.objects.get(logfile_id=logfile_id).file_format
        
        if file_format.find('D') != -1:
            return 'D'
        elif file_format.find('T') != -1:
            return 'T'
        else:
            return None


    def getMetricTimeValue(self, metric_unit, metric_time, timetakenUnit):   
        timeValue = 0    
        if timetakenUnit == 'T':      # second
            if metric_unit == 'millis':
                timeValue = round(metric_time/1000)
            elif metric_unit == 'micros':   
                timeValue = round(metric_time/1000000)
        else:                         # microsecond  
            if metric_unit == 'millis':
                timeValue = metric_time * 1000
            elif metric_unit == 'micros':   
                timeValue = metric_time

        return timeValue
           
    @action(methods=['post'], detail=False)
    def get_before_after_detail(self, request, pk=None):        
       
        try:
            project_id = request.data['project_id']
            before = int(request.data['before'])
            after = int(request.data['after'])
            logs = request.data['logs']
            results = []
            
            if settings.DEBUG:
    	        logger.debug('get_before_after_detail project_id : %s' % project_id)
            
            model_name = "logdetail_"+project_id
            LogDetail_dynamic = ModelSchema.objects.get(name=model_name).as_model()
            
            for log in logs['results']:
                
                #if settings.DEBUG:
        	    #    logger.debug("log : ", log)
                                  
                rows = LogDetail_dynamic.objects.filter(id__range=(log['id']-before, log['id']+after)).order_by('id')
                
                cnt = rows.values('id','log_line').count()
                for row in rows.values('id','log_line'):
                    
                    #if settings.DEBUG:
                    #    logger.debug("row['id'] : ", row['id'])
                    #    logger.debug("row['log_line'] : ", row['log_line'])
                    
                    cnt = cnt - 1
                    results.append({'id' : row['id'], 'log_line' : row['log_line'], 'is_main' : "true" if log['id'] == row['id'] else "false", 'is_last': "true" if cnt == 0 else "false"})
            
            response = {'message': 'get_before_after_detail returned successfully', 'results': results, 'count': len(results) }        
            return Response(response, status = status.HTTP_200_OK)
            
        except Exception as ex:
            logger.error('Error Occured while processing get_before_after_detail : %s' % ex)
                    
            response = {'message': 'get_before_after_detail creation failed.'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(methods=['post'], detail=False)
    def findings(self, request, pk=None):
        
        try:
            project_id = request.data['project_id']
            timetakenUnit = ""
            findingsResultList = []
            
            # 검색 조건 적용 TODO: 검증
            queryset_tmp = self.get_queryset()

            if settings.DEBUG:
                logger.debug('findings project_id : %s' % project_id)            
            
            # 관련 project 가져오기. : multifile 처리
            logfiles = LogFile.objects.filter(project=project_id).values('logfile_id')
            list_logfile_id = []
            
            # logfile id 가져오기
            for logfile in logfiles:
                list_logfile_id.append(str(logfile['logfile_id']))
                # timetakenUnit 가져오기
                timetakenUnit = self.getTimetakenUnit(str(logfile['logfile_id']))
            
            # project에 설정된 metric 가져오기
            metrics = LogMasterMetric.objects.filter(project_id=project_id).values('metric')

            # project에 설정된 metric id로 루프 돌면서 metric 조건 처리 
            for metric in metrics:
                metric_id = str(metric['metric'])

                metricDetail = Metrics.objects.filter(metric_id=metric_id).values()

                metric_kind = metricDetail[0]['metric_kind']
                metric_filter = metricDetail[0]['metric_filter']                
                metric_unit = metricDetail[0]['metric_unit']
                metric_value1 = metricDetail[0]['metric_value1']
                metric_value2 = metricDetail[0]['metric_value2']   
                metric_static = metricDetail[0]['metric_static']   
                
                queryset = queryset_tmp.filter(logfile_id__in=list_logfile_id)

                # Static file 조회 여부('js', 'html','ico','jpg','png','bmp','otf','css')
                if metric_static == 'Y':
                    queryset = queryset.exclude(fextension='-')
                
                # 전체건수
                totalCnt = queryset.count()
                results = []

                if metric_unit == 'millis' or metric_unit == 'micros':
                    metric_value1 = self.getMetricTimeValue(metric_unit, int(metric_value1), timetakenUnit)
                    metric_value2 = self.getMetricTimeValue(metric_unit, int(metric_value2), timetakenUnit)


                # TODO: if metric_filter 사용 회피 필요... 
                # threshold : gte (<=)
                if metric_kind == 'threshold':
                    # timetaken / byte 조회 조건
                    if metric_filter == 'ftime_taken' or metric_filter == 'fbyte':
                        queryset = queryset.values(metric_filter).filter(**{metric_filter+'__gte': metric_value1})
                        result_count = queryset.count()
                        results.append({"result" : "count", "result_value" : result_count})             

                    # annotate 조건
                    if metric_filter == 'fip' or metric_filter == 'freferer' or metric_filter == 'freserve1' or metric_filter == 'freserve2':
                        result = queryset.values(metric_filter).annotate(f_count=Count(metric_filter)).order_by('-f_count')
                        rows = result.values(metric_filter,'f_count')                       
                        for row in rows:
                            ratio = round(row['f_count']/totalCnt*100)
                            if ratio < int(metric_value1):                                
                                break                           
                            else:
                                results.append({"result" : row[metric_filter], "result_value" : str(ratio) + '%'})        

                    # status 4xx, 5xx 비율 
                    if metric_filter == 'fstatus':
                        result = queryset.values(metric_filter).filter(**{metric_filter+'__startswith': metric_unit}).annotate(f_count=Count(metric_filter)).order_by('-f_count')
                        rows = result.values(metric_filter,'f_count')
                        for row in rows:
                            ratio = round(row['f_count']/totalCnt*100)
                            if ratio < int(metric_value1):                                
                                break                           
                            else:
                                results.append({"result" : row[metric_filter], "result_value" : str(ratio) + '%'})  

                    # TODO: freserve1 서비스, IP:PORT 추출 작업 필요
                    # Nginx Ingress : Upstream Info 서비스별 호출 비율 / $proxy_upstream_name/$upstream_addr(<namespace>-<service name>-<service port>/<IP>:<port>) 
                    # Nginx Ingress : Upstream Info IP:PORT별 호출 비율 / $proxy_upstream_name/$upstream_addr(<namespace>-<service name>-<service port>/<IP>:<port>) 
                    # if metric_filter == 'freserve1':
                    #     # result_referer_domain = queryset.annotate(f_ipport=Substr('freserve1',StrIndex('freserve1', Value("/")))).values('f_ipport').annotate(ipport_count=Count('f_ipport')).order_by('-ipport_count')
                    #     # result_referer_domain = queryset.annotate(f_ipport=Substr('freserve1',StrIndex('freserve1', Value('/')),Length('freserve1')-StrIndex('freserve1', Value('/'))+1)).values('f_ipport').annotate(ipport_count=Count('f_ipport')).order_by('-ipport_count')
                    #     # result_referer_domain = queryset.annotate(f_ipport=Substr('freserve1',24,11)).values('f_ipport').annotate(f_count=Count('f_ipport')).order_by('-f_count')
                    #     rows = result.values(metric_filter,'f_count')                       
                    #     for row in rows:
                    #         ratio = round(row['f_count']/totalCnt*100)
                    #         if ratio < int(metric_value1):                                
                    #             break                           
                    #         else:
                    #             results.append({"result" : row[metric_filter], "result_value" : str(ratio) + '%'})               

                # Pattern Matching / 비율,건수:
                # frequest, fuser_agent
                elif metric_kind == 'pattern': 
                    queryset = queryset.values(metric_filter).filter(**{metric_filter+'__icontains': metric_value2})                        
                    ratio = round(queryset.count()/totalCnt*100)
                    if ratio >= int(metric_value1):                                
                        results.append({"result" : metric_value2, "result_value" : str(ratio) + '%'})                                    

                # scope : Between
                # ftime_taken, fbyte
                elif metric_kind == 'scope': 
                    # print(">>"+metric_kind+", "+metric_filter+", "+metric_value1+", "+metric_value2)
                    queryset = queryset.values(metric_filter).filter(**{metric_filter+'__range': (metric_value1, metric_value2)})
                    result_count = queryset.count()
                    results.append({"result" : "count", "result_value" : result_count})  

                
                tmp = list(metricDetail)
                # 숫자 3자리(천단위) 마다 "," 표시
                # tmp[0]['result'] = format(findingsResult, ',')  
                tmp[0]['results'] = results
                print(tmp[0]['results'])           
                findingsResultList.append(tmp[0]) 
 
            response = {'message': 'findings returned successfully', 'findingsResult': findingsResultList}        
            return Response(response, status = status.HTTP_200_OK)
            
        except Exception as ex:
            logger.error('Error Occured while processing findings : %s' % ex)
                    
            response = {'message': 'findings creation failed.'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def setDefaultMetrics(self, project_id, creator):
        
        try:
            
            # 이미 한 작업이면 디폴트 설정없이 리턴한다.
            if LogMasterMetric.objects.filter(project_id=project_id, creator=creator).count() != 0:
                return
            
            # 처음에는 전체 Metric 항목을 사용자에게 복사 - creator만 변경하여 추가
            # admin을 시스템 공통으로 해야 한다.(기준 Metric)
            # TODO: Logic 추가 - metric.metric_definition이 존재하는 것은 제외
            exist_metric_definitions = []
            for metric in Metrics.objects.filter(creator=creator):
                exist_metric_definitions.append(metric.metric_definition)
                
            
            admins = ['admin', 'Admin', 'Leehs'] 
            for metric in Metrics.objects.filter(creator__in=admins):
                #print(metric)
                
                if creator not in admins and metric.metric_definition not in exist_metric_definitions:                    
                    
                    new_metric = Metrics.objects.create(metric_kind=metric.metric_kind, metric_definition=metric.metric_definition, metric_filter=metric.metric_filter,
                    metric_unit=metric.metric_unit, metric_value1=metric.metric_value1,
                    metric_value2=metric.metric_value2, metric_static=metric.metric_static, creator=creator)
                    
                    new_metric.save()   # commit
            
            # Metrics 전체 가져와서 추가하기
            for metric in Metrics.objects.filter(creator=creator):
                logmastermetric = LogMasterMetric.objects.create(project_id=project_id, metric_id=metric.metric_id,  creator=creator)

                logmastermetric.save()
            
        except Exception as ex:
            logger.error('Error Occured while processing setDefaultMetrics : %s' % ex)
            raise
        

    @action(methods=['post'], detail=False)
    def start_end(self, request, pk=None):        
       
        try:
            project_id = request.data['project_id']
            creator = request.data['creator']
            
            if settings.DEBUG:
    	        logger.debug('start_end project_id : %s' % project_id)
            
            logfiles = LogFile.objects.filter(project_id=project_id).values('logfile_id', 'file_name')
            list_logfile_id = []
            list_file_name = []
            
            for logfile in logfiles:
                list_logfile_id.append(str(logfile['logfile_id']))
                list_file_name.append(logfile['file_name'])
            
            model_name = "logdetail_"+project_id
            LogDetail_dynamic = ModelSchema.objects.get(name=model_name).as_model()
            
            # All Period            
            tempset = LogDetail_dynamic.objects.filter(logfile_id__in=list_logfile_id).order_by('fdatetime')            
            
            firstRow = tempset.first()
            lastRow = tempset.last()
            
            # TODO: Metric을 기본 설정한다.
            self.setDefaultMetrics(project_id, creator)
            
            # Limit 30% of Total for default loading : TODO: Setting
            #limitRows = int(tempset.count() * 1)
            #lastLimitedRow = LogDetail_dynamic.objects.filter(logfile_id__in=list_logfile_id, id=limitRows).get()
            # 없을 경우 오류처리 필요, 우선 동일하게
            
            #response = {'message': 'start_end returned successfully', 'start_date': firstRow.fdate, 'start_time': firstRow.ftime, 'end_date': lastRow.fdate, 'end_time': lastRow.ftime, 'limit_end_date': lastLimitedRow.fdate, 'limit_end_time': lastLimitedRow.ftime, 'file_names': list_file_name}        
            
            # 우선 동일하게
            response = {'message': 'start_end returned successfully', 'start_date': firstRow.fdate, 'start_time': firstRow.ftime, 'end_date': lastRow.fdate, 'end_time': lastRow.ftime, 'limit_end_date': lastRow.fdate, 'limit_end_time': lastRow.ftime, 'file_names': list_file_name}
            
            return Response(response, status = status.HTTP_200_OK)
            
        except Exception as ex:
            logger.error('Error Occured while processing start_end : %s' % ex)
                    
            response = {'message': 'start_end creation failed.'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    # For Statistics
    @action(methods=['post'], detail=False)
    def statistics(self, request, pk=None):
        
        if settings.DEBUG:
    	    logger.debug("DynamicLogDetailViewSet : %s !!" % "statistics" )                
        
        try:       
            project_id = request.data['project_id']        

            type = request.data['type']
            N = request.data['N']
            intN = int(N)
            strN = str(N)
            
            queryset = None
                                
            # 검색 조건 적용
            if type != 0:
                queryset = self.get_queryset()
            else:
                model_name = "logdetail_"+project_id
                LogDetail_dynamic = ModelSchema.objects.get(name=model_name).as_model()
                queryset = LogDetail_dynamic.objects.all()

            results = []
            timetakenUnit = ""
            
            start_time = time.time()
            
            logfiles = LogFile.objects.filter(project_id=project_id).values('logfile_id')            
            list_logfile_id = []         
            
            # logfile id 가져오기
            for logfile in logfiles:    # Loop 시작구간
                list_logfile_id.append(str(logfile['logfile_id']))
                timetakenUnit = self.getTimetakenUnit(str(logfile['logfile_id']))           
            
            queryset = queryset.filter(logfile_id__in=list_logfile_id).order_by('fdatetime')
            totalCnt = queryset.count()
            
            #type=0. 전체 처리량(건수)
            if type == 0:
                if settings.DEBUG:
                    logger.debug("type0 : queryset.count() - %s" % totalCnt)
                    
                results.append({"result" : 'Total', "result_count" : totalCnt})
            
            #type=1. Status Codes Top N       
            elif type == 1:
                topn_status = queryset.values('fstatus').annotate(fstatus_count=Count('fstatus')).order_by('-fstatus_count')[0:intN]                        
                rows = topn_status.values('fstatus','fstatus_count')
                
                for row in rows:
                    
                    if settings.DEBUG:
                        logger.debug("type1 : TOP"+strN+" STATUS - %s" % row['fstatus'])
                        logger.debug("type1 : TOP"+strN+" STATUS Count - %s" % row['fstatus_count'])
                    
                    results.append({"result" : row['fstatus'], "result_count" : row['fstatus_count']})                      
            
            #type=2. Requests Top N
            elif type == 2:
                topn_request = queryset.values('frequest').annotate(frequest_count=Count('frequest')).order_by('-frequest_count')[0:intN]
                rows = topn_request.values('frequest','frequest_count')
                
                for row in rows:
                    
                    if settings.DEBUG:
                        logger.debug("type2 : TOP"+strN+"REQUEST - %s" % row['frequest'])
                        logger.debug("type2 : TOP"+strN+"REQUEST Count - %s" % row['frequest_count'])
                    
                    results.append({"result" : row['frequest'], "result_count" : row['frequest_count']})   
                        
            #type=3. 최다 404 발생 URL Top5
            elif type == 3:
                topn_404_request = queryset.filter(fstatus__startswith='404').values('frequest').annotate(frequest_404_count=Count('frequest')).order_by('-frequest_404_count')[0:intN]
                rows = topn_404_request.values('frequest','frequest_404_count')
                
                if rows.count() > 0 :
                    for row in rows:
                        
                        if settings.DEBUG:
                            logger.debug("type3 : TOP"+strN+" 404 REQUEST - %s" % row['frequest'])
                            logger.debug("type3 : TOP"+strN+" 404 REQUEST Count - %s" % row['frequest_404_count'])
                        
                        results.append({"result" : row['frequest'], "result_count" : row['frequest_404_count']}) 
                else:
                    results.append({"result" : "-", "result_count" : "0" }) 
                
            #type=4. Time-taken Top5(오래 걸린시간) -> 초(second)로 통일
            elif type == 4:
                topn_timetaken_request = queryset.order_by('-ftime_taken')[0:intN]
                rows = topn_timetaken_request.values('frequest','ftime_taken')
                
                for row in rows:
                    
                    if settings.DEBUG:
                        logger.debug("type4 : TOP"+strN+" Timtaken REQUEST - %s" % row['frequest'])
                        logger.debug("type4 : TOP"+strN+" Timtaken REQUEST Count - %s" % row['ftime_taken'])
                    
                    # 초(second)로 통일
                    duration_sec = round(row['ftime_taken']/1000000, 1) if timetakenUnit == 'D' else row['ftime_taken']
                    results.append({"result" : row['frequest'], "result_count" : duration_sec, "timetakenUnit" : 'T'})
                    
            #type=5. Visitor(Unique IP) Top5
            elif type == 5:
                topn_visitor = queryset.values('fip').annotate(fip_count=Count('fip')).order_by('-fip_count')[0:intN]
                rows = topn_visitor.values('fip','fip_count')
                
                for row in rows:
                    
                    if settings.DEBUG:
                        logger.debug("type5 : TOP"+strN+" VISITOR - %s" % row['fip'])
                        logger.debug("type5 : TOP"+strN+" VISITOR Count - %s" % row['fip_count'])
                    
                    results.append({"result" : row['fip'], "result_count" : row['fip_count']})   
            
            #type=6. Referers Top N
            elif type == 6:
                topn_referer = queryset.values('freferer').annotate(freferer_count=Count('freferer')).order_by('-freferer_count')[0:intN]
                rows = topn_referer.values('freferer','freferer_count')
                
                for row in rows:
                    
                    if settings.DEBUG:
                        logger.debug("type6 : TOP"+strN+" freferer - %s" % row['freferer'])
                        logger.debug("type6 : TOP"+strN+" freferer Count - %s" % row['freferer_count'])
                    
                    results.append({"result" : row['freferer'], "result_count" : row['freferer_count']}) 
            
            #type=7. User Agent Top N               
            elif type == 7:
                topn_useragent = queryset.values('fuser_agent').annotate(fuser_agent_count=Count('fuser_agent')).order_by('-fuser_agent_count')[0:intN]
                rows = topn_useragent.values('fuser_agent','fuser_agent_count')
                
                for row in rows:
                    
                    if settings.DEBUG:
                        logger.debug("type7 : TOP"+strN+" fuser_agent - %s" % row['fuser_agent'])
                        logger.debug("type7 : TOP"+strN+" fuser_agent Count - %s" % row['fuser_agent_count'])
                    
                    results.append({"result" : row['fuser_agent'], "result_count" : row['fuser_agent_count']})  
                    
            #type=8. URI Total Byte Top N               
            elif type == 8:
                topn_byte = queryset.values('frequest').annotate(requestURL=F('frequest'), fbyte_sum=Sum('fbyte')).order_by('-fbyte_sum')[0:intN]
                rows = topn_byte.values('requestURL','fbyte_sum')
                
                for row in rows:
                    
                    if settings.DEBUG:
                        logger.debug("type8 : TOP"+strN+" requestURL - %s" % row['requestURL'])
                        logger.debug("type8 : TOP"+strN+" fbyte_sum - %s" % row['fbyte_sum'])
                    
                    results.append({"result" : row['requestURL'], "result_count" : row['fbyte_sum']})
                    
            #type=9. Static files Top N               
            elif type == 9:
                topn_static = queryset.values('fextension').annotate(fextension_count=Count('fextension')).order_by('-fextension_count')[0:intN]
                rows = topn_static.values('fextension','fextension_count')
                
                for row in rows:
                    
                    if settings.DEBUG:
                        logger.debug("type9 : TOP"+strN+" fextension - %s" % row['fextension'])
                        logger.debug("type9 : TOP"+strN+" fextension Count - %s" % row['fextension_count'])
                    
                    results.append({"result" : row['fextension'], "result_count" : row['fextension_count']})  
                    
            #type=10. URI Average Byte Top N               
            elif type == 10:
                topn_avgbyte = queryset.values('frequest').annotate(requestURL=F('frequest'), fbyte_avg=Avg('fbyte')).order_by('-fbyte_avg')[0:intN]
                rows = topn_avgbyte.values('requestURL','fbyte_avg')
                
                for row in rows:
                    
                    if settings.DEBUG:
                        logger.debug("type10 : TOP"+strN+" requestURL - %s" % row['requestURL'])
                        logger.debug("type10 : TOP"+strN+" fbyte_avg - %s" % row['fbyte_avg'])
                    
                    results.append({"result" : row['requestURL'], "result_count" : round(row['fbyte_avg'], 1)})
                    
            #type=11. URI Average Time-taken Top N
            elif type == 11:
                topn_avg_timetaken_request = queryset.values('frequest').annotate(requestURL=F('frequest'), ftime_taken_avg=Avg('ftime_taken')).order_by('-ftime_taken_avg')[0:intN]
                rows = topn_avg_timetaken_request.values('requestURL','ftime_taken_avg')
                
                for row in rows:
                    
                    if settings.DEBUG:
                        logger.debug("type11 : TOP"+strN+" requestURL - %s" % row['requestURL'])
                        logger.debug("type11 : TOP"+strN+" ftime_taken_avg - %s" % row['ftime_taken_avg'])
                    
                    # 초(second)로 통일
                    duration_sec = round(row['ftime_taken_avg']/1000000, 1) if timetakenUnit == 'D' else row['ftime_taken_avg']
                    results.append({"result" : row['requestURL'], "result_count" : duration_sec, "timetakenUnit" : 'T'})
                    
            #type=12. Static filenames Top N               
            elif type == 12:
                
                topn_static_filenames = queryset.filter(fextension__in=['js', 'html','ico','jpg','png','bmp','otf','css']).values('frequest').annotate(frequest_count=Count('frequest')).order_by('-frequest_count')[0:intN]
                rows = topn_static_filenames.values('frequest','frequest_count')
                
                for row in rows:
                    if settings.DEBUG:
                        logger.debug("type12 : TOP"+strN+" frequest - %s" % row['frequest'])
                        logger.debug("type12 : TOP"+strN+" frequest_count %s " % row['frequest_count'])
                    
                    results.append({"result" : row['frequest'].split(' ')[1], "result_count" : row['frequest_count']})        
                    
            # type=13. Nginx Ingress : $proxy_upstream_name/$upstream_addr(<namespace>-<service name>-<service port>/<IP>:<port>) Top N
            elif type == 13:
                topn_ingress = queryset.values('freserve1').annotate(freserve1_count=Count('freserve1')).order_by('-freserve1_count')[0:intN]
                rows = topn_ingress.values('freserve1','freserve1_count')
                
                for row in rows:
                    
                    if settings.DEBUG:
                        logger.debug("type13 : TOP"+strN+" freserve1($proxy_upstream_name/$upstream_addr) - %s" % row['freserve1'])
                        logger.debug("type13 : TOP"+strN+" freserve1($proxy_upstream_name/$upstream_addr) Count - %s" % row['freserve1_count'])
                    
                    results.append({"result" : row['freserve1'], "result_count" : row['freserve1_count']})                                
        
            # type=14. Nginx Ingress : Domain Top N - Referer에서 Domain만
            elif type == 14:
                
                topn_referer_domain = queryset.values('freserve2').annotate(freserve2_count=Count('freserve2')).order_by('-freserve2_count')[0:intN]
                rows = topn_referer_domain.values('freserve2','freserve2_count')
                
                for row in rows:
                    
                    if settings.DEBUG:
                        logger.debug("type14 : TOP"+strN+" freserve2(Domain) - %s" % row['freserve2'])
                        logger.debug("type14 : TOP"+strN+" freserve2(Domain) Count - %s" % row['freserve2_count'])
                    
                    results.append({"result" : row['freserve2'], "result_count" : row['freserve2_count']})              
            
            if settings.DEBUG:
                logger.debug("== statistics (type="+str(type)+") duration(sec) : %s " % (time.time() - start_time))
            
            response = {'message': 'statistics returned', 'resultType': type, 'results': results, 'totalCnt': totalCnt}
            return Response(response, status = status.HTTP_200_OK)
        
        except Exception as ex:
            logger.error('Error Occured while creating statistics : %s' % ex)
                    
            response = {'message': 'statistics creation failed.'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    # For Statistics - chartdata    
    @action(methods=['post'], detail=False)
    def chartdata(self, request, pk=None):

        if settings.DEBUG:
    	    logger.debug("DynamicLogDetailViewSet : %s !!" % "chartdata" )
        
        try:        
            
            project_id = request.data['project_id']        
            
            type = request.data['type']
            kind = request.data['kind']
            
            # 검색 조건 적용
            queryset = self.get_queryset()
            
            # 결과 처리
            resultX = []
            resultY = []
            resultY_time = []
            resultY_time_unit = 0
                    
            resultY_200 = []
            resultY_300 = []
            resultY_400 = []
            resultY_500 = []
            
            resultY_SCode = {}
            
            start_time = time.time()
            
            #1. project_id에 연관된 logfile_id들을 가져온다.
            logfiles = LogFile.objects.filter(project_id=project_id).values('logfile_id')                        
            list_logfile_id = []         
            
            # logfile id 가져오기
            for logfile in logfiles:    # Loop 시작구간
                list_logfile_id.append(str(logfile['logfile_id']))   
        
            #2. 아래 로직을 Loop 돌린다.
            queryset = queryset.filter(logfile_id__in=list_logfile_id).order_by('fdatetime')

            # Type1 : 시(HH)기준
            #   Kind1 : request(요청) 건수(count)        
            #   Kind2 : status code 건수(count)
            #   Kind3 : time-taken 시간(max, min, count)
            
            #type=1. 시(HH)기준
            if type == '1':          

                if(kind == 1):
                    
                    hhRequest = queryset.values('fdate','fhour').order_by('fdate', 'fhour').annotate(x=Concat('fdate', 'fhour'), y=Count('frequest'))
                    rows = hhRequest.values('x','y')
                                
                    for row in rows:
                        # print("type1, kind1 : request(요청) 건수(count) x - ",row['x'])
                        # print("type1, kind1 : request(요청) 건수(count) y - ",row['y'])
                        
                        resultX.append(row['x'])
                        resultY.append(round(row['y']/3600,1))  # TPS
                        
                elif(kind == 2):
                    
                    start_time = time.time()
                    
                    hhRequest = queryset.annotate(f_date=Concat('fdate','fhour'), f_status=Substr('fstatus',1,1)).values('f_date', 'f_status').annotate(status_count=Count('f_status')).order_by('f_date')
                    rows = hhRequest.values('f_date', 'f_status', 'status_count')
                    
                    dateStatusCount = {}    # {'날짜' : { 'status_code' : 'status_count'}, '날짜' : { 'status_code' : 'status_count'}, ...}                   
                    resultStatusCode = []
                                                
                    for row in rows:
                        # print("type1, kind2 : status code 건수(count) x - ",row['f_date'])
                        # print("type1, kind2 : status code 건수(count) y - ",row['f_status'])
                        # print("type1, kind2 : status code 건수(count) y - ",row['status_count'])
                        
                        # x축 : 중복제거
                        if row['f_date'] not in resultX:
                            resultX.append(row['f_date'])
                            
                        # y축-1 : status 코드 중복제거
                        if row['f_status'] not in resultStatusCode:
                            resultStatusCode.append(row['f_status']) 
                            
                        # 전체 Map 구하기     
                        statusCount = {}               
                        statusCount[row['f_status']] = row['status_count']
                        dateStatusCount[row['f_date']] = copy.deepcopy(statusCount)
                        
                    for xDate in resultX:
                        for yStatusCode in ['2', '3', '4', '5']:
                            
                            if yStatusCode == '2':
                                if yStatusCode in dateStatusCount[xDate]:
                                    resultY_200.append(dateStatusCount[xDate][yStatusCode])
                                else:
                                    resultY_200.append(0)
                            
                            if yStatusCode == '3':
                                if yStatusCode in dateStatusCount[xDate]:
                                    resultY_300.append(dateStatusCount[xDate][yStatusCode])
                                else:
                                    resultY_300.append(0)
                            
                            if yStatusCode == '4':
                                if yStatusCode in dateStatusCount[xDate]:
                                    resultY_400.append(dateStatusCount[xDate][yStatusCode])
                                else:
                                    resultY_400.append(0)
                                    
                            if yStatusCode == '5':
                                if yStatusCode in dateStatusCount[xDate]:
                                    resultY_500.append(dateStatusCount[xDate][yStatusCode])
                                else:
                                    resultY_500.append(0)
                            
                elif(kind == 3):
                    # Step1 : logfile_id 로 Logfile 에서 Format 찾아서 %D나 %T 있는지 확인하고
                    # Step2 : 있으면 단위까지 리턴한다. 없으면 비어있는 결과로 리턴한다.
                    file_format = LogFile.objects.get(logfile_id=list_logfile_id[0]).file_format
                    # 0: None, 1 : second(%T), 2: microsecond(%D)
                    time_unit = 0
                    if file_format.find('%T') != -1:
                        time_unit = 1 
                    elif file_format.find('%D') != -1:
                        time_unit = 2
                    elif file_format.find('$request_time') != -1:
                        time_unit = 2
                    elif file_format.find('time-taken') != -1:
                        time_unit = 2
                    
                    resultY_time_unit = time_unit
                                        
                    if time_unit != 0:
                        hhRequest = queryset.values('fdate','fhour').order_by('fdate', 'fhour').annotate(x=Concat('fdate', 'fhour'), y=Count('frequest'), yt=Avg('ftime_taken'))
                        rows = hhRequest.values('x','y', 'yt')
                                    
                        for row in rows:
                            # print("type1, kind3 : request(요청) 건수(count) x - ",row['x'])
                            # print("type1, kind3 : request(요청) 건수(count) y - ",row['y'])
                            # print("type1, kind3 : time-taken(요청) 건수(count) y - ",row['yt'])
                            
                            resultX.append(row['x'])
                            resultY.append(row['y'])
                            
                            # 시간은 초단위로 환산한다.      
                            resultY_time.append(round(row['yt']/1000000, 1) if time_unit == 2 else row['yt'])
                            
                            #resultY_time.append(row['yt'])
                    else:
                        hhRequest = queryset.values('fdate','fhour').order_by('fdate', 'fhour').annotate(x=Concat('fdate', 'fhour'), y=Count('frequest'))
                        rows = hhRequest.values('x','y')
                                    
                        for row in rows:
                            # print("type1, kind3 : request(요청) 건수(count) x - ",row['x'])
                            # print("type1, kind3 : request(요청) 건수(count) y - ",row['y'])                            
                            resultX.append(row['x'])
                            resultY.append(row['y'])
            
            # Type2 : 시분(HHMM)기준                    
            #   Kind1 : request(요청) 건수(count)
            #   Kind2 : status code 건수(count)
            #   Kind3 : time-taken 시간(max, min, count) 
            elif type == '2':          
                            
                if(kind == 1):               
                    
                    hhmmRequest = queryset.values('fdate','fhour','fminute').order_by('fdate','fhour','fminute').annotate(x=Concat('fdate','fhour','fminute'), y=Count('frequest'))
                    # print("== 쿼리 시간 : ", time.time() - start_time)
                    rows = hhmmRequest.values('x','y')
                    
                    for row in rows:
                        # print("type2, kind1 : request(요청) 건수(count) x - ",row['x'])
                        resultX.append(row['x'])
                        #resultY.append(row['y'])
                        resultY.append(round(row['y']/60,1))  # TPS
                    
                elif(kind == 2):
                    
                    hhmmRequest = queryset.annotate(f_date=Concat('fdate','fhour', 'fminute'), f_status=Substr('fstatus',1,1)).values('f_date', 'f_status').annotate(status_count=Count('f_status')).order_by('f_date')
                    rows = hhmmRequest.values('f_date', 'f_status', 'status_count')
                    
                    dateStatusCount = {}    # {'날짜' : { 'status_code' : 'status_count'}, '날짜' : { 'status_code' : 'status_count'}, ...}                    
                    
                    resultStatusCode = []
                                                
                    for row in rows:
                        # print("type2, kind2 : status code 건수(count) x - ",row['f_date'])
                        # print("type2, kind2 : status code 건수(count) y - ",row['f_status'])
                        # print("type2, kind2 : status code 건수(count) y - ",row['status_count'])
                        
                        # x축 : 중복제거
                        if row['f_date'] not in resultX:
                            resultX.append(row['f_date'])
                            
                        # y축-1 : status 코드 중복제거
                        if row['f_status'] not in resultStatusCode:
                            resultStatusCode.append(row['f_status']) 
                            
                        # 전체 Map 구하기
                        statusCount = {}
                        statusCount[row['f_status']] = row['status_count']
                        dateStatusCount[row['f_date']] = copy.deepcopy(statusCount)
                        
                    for xDate in resultX:
                        for yStatusCode in ['2', '3', '4', '5']:
                            
                            if yStatusCode == '2':
                                if yStatusCode in dateStatusCount[xDate]:
                                    resultY_200.append(dateStatusCount[xDate][yStatusCode])
                                else:
                                    resultY_200.append(0)
                            
                            if yStatusCode == '3':
                                if yStatusCode in dateStatusCount[xDate]:
                                    resultY_300.append(dateStatusCount[xDate][yStatusCode])
                                else:
                                    resultY_300.append(0)
                            
                            if yStatusCode == '4':
                                if yStatusCode in dateStatusCount[xDate]:
                                    resultY_400.append(dateStatusCount[xDate][yStatusCode])
                                else:
                                    resultY_400.append(0)
                                    
                            if yStatusCode == '5':
                                if yStatusCode in dateStatusCount[xDate]:
                                    resultY_500.append(dateStatusCount[xDate][yStatusCode])
                                else:
                                    resultY_500.append(0)
                                
                elif(kind == 3):
                    # Step1 : logfile_id 로 Logfile 에서 Format 찾아서 %D나 %T 있는지 확인하고
                    # Step2 : 있으면 단위까지 리턴한다. 없으면 비어있는 결과로 리턴한다.
                    file_format = LogFile.objects.get(logfile_id=list_logfile_id[0]).file_format
                    # 0: None, 1 : second(%T), 2: microsecond(%D)
                    time_unit = 0
                    if file_format.find('%T') != -1:
                        time_unit = 1 
                    elif file_format.find('%D') != -1:
                        time_unit = 2
                    elif file_format.find('$request_time') != -1:
                        time_unit = 2
                    elif file_format.find('time-taken') != -1:
                        time_unit = 2
                    
                    resultY_time_unit = time_unit
                                        
                    if time_unit != 0:
                        hhmmRequest = queryset.values('fdate','fhour','fminute').order_by('fdate', 'fhour','fminute').annotate(x=Concat('fdate', 'fhour','fminute'), y=Count('frequest'), yt=Avg('ftime_taken'))
                        rows = hhmmRequest.values('x','y', 'yt')
                                    
                        for row in rows:
                            # print("type2, kind3 : request(요청) 건수(count) x - ",row['x'])
                            # print("type2, kind3 : request(요청) 건수(count) y - ",row['y'])
                            # print("type2, kind3 : time-taken(요청) 건수(count) y - ",row['yt'])
                            
                            resultX.append(row['x'])
                            resultY.append(row['y'])
                            #resultY_time.append(row['yt'])
                            
                            # 시간은 초단위로 환산한다.      
                            resultY_time.append(round(row['yt']/1000000, 1) if time_unit == 2 else row['yt'])
                    else:
                        hhmmRequest = queryset.values('fdate','fhour','fminute').order_by('fdate','fhour','fminute').annotate(x=Concat('fdate','fhour','fminute'), y=Count('frequest'))
                        # print("== 쿼리 시간 : ", time.time() - start_time)
                        rows = hhmmRequest.values('x','y')
                        
                        for row in rows:
                            # print("type2, kind1 : request(요청) 건수(count) x - ",row['x'])
                            resultX.append(row['x'])
                            resultY.append(row['y'])
                            
            # Type3 : 시분초(HHMMSS)기준                    
            #   Kind1 : request(요청) 건수(count)
            #   Kind2 : status code 건수(count)
            #   Kind3 : time-taken 시간(max, min, count) 
            elif type == '3':          
                            
                if(kind == 1):               
                    
                    hhmmssRequest = queryset.values('fdate','fhour','fminute','fsecond').order_by('fdate','fhour','fminute','fsecond').annotate(x=Concat('fdate','fhour','fminute','fsecond'), y=Count('frequest'))

                    rows = hhmmssRequest.values('x','y')
                    
                    for row in rows:
                        #print("type3, kind3 : request(요청) 건수(count) x - ",row['x'])
                        resultX.append(row['x'])
                        resultY.append(row['y'])    # TPS
                    
                elif(kind == 2):
                    
                    hhmmssRequest = queryset.annotate(f_date=Concat('fdate','fhour', 'fminute','fsecond'), f_status=Substr('fstatus',1,1)).values('f_date', 'f_status').annotate(status_count=Count('f_status')).order_by('f_date')
                    rows = hhmmssRequest.values('f_date', 'f_status', 'status_count')
                    
                    dateStatusCount = {}    # {'날짜' : { 'status_code' : 'status_count'}, '날짜' : { 'status_code' : 'status_count'}, ...}
                    resultStatusCode = []
                                                
                    for row in rows:
                        # print("type3, kind2 : status code 건수(count) x - ",row['f_date'])
                        # print("type3, kind2 : status code 건수(count) y - ",row['f_status'])
                        # print("type3, kind2 : status code 건수(count) y - ",row['status_count'])
                        
                        # x축 : 중복제거
                        if row['f_date'] not in resultX:
                            resultX.append(row['f_date'])
                            
                        # y축-1 : status 코드 중복제거
                        if row['f_status'] not in resultStatusCode:
                            resultStatusCode.append(row['f_status']) 
                            
                        # 전체 Map 구하기
                        statusCount = {}
                        statusCount[row['f_status']] = row['status_count']
                        dateStatusCount[row['f_date']] = copy.deepcopy(statusCount)
                        
                    for xDate in resultX:
                        for yStatusCode in ['2', '3', '4', '5']:
                            
                            if yStatusCode == '2':
                                if yStatusCode in dateStatusCount[xDate]:
                                    resultY_200.append(dateStatusCount[xDate][yStatusCode])
                                else:
                                    resultY_200.append(0)
                            
                            if yStatusCode == '3':
                                if yStatusCode in dateStatusCount[xDate]:
                                    resultY_300.append(dateStatusCount[xDate][yStatusCode])
                                else:
                                    resultY_300.append(0)
                            
                            if yStatusCode == '4':
                                if yStatusCode in dateStatusCount[xDate]:
                                    resultY_400.append(dateStatusCount[xDate][yStatusCode])
                                else:
                                    resultY_400.append(0)
                                    
                            if yStatusCode == '5':
                                if yStatusCode in dateStatusCount[xDate]:
                                    resultY_500.append(dateStatusCount[xDate][yStatusCode])
                                else:
                                    resultY_500.append(0)
                                                    
                elif(kind == 3):
                    # Step1 : logfile_id 로 Logfile 에서 Format 찾아서 %D나 %T 있는지 확인하고
                    # Step2 : 있으면 단위까지 리턴한다. 없으면 비어있는 결과로 리턴한다.
                    file_format = LogFile.objects.get(logfile_id=list_logfile_id[0]).file_format
                    # 0: None, 1 : second(%T), 2: microsecond(%D)
                    time_unit = 0
                    if file_format.find('%T') != -1:
                        time_unit = 1 
                    elif file_format.find('%D') != -1:
                        time_unit = 2
                    elif file_format.find('$request_time') != -1:
                        time_unit = 2
                    elif file_format.find('time-taken') != -1:
                        time_unit = 2
                    
                    resultY_time_unit = time_unit
                                        
                    if time_unit != 0:
                        hhmmssRequest = queryset.values('fdate','fhour','fminute','fsecond').order_by('fdate', 'fhour','fminute','fsecond').annotate(x=Concat('fdate', 'fhour','fminute','fsecond'), y=Count('frequest'), yt=Avg('ftime_taken'))
                        rows = hhmmssRequest.values('x','y', 'yt')
                                    
                        for row in rows:
                            # print("type3, kind3 : request(요청) 건수(count) x - ",row['x'])
                            # print("type3, kind3 : request(요청) 건수(count) y - ",row['y'])
                            # print("type3, kind3 : time-taken(요청) 건수(count) y - ",row['yt'])
                            
                            resultX.append(row['x'])
                            resultY.append(row['y'])
                            #resultY_time.append(row['yt'])
                            
                            # 시간은 초단위로 환산한다.      
                            resultY_time.append(round(row['yt']/1000000, 1) if time_unit == 2 else row['yt'])
                    else:
                        hhmmssRequest = queryset.values('fdate','fhour','fminute','fsecond').order_by('fdate','fhour','fminute','fsecond').annotate(x=Concat('fdate','fhour','fminute','fsecond'), y=Count('frequest'))
                        print("== 쿼리 시간 : ", time.time() - start_time)
                        rows = hhmmssRequest.values('x','y')
                        
                        for row in rows:
                            print("type3, kind3 : request(요청) 건수(count) x - ",row['x'])
                            resultX.append(row['x'])
                            resultY.append(row['y'])        
                    
            response = {'message': 'linechartdata returned successfully', 'resultX': resultX, 'resultY': resultY, 'resultY_time': resultY_time, 'resultY_time_unit': resultY_time_unit, 'resultY_200': resultY_200, 'resultY_300': resultY_300, 'resultY_400': resultY_400, 'resultY_500': resultY_500}        
            return Response(response, status = status.HTTP_200_OK)
        
        except Exception as ex:
            logger.error('Error Occured while creating chartdata : %s' % ex)
                    
            response = {'message': 'chartdata creation failed.'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
             
    def create(self, request, *args, **kwargs):
            
        if settings.DEBUG:
    	    logger.debug("DynamicLogDetailViewSet : %s !!" % "create" )

        start = time.time()
        response = {}
        
        try:
            
            logfile_id = request.data['logfile_id']
            project_id = request.data['project_id']
            
            model_name = "logdetail_"+project_id
            
            LogDetail_dynamic = ModelSchema.objects.get(name=model_name).as_model()  
           
            # id=1인 행(null 행) 삭제
            if LogDetail_dynamic.objects.count() == 1:
                LogDetail_dynamic.objects.filter(id=1).delete()
            
            # 이미 생성되어 있는지 확인
            if LogDetail_dynamic.objects.filter(logfile_id=logfile_id).count() > 0:
                response = {'message': 'Dynamic logdetail already created.'}
                
            else:                  
                        
                logfile_model = LogFile.objects.get(logfile_id=logfile_id)   
                logfile = logfile_model.file_object.file    
                
                print("logfile :", logfile)
                
                # 파일 추가를 위한 기존정보 체크
                id_startnum = 0
                if LogDetail_dynamic.objects.count() > 0:
                    id_startnum = LogDetail_dynamic.objects.all().order_by("-id")[0].id + 1
                
                # Log Parsing : postgresql copy 사용을 위해 csv파일 생성                
                # 로그 파일이 크면 분할한다.
                # 1. 압축파일인지 확인
                # 2. 압축파일이 풀면 1.5GB 이상인지 확인
                isCompressed = False
                limitFileSize = 1.5 * 1024 * 1024 * 1024
                workFileSize = 0
                
                # 1. 압축파일인지 확인(zip, gz)
                p = re.compile('(.zip|.gz)', re.DOTALL )
                if len(p.findall(logfile.name)) > 0:    # 압축 파일
                    isCompressed = True
                    workFileSize = self.get_original_filesize(logfile.name)
                else:                                   # 압축 파일 아닌 경우
                    workFileSize = logfile.size
                    
                # 2. 압축파일이 풀면 1.5GB 이상인지 확인
                workFileCount = 1   # 기본값 = 1
                resultFiles = []
                
                if workFileSize > limitFileSize:                    
                    # 분할 파일 수를 계산해야 한다.
                    workFileCount = math.ceil(workFileSize/limitFileSize)
                    
                    # 압축 해제한다.
                    target_filename = self.decompress_file(logfile.name)
                    
                    # 전체 라인 카운트(gz, zip 가능)
                    totalLines = self.get_total_lines(target_filename)
                    
                    # Target File Name
                    #target_filename = logfile.name+"_decompressed"
                    
                    # 분할 파일 수로 나누어서 작업을 순차적으로 진행 - 메모리 사용률을 줄이기 위해서
                    startTime = time.time()
                                        
                    unit = int(totalLines/workFileCount)

                    for idx in range(workFileCount):
                        resultFiles.append(self.parse_log_div(target_filename, logfile_id, id_startnum+idx*unit, unit*idx, unit, idx))
                                                            
                    print("## 분할 csv 작업완료 까지 : 총 작업 시간 - ", round((time.time() - startTime),4))   
                    
                else:
                    # 기존로직
                    #self.parse_log(logfile, logfile_id, id_startnum )
                    resultFiles.append(self.parse_log_div(logfile.name, logfile_id, id_startnum, None, None, 0))
           
                # postgresql copy 실행                
                LogDetail_dynamic.objects.model.objects = CopyManager()
                LogDetail_dynamic.objects.model = ModelSchema.objects.get(name=model_name).as_model()
                                
                #LogDetail_dynamic.objects.from_csv(logfile.name+'.csv', delimiter=',', encoding="utf-8")
                
                for filename in resultFiles:
                    LogDetail_dynamic.objects.from_csv(filename, delimiter=',', encoding="utf-8")
                    
                if settings.DEBUG:
                    logger.debug("To DB, Total Duration : %s sec" % (time.time() - start))
                
                response = {'message': 'logdetail created successfully.', 'processing_time': round(time.time() - start, 3) }
                
            return Response(response, status = status.HTTP_200_OK)
        
        except Exception as ex: 
            logger.error('Error Occured while creating logdetail : %s' % ex)
            
            response = {'message': 'logdetail creation failed.'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def parse_log_div(self, logfile_name, logfile_id, existed_row_size, skiprows, nrows, file_order):
    
        log_lines = []
        result = []
        count = 0               
        start = time.time()
        
        # Fileformat 가져온다.(from logfile DB using logfile_id)
        # 예시 : log_format = '%h %l %u %t \"%r\" %>s %b'      
        format_model = LogFile.objects.get(logfile_id=logfile_id)
        log_format = format_model.file_format
        
        # format_kind : apache, tomcat, webtob, nginx, IIS-W3C, IIS-NCSA 
        format_kind = format_model.format_kind        
        format_name = format_model.format_name
                
        # 임시 csv 파일생성 for copy to postgresql
        # For dynamic : logdetail_id -> id
        log_line_header = ['id','log_line','fhour','fminute','fsecond','fip','freferer','fuser_agent',
                           'fstatus','ftime_taken','freserve1','freserve2','freserve3','created','logfile_id',
                           'frequest','fday','fmonth','fyear','fdate','ftime','fdatetime','fbyte', 'fextension']
        
        # format_kind - Apache, Nginx, IIS를 구분해야 한다.
        
        # {'h': 0, 't': 3, 'r': 4, 's': 5} 이런 형태
        # 예시 : log_format = '%h %l %u %t \"%r\" %>s %b'
        format_index = self.get_logformat_index(log_format, format_kind)     
        
        # X-Forwarded-For 처리 위해 전체라인을 먼저 처리한다.
        # 'log_line' : 그대로 들어가야 한다. - Delimiter가 없다.(\t 사용)
        # 전체 읽을 때에는 escapechar="\\" 불필요하다.
        df_logs = None
        df_logs_all = None
        file_name = logfile_name
        
        try:
            
            df_logs_all = pd.read_csv(file_name, encoding="utf-8", header=None, comment='#', delimiter="\t", error_bad_lines=False,  skiprows=skiprows, nrows=nrows, na_filter=False)
            
        except UnicodeDecodeError as ude:
            
            logger.error('UnicodeDecodeError Occured! Trying again with another encoding = cp1252 : %s' % ude)    
            
            try:
                df_logs_all = pd.read_csv(file_name, encoding="cp1252", header=None, comment='#', delimiter="\t", error_bad_lines=False, skiprows=skiprows, nrows=nrows, na_filter=False)
            except Exception as uex:
                logger.error('UnicodeDecodeError Occured AGAIN!')
                raise uex            
            
        except Exception as ex: 
            logger.error('Error Occured while creating logdetail read_csv#2 whole lines : %s' % ex)            
            raise ex        
        
        # X-Forwarded-For 처리 : apache, nginx   
        # 성능 때문에 %h가 없는 경우에만 일단 처리(apache)
        # 성능 때문에 $remote_addr 없는 경우에만 일단 처리(nginx) TODO: 차후 확인필요
        if (log_format.find('h') == -1 and log_format.find('X-Forwarded-For') != -1) or (log_format.find('$remote_addr') == -1 and log_format.find('$http_x_forwarded_for') != -1):
            repl = lambda m: m.group(0)[:-1:]
            df_logs_re = df_logs_all[0].str.replace(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(\, )+', repl)            
            np.savetxt(logfile_name+"_X-Forwarded-For", df_logs_re.values, fmt="%s")
            
            # 파일이 나누어서 만들어진다. 대상 파일이 변경됨
            file_name = logfile_name+"_X-Forwarded-For"            
            skiprows = None
            nrows = None
                        
        try:           
            # IIS-W3C의 경우 Log의 내용 중 시작에 #가 있는 라인은 주석으로 처리한다.
            # Delimiter로 공백이 여러개 있을 수 있으므로 \s+ 사용한다. 
            df_logs = pd.read_csv(file_name, encoding="utf-8", error_bad_lines=False, header=None, comment='#', delimiter="\s+", escapechar="\\", skiprows=skiprows, nrows=nrows, na_filter=False, quotechar='"')
            
        except UnicodeDecodeError as ude:
            
            logger.error('UnicodeDecodeError Occured! Trying again with another encoding = cp1252 : %s' % ude)
            
            try:
                df_logs = pd.read_csv(file_name, encoding="cp1252", error_bad_lines=False, header=None, comment='#', delimiter="\s+", escapechar="\\", skiprows=skiprows, nrows=nrows, na_filter=False, quotechar='"')
            except Exception as uex:
                logger.error('UnicodeDecodeError Occured AGAIN!')
                raise uex            
            
        except Exception as ex: 
            logger.error('Error Occured while creating logdetail read_csv#1  : %s' % ex)
            raise ex                      
                  
        df_logs['log_line'] = df_logs_all
        
        # 읽어들인 Dataframe에서 Merge하기 : 성능향상 목적(File에서 한번 더 읽는 것보다 빠르다.)
        #df_logs['log_line'] = df_logs[df_logs.columns[0:]].apply(lambda x: ' '.join(x.astype(str)), axis=1)              
        
        if format_kind == 'apache' or format_kind == 'tomcat' or format_kind == 'webtob' or format_kind == 'IIS-NCSA':
            df_logs = self.setColumn(df_logs, format_kind, log_format, format_index)
        elif format_kind == 'IIS-W3C':
            df_logs = self.setColumnW3C(df_logs, format_kind, log_format, format_index)
        elif format_kind == 'nginx':
            df_logs = self.setColumnNginx(df_logs, format_kind, log_format, format_index)

        #'freserve1', 'freserve2', 'freserve3'        
        df_logs['freserve1'] = ''
        df_logs['freserve2'] = ''
        df_logs['freserve3'] = ''
        
        # freserve1 : Nginx Ingress Controller의 upstream 정보 용도로 사용 - df_logs['proxy_upstream_name'], df_logs['upstream_addr']
        # TODO: 값이 없는 경우의 처리는?
        if format_kind == 'nginx':
            df_logs['freserve1'] = df_logs['proxy_upstream_name'] + '/' + df_logs['upstream_addr']
            
            # TODO: Domain 추출 - 패턴 : "http:// ~ /"            
            p = re.compile('http://[a-zA-Z0-9.\-_]+/', re.DOTALL )
            df_logs['freserve2']  = df_logs['freferer'].apply(lambda x: p.findall(x)[0] if len(p.findall(x)) > 0 else '-')
        
        #'created'
        datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        df_logs['created'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')
                
        #'logfile_id'
        df_logs['logfile_id'] = logfile_id
        
        df_time = pd.DataFrame()
        if format_kind == 'IIS-W3C':
                        
            series = df_logs[format_index['date']].str.split('-') + df_logs[format_index['time']].str.split(':')
            df_time = pd.DataFrame(series.tolist(), columns=['fyear','fmonth','fday','fhour','fminute','fsecond'])            
            
            #df_time['fdate'] = df_time['fyear'] + df_time['fmonth'] + df_time['fday']
            #df_time['ftime'] = df_time['fhour'] + df_time['fminute'] + df_time['fsecond']
            #df_time['fdatetime'] = df_time['fdate']+df_time['ftime']
            
        else:
            #'fhour', #'fminute', #'fsecond', #'fday', #'fmonth', #'fyear'
            # 시간관련, dummy는 , 때문에
            if format_kind == 'nginx':
                time_index = format_index['$time_local']
            else:
                time_index = format_index['t']
            
            df_datetime = df_logs[time_index].str.replace(pat='[\:\/\[]', repl= r' ', regex=True)
            series = df_datetime.str.split(' ')
            df_time = pd.DataFrame(series.tolist(), columns=['dummy','fday','fmonth','fyear','fhour','fminute','fsecond'])
            
            # 보완로직1 - 결측치 제거 : None있으면 해당 row 제거
            df_time.dropna(axis=0, inplace=True)

            month_map = {
                'Jan' : '01', 'Feb' : '02', 'Mar' : '03', 'Apr' : '04', 'May' : '05', 'Jun' : '06',
                'Jul' : '07', 'Aug' : '08', 'Sep' : '09', 'Oct' : '10', 'Nov' : '11', 'Dec' : '12',
            }

            df_time['fmonth'] = df_time['fmonth'].apply(lambda x : month_map[x])       
            
        # Add Columns : fdate YYYYMMDD(fyear+fmonth+fday), ftime hhmmss(fhour+fminute+fsecond), fdatetime(YYYYMMDDhhmmss)
        df_time['fdate'] = df_time['fyear'] + df_time['fmonth'] + df_time['fday']
        df_time['ftime'] = df_time['fhour'] + df_time['fminute'] + df_time['fsecond']
        df_time['fdatetime'] = df_time['fdate']+df_time['ftime']
        
        # fbyte 처리 : - 를 0으로 처리
        df_logs['fbyte'] = df_logs['fbyte'].apply(lambda x : 0 if x == '-' else x )      
        
        # fextension 처리 : frequest로부터 처리한다.
        # 정적파일 추출 : js, html, ico, jpg, png, bmp, otf, css
        p = re.compile('(.js|.html|.ico|.jpg|.png|.bmp|.otf|.css)\s', re.DOTALL )
        df_logs['fextension'] = df_logs['frequest'].apply(lambda x: p.findall(x)[0][1:] if len(p.findall(x)) > 0 else '-')
        
        # Merge : logdetail_id -> id
        # ID 기존의 개수 + 1 만큼 + 해주어야 한다. 0부터 시작이므로        
        df_logs = df_logs.rename_axis('id').reset_index()
        df_logs['id'] = df_logs['id'] + existed_row_size
        
        df_logs = pd.concat([df_logs, df_time], axis=1)
        
        # 보완로직2 - 결측치 제거 : None있으면 해당 row 제거
        df_logs.dropna(axis=0, inplace=True)
                        
        # index 미사용
        result_file_name = file_name+'_'+str(file_order)+'.csv'
        df_logs[log_line_header].to_csv(result_file_name, index=False)
       
        if settings.DEBUG:
    	    logger.debug("Duration to create temporary csv : %s" % (time.time() - start))
        
        return result_file_name
    
    def get_logformat_index(self, log_format, format_kind):
        format_index = {}
        index = 0
        for tmp in log_format.split(sep=' '):
            
            if format_kind == 'apache' or format_kind == 'tomcat' or format_kind == 'webtob' or format_kind == 'IIS-NCSA':
                if tmp.find('Referer') != -1:
                    format_index['Referer'] = index
                elif tmp.find('User-Agent') != -1:
                    format_index['User-Agent'] = index
                elif tmp.find('X-Forwarded-For') != -1:
                    format_index['X-Forwarded-For'] = index                    
                elif "%h" in tmp:
                    format_index['h'] = index
                elif "%t" in tmp:
                    format_index['t'] = index
                    index = index + 1 # 하나 더 세야 한다.(apache 시간의 경우 [24/Dec/2019:13:54:26 +0900] 이런 형식이기 때문에)
                elif "%r" in tmp:
                    format_index['r'] = index
                elif "%s" in tmp or "%>s" in tmp:
                    format_index['s'] = index
                elif "%b" in tmp or "%B" in tmp:
                    format_index['b'] = index
                elif "%D" in tmp:   # millisecond
                    format_index['D'] = index
                elif "%T" in tmp:   # second
                    format_index['T'] = index   
                        
            elif format_kind == 'nginx':
                if tmp.find('$http_referer') != -1:
                    format_index['$http_referer'] = index
                elif tmp.find('$http_user_agent') != -1:
                    format_index['$http_user_agent'] = index
                elif tmp.find('$http_x_forwarded_for') != -1:
                    format_index['$http_x_forwarded_for'] = index                    
                elif "$remote_addr" in tmp:
                    format_index['$remote_addr'] = index
                elif "$time_local" in tmp:
                    format_index['$time_local'] = index
                    index = index + 1 # 하나 더 세야 한다.(apache 시간의 경우 [24/Dec/2019:13:54:26 +0900] 이런 형식이기 때문에)
                elif "$request" in tmp and "$request_" not in tmp:
                    format_index['$request'] = index
                elif "$status" in tmp:
                    format_index['$status'] = index
                elif "$body_bytes_sent" in tmp:
                    format_index['$body_bytes_sent'] = index
                elif "$request_time" in tmp:   # millisecond
                    format_index['$request_time'] = index
                # Ingress Nginx
                elif "$proxy_upstream_name" in tmp:   
                    format_index['$proxy_upstream_name'] = index
                elif "$upstream_addr" in tmp:   
                    format_index['$upstream_addr'] = index                  
            
            elif format_kind == 'IIS-W3C':
                if tmp.find('cs(Referer)') != -1:
                    format_index['cs(Referer)'] = index
                elif tmp.find('cs(User-Agent)') != -1:
                    format_index['cs(User-Agent)'] = index                
                elif "c-ip" in tmp:
                    format_index['c-ip'] = index
                # date, time 처리 필요
                elif "date" in tmp:
                    format_index['date'] = index
                elif "time" in tmp and "time-taken" not in tmp:
                    format_index['time'] = index
                # Request 결합 필요
                elif "cs-method" in tmp:
                    format_index['cs-method'] = index
                elif "cs-uri-stem" in tmp:
                    format_index['cs-uri-stem'] = index
                elif "cs-uri-query" in tmp:
                    format_index['cs-uri-query'] = index
                elif "sc-status" in tmp:
                    format_index['sc-status'] = index
                elif "cs-bytes" in tmp:
                    format_index['cs-bytes'] = index
                elif "time-taken" in tmp:
                    format_index['time-taken'] = index
                
            index = index + 1 
            
        return format_index    

    def setColumn(self, df_logs, format_kind, log_format, format_index):
        
        # if 'h' in log_format:
        if log_format.find('h') != -1:
            df_logs.rename(columns = {format_index['h'] : 'fip'}, inplace = True)
        else:
            #  %{X-Forwarded-For}i의 맨 앞은 사용자 IP, %h와 같이 사용하지 않을 것임   
            if log_format.find('X-Forwarded-For') != -1:
                df_logs['fip'] = df_logs[format_index['X-Forwarded-For']].str.split(',').str[0]            
            else:
                df_logs['fip'] = 'NA'
            
        # if 'r' in log_format:
        if log_format.find('r') != -1:
            df_logs.rename(columns = {format_index['r'] : 'frequest'}, inplace = True)
        else:           
            df_logs['frequest'] = 'NA'    

        # if 's' in log_format:
        if log_format.find('s') != -1:
            df_logs.rename(columns = {format_index['s'] : 'fstatus'}, inplace = True)
        else:
            df_logs['fstatus'] = 'NA'
            
        # bytes    
        if log_format.find('b') != -1 or log_format.find('B') != -1:
            df_logs.rename(columns = {format_index['b'] : 'fbyte'}, inplace = True)
        else:
            df_logs['fbyte'] = 0

        if log_format.find('Referer') != -1:
            df_logs.rename(columns = {format_index['Referer'] : 'freferer'}, inplace = True)
        else:
            df_logs['freferer'] = 'NA'
            
        if log_format.find('User-Agent') != -1:
            df_logs.rename(columns = {format_index['User-Agent'] : 'fuser_agent'}, inplace = True)
        else:
            df_logs['fuser_agent'] = 'NA'

        time_taken_flag = False    
        if log_format.find('%T') != -1:
            df_logs.rename(columns = {format_index['T'] : 'ftime_taken'}, inplace = True)
            time_taken_flag = True

        if (not time_taken_flag) & (log_format.find('%D') != -1):
            df_logs.rename(columns = {format_index['D'] : 'ftime_taken'}, inplace = True)
            
            # Tomcat, WebtoB의 경우 단위가 ms이므로 *1000 필요 df_logs['ftime_taken']
            if format_kind == 'tomcat' or format_kind == 'webtob':
                df_logs['ftime_taken'] = df_logs['ftime_taken'].mul(1000)
        else:
            df_logs['ftime_taken'] = -1
            
        return df_logs
    
    def setColumnW3C(self, df_logs, format_kind, log_format, format_index):
        
        # if 'c-ip' in log_format:
        if log_format.find('c-ip') != -1:
            df_logs.rename(columns = {format_index['c-ip'] : 'fip'}, inplace = True)
        else:
            df_logs['fip'] = 'NA'
            
        # Request 생성부분
        # cs-method가 있으면 cs-uri-stem, cs-uri-query 있다고 가정한다.
        if log_format.find('cs-method') != -1 and log_format.find('cs-uri-stem') != -1 and log_format.find('cs-uri-query') != -1:
            df_logs['frequest'] = df_logs[format_index['cs-method']]+" "+df_logs[format_index['cs-uri-stem']]+"?"+df_logs[format_index['cs-uri-query']]
        else:
            df_logs['frequest'] = 'NA'

        if log_format.find('sc-status') != -1:
            df_logs.rename(columns = {format_index['sc-status'] : 'fstatus'}, inplace = True)
        else:
            df_logs['fstatus'] = 'NA'
            
        # bytes    
        if log_format.find('cs-bytes') != -1:
            df_logs.rename(columns = {format_index['cs-bytes'] : 'fbyte'}, inplace = True)
        else:
            df_logs['fbyte'] = 0

        if log_format.find('cs(Referrer)') != -1:
            df_logs.rename(columns = {format_index['cs(Referrer)'] : 'freferer'}, inplace = True)
        else:
            df_logs['freferer'] = 'NA'
            
        if log_format.find('cs(User-Agent)') != -1:
            df_logs.rename(columns = {format_index['cs(User-Agent)'] : 'fuser_agent'}, inplace = True)
        else:
            df_logs['fuser_agent'] = 'NA'

        if log_format.find('time-taken') != -1:
            df_logs.rename(columns = {format_index['time-taken'] : 'ftime_taken'}, inplace = True)
            
            # millisecond
            df_logs['ftime_taken'] = df_logs['ftime_taken'].mul(1000).astype(int)
                    
        else:
            df_logs['ftime_taken'] = -1
            
        return df_logs
    
    def setColumnNginx(self, df_logs, format_kind, log_format, format_index):
        
        # if 'h' in log_format:
        if log_format.find('$remote_addr') != -1:
            df_logs.rename(columns = {format_index['$remote_addr'] : 'fip'}, inplace = True)
        else:
            #  %{X-Forwarded-For}i의 맨 앞은 사용자 IP, %h와 같이 사용하지 않을 것임   
            if log_format.find('$http_x_forwarded_for') != -1:
                df_logs['fip'] = df_logs[format_index['$http_x_forwarded_for']].str.split(',').str[0]            
            else:
                df_logs['fip'] = 'NA'
            
        # if 'r' in log_format:
        if log_format.find('$request') != -1:
            df_logs.rename(columns = {format_index['$request'] : 'frequest'}, inplace = True)
        else:
            df_logs['frequest'] = 'NA'    

        # if 's' in log_format:
        if log_format.find('$status') != -1:
            df_logs.rename(columns = {format_index['$status'] : 'fstatus'}, inplace = True)
        else:
            df_logs['fstatus'] = 'NA'
            
        # bytes    
        if log_format.find('$body_bytes_sent') != -1:
            df_logs.rename(columns = {format_index['$body_bytes_sent'] : 'fbyte'}, inplace = True)
        else:
            df_logs['fbyte'] = 0

        if log_format.find('$http_referer') != -1:
            df_logs.rename(columns = {format_index['$http_referer'] : 'freferer'}, inplace = True)
        else:
            df_logs['freferer'] = 'NA'
            
        if log_format.find('$http_user_agent') != -1:
            df_logs.rename(columns = {format_index['$http_user_agent'] : 'fuser_agent'}, inplace = True)
        else:
            df_logs['fuser_agent'] = 'NA'
       
        if log_format.find('$request_time') != -1:
            df_logs.rename(columns = {format_index['$request_time'] : 'ftime_taken'}, inplace = True)
            
            # millisecond
            #df_logs['ftime_taken'].mul(1000).fillna(0).apply(np.int64)
            # 잘못 파싱되어 문자열 들어간 경우
            df_logs['ftime_taken'] = pd.to_numeric(df_logs['ftime_taken'], errors='coerce').fillna(0).mul(1000).astype(int)
        
        # Ingress Nginx    
        if log_format.find('$proxy_upstream_name') != -1:
            df_logs.rename(columns = {format_index['$proxy_upstream_name'] : 'proxy_upstream_name'}, inplace = True)
            
        if log_format.find('$upstream_addr') != -1:
            df_logs.rename(columns = {format_index['$upstream_addr'] : 'upstream_addr'}, inplace = True)
                        
        else:
            df_logs['ftime_taken'] = -1
            
        return df_logs
        
    
    def get_original_filesize(self, logfile_name):
        
        if 'zip' in logfile_name:
            
            with ZipFile(logfile_name) as zip_archive:
                for item in zip_archive.filelist:
                    print(item)
                    print("# file_size = ", item.file_size)
                    
                #print(f'\nThere are {len(zip_archive.filelist)} ZipInfo objects present in archive')                
                return item.file_size

        else:   # 'gz'
            
            with gzip.open(logfile_name, "rb") as f:
                #data = f.read()
                f.seek(0, 2)
                return f.tell()
                
    def decompress_file(self, logfile_name):
        
        # 저장할 디렉토리 설정
        #target_dir = os.path.dirname(logfile_name)+os.path.sep+"decompressed"
        #original_filename = os.path.basename(logfile_name)
        result_filename = logfile_name+"_decompressed"
        
        #if not(os.path.isdir(target_dir)):
        #    os.makedirs(os.path.join(target_dir))
        
        decompressedFile = ""
        
        if 'zip' in logfile_name:
            with ZipFile(logfile_name, 'r') as zip_ref:
                zip_ref.extractall(result_filename)
                # 단일 파일만 지원
                decompressedFile = result_filename+os.path.sep+zip_ref.filelist[0].filename
                
        else:                     
            with gzip.open(logfile_name, 'rb') as s_file, \
                open(result_filename, 'wb') as d_file:   # 파일명까지 지정해줘여 하는가?
                
                while True:
                    block = s_file.read(65536)
                    if not block:
                        break
                    else:
                        d_file.write(block)       
                                
            decompressedFile = result_filename    
        
        # 생성된 파일 경로를 리턴                
        return decompressedFile

    def get_total_lines(self, file_name):
        
        startTime = time.time()
        
        processes = multiprocessing.cpu_count()
        
        def blocks(files, size=65536):
            while True:
                b = files.read(size*(processes))
                if not b: break
                yield b

        linecount = 0

        with open(file_name, "r", encoding="utf-8", errors='ignore') as f:
            linecount = sum(bl.count("\n") for bl in blocks(f))
            print (linecount)
        
        endTime = time.time()
        
        print("## 프로세스 수 : ", processes)
        print("## line count 까지 : 총 작업 시간 - ", round((endTime - startTime),4)) 
        
        return linecount

class MetricsViewSet(viewsets.ModelViewSet):
    queryset = Metrics.objects.all()
    serializer_class = MetricsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['metric_kind', 'creator']

class LogMasterMetricViewSet(viewsets.ModelViewSet):
    queryset = LogMasterMetric.objects.all()
    serializer_class = LogMasterMetricSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['metric', 'project', 'creator']
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import viewsets, status
from rest_framework.renderers import JSONRenderer
from loganalyzerapi.models import LogMaster, LogFile, LogDetail, LogFormat, LogFormatString
from loganalyzerapi.serializers import LogMasterSerializer, LogDetailSerializer, LogFileSerializer, LogFormatSerializer, LogFormatStringSerializer, UserSerializer, DynamicLogDetailSerializer
import time, uuid, re, csv, io
from datetime import datetime, timezone
from rest_framework.response import Response
from django.db import transaction
import pandas as pd
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum, Max, Min, Avg, F
from django.db.models.functions import Concat, Coalesce, Substr
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from postgres_copy import CopyManager
import copy
import numpy as np

from dynamic_models.models import ModelSchema, FieldSchema
from django.apps import apps

    
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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    # Multiple Search
    # http://127.0.0.1:8000/logmaster/?search=aa,22
    search_fields = ['project_name', 'project_description', 'creator']
    
    ordering_fields = ['project_name', 'project_description', 'created']
    ordering = ['created']
    
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
            ftime_taken = FieldSchema.objects.create(model_schema=logdetail_schema, name='ftime_taken', data_type='integer', null=True)
            
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
    
class LogDetailViewSet(viewsets.ModelViewSet):
    queryset = LogDetail.objects.all()
    serializer_class = LogDetailSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # filterset_fields 사용
    # -> http://example.com/api/products?category=clothing&in_stock=True
    # 정확한 검색
    filterset_fields = ['fdate', 'ftime', 'fyear', 'fmonth', 'fday', 'fhour', 'fminute', 'fsecond', 'ftime_taken']
    search_fields = ['fdate', 'ftime', 'fyear', 'fmonth', 'fday', 'fhour', 'fminute', 'fsecond', 'frequest', 'fip', 'freferer', 'fuser_agent', 'fstatus']    
    
    ordering_fields = ['fdate', 'ftime', 'fyear', 'fmonth', 'fday', 'fhour', 'fminute', 'fsecond', 'frequest', 'fip', 'freferer', 'fuser_agent', 'fstatus', 'ftime_taken']
    ordering = ['fdate', 'ftime']
    
    # Multiple Order
    # http://127.0.0.1:8000/logdetail/?ordering=project_name,-created
    
    # search + pagination + ordering
    # http://127.0.0.1:8000/logdetail/?search=te&ordering=-created&limit=10&offset=1
    
    # Pagination : LimitOffsetPagination
    # http://127.0.0.1:8000/logdetail/?limit=10&offset=20
    
    
    # Reference API : http://www.cdrf.co/3.1/rest_framework.viewsets/ModelViewSet.html#get_queryset 
    # QuerySet(Field lookups) : https://docs.djangoproject.com/en/3.0/ref/models/querysets/#id4    
    
    def getTimetakenUnit(self, logfile_id):
        file_format = LogFile.objects.get(logfile_id=logfile_id).file_format
        
        if file_format.find('D') != -1:
            return 'D'
        elif file_format.find('T') != -1:
            return 'T'
        else:
            return None
        
    @action(methods=['post'], detail=False)
    def notice(self, request, pk=None):
        
        try:
            project_id = request.data['project_id']        
            print('notice project_id : ', project_id)
            
            logfiles = LogFile.objects.filter(project_id=project_id).values('logfile_id')
            list_logfile_id = []
            timetakenUnit = "" 
            
            tiemtakenResult = 0
            
            for logfile in logfiles:
                list_logfile_id.append(str(logfile['logfile_id']))
                timetakenUnit = self.getTimetakenUnit(str(logfile['logfile_id']))
                
            #CASE1 : TimeTaken 3초 이상 건수(%T : seconds, %D : microseconds)
            #TODO: Threshold 설정값 관리
            if timetakenUnit is not None:
                threshold = 3 if timetakenUnit == 'T' else 3*1000000    
                tiemtakenResult = LogDetail.objects.filter(logfile_id__in=list_logfile_id).filter(ftime_taken__gt=threshold).count()
            else:
                tiemtakenResult = "N/A"
            
            response = {'message': 'notice returned successfully', 'tiemtakenResult': tiemtakenResult}        
            return Response(response, status = status.HTTP_200_OK)
            
        except Exception as ex:
            print('Error Occured while processing notice...', ex)
                    
            response = {'message': 'notice creation failed.'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(methods=['post'], detail=False)
    def start_end(self, request, pk=None):
        
        # logfile_id 1개의 경우
        # logfile_id = request.data['logfile_id']        
        # print('start_end logfile_id : ', logfile_id)
        
        # tempset = LogDetail.objects.filter(logfile_id=logfile_id).order_by('fdatetime')
        
        # logfile_id 여러개의 경우 : project_id로 logfile_id 목록을 가져옴 from Logfile Model
        try:
            project_id = request.data['project_id']        
            print('start_end project_id : ', project_id)
            
            logfiles = LogFile.objects.filter(project_id=project_id).values('logfile_id', 'file_name')
            list_logfile_id = []
            list_file_name = []
            
            for logfile in logfiles:
                list_logfile_id.append(str(logfile['logfile_id']))
                list_file_name.append(logfile['file_name'])
            
            tempset = LogDetail.objects.filter(logfile_id__in=list_logfile_id).order_by('fdatetime')
            
            firstRow = tempset.first()
            lastRow = tempset.last()
            
            response = {'message': 'start_end returned successfully', 'start_date': firstRow.fdate, 'start_time': firstRow.ftime, 'end_date': lastRow.fdate, 'end_time': lastRow.ftime, 'file_names': list_file_name}        
            return Response(response, status = status.HTTP_200_OK)
            
        except Exception as ex:
            print('Error Occured while processing start_end...', ex)
                    
            response = {'message': 'start_end creation failed.'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
           
    
    # For Statistics - chartdata    
    @action(methods=['post'], detail=False)
    def chartdata(self, request, pk=None):

        try:        
            # project_id 가져와야 한다.(화면 연계필요)
            #logfile_id = request.data['logfile_id']
            
            project_id = request.data['project_id']        
            print('**chartdata project_id : ', project_id) 
            
            type = request.data['type']
            kind = request.data['kind']
            print("** chartdata : type, kind --> ", type, kind)
            
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
                        resultY.append(row['y'])
                        
                elif(kind == 2):
                    
                    start_time = time.time()
                    
                    hhRequest = queryset.annotate(f_date=Concat('fdate','fhour'), f_status=Substr('fstatus',1,1)).values('f_date', 'f_status').annotate(status_count=Count('f_status')).order_by('f_date')
                    rows = hhRequest.values('f_date', 'f_status', 'status_count')
                    
                    dateStatusCount = {}    # {'날짜' : { 'status_code' : 'status_count'}, '날짜' : { 'status_code' : 'status_count'}, ...}
                    statusCount = {}
                    
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
                        statusCount[row['f_status']] = row['status_count']
                        dateStatusCount[row['f_date']] = copy.deepcopy(statusCount)
                        
                    for xDate in resultX:
                        for yStatusCode in resultStatusCode:
                            
                            if yStatusCode == '2' and yStatusCode in dateStatusCount[xDate] :
                                resultY_200.append(dateStatusCount[xDate][yStatusCode])
                            elif yStatusCode == '3' and yStatusCode in dateStatusCount[xDate] :
                                resultY_300.append(dateStatusCount[xDate][yStatusCode])
                            elif yStatusCode == '4' and yStatusCode in dateStatusCount[xDate] :
                                resultY_400.append(dateStatusCount[xDate][yStatusCode])
                            elif yStatusCode == '5' and yStatusCode in dateStatusCount[xDate] :
                                resultY_500.append(dateStatusCount[xDate][yStatusCode])
                            else:
                                print('There is no available status code.')
                            
                    print("== 전체 시간 : ", time.time() - start_time)
                    
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
                            resultY_time.append(row['yt'])
                    else:
                        pass
            
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
                        resultY.append(row['y'])
                                        
                    print("== 전체 시간 : ", time.time() - start_time)                    
                    
                elif(kind == 2):
                    
                    hhmmRequest = queryset.annotate(f_date=Concat('fdate','fhour', 'fminute'), f_status=Substr('fstatus',1,1)).values('f_date', 'f_status').annotate(status_count=Count('f_status')).order_by('f_date')
                    rows = hhmmRequest.values('f_date', 'f_status', 'status_count')
                    
                    dateStatusCount = {}    # {'날짜' : { 'status_code' : 'status_count'}, '날짜' : { 'status_code' : 'status_count'}, ...}
                    statusCount = {}
                    
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
                        statusCount[row['f_status']] = row['status_count']
                        dateStatusCount[row['f_date']] = copy.deepcopy(statusCount)
                        
                    for xDate in resultX:
                        for yStatusCode in resultStatusCode:
                            
                            if yStatusCode == '2' and yStatusCode in dateStatusCount[xDate] :
                                resultY_200.append(dateStatusCount[xDate][yStatusCode])
                            elif yStatusCode == '3' and yStatusCode in dateStatusCount[xDate] :
                                resultY_300.append(dateStatusCount[xDate][yStatusCode])
                            elif yStatusCode == '4' and yStatusCode in dateStatusCount[xDate] :
                                resultY_400.append(dateStatusCount[xDate][yStatusCode])
                            elif yStatusCode == '5' and yStatusCode in dateStatusCount[xDate] :
                                resultY_500.append(dateStatusCount[xDate][yStatusCode])
                            else:
                                #print('There is no available status code.')
                                pass
                            
                    print("== 전체 시간 : ", time.time() - start_time)
                        
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
                            resultY_time.append(row['yt'])
                    else:
                        pass
            # Type3 : 시분초(HHMMSS)기준                    
            #   Kind1 : request(요청) 건수(count)
            #   Kind2 : status code 건수(count)
            #   Kind3 : time-taken 시간(max, min, count) 
            elif type == '3':          
                            
                if(kind == 1):               
                    
                    hhmmssRequest = queryset.values('fdate','fhour','fminute','fsecond').order_by('fdate','fhour','fminute','fsecond').annotate(x=Concat('fdate','fhour','fminute','fsecond'), y=Count('frequest'))
                    print("== 쿼리 시간 : ", time.time() - start_time)
                    rows = hhmmssRequest.values('x','y')
                    
                    for row in rows:
                        print("type3, kind1 : request(요청) 건수(count) x - ",row['x'])
                        resultX.append(row['x'])
                        resultY.append(row['y'])
                                        
                    print("== 전체 시간 : ", time.time() - start_time)
                    
                elif(kind == 2):
                    
                    hhmmssRequest = queryset.annotate(f_date=Concat('fdate','fhour', 'fminute','fsecond'), f_status=Substr('fstatus',1,1)).values('f_date', 'f_status').annotate(status_count=Count('f_status')).order_by('f_date')
                    rows = hhmmssRequest.values('f_date', 'f_status', 'status_count')
                    
                    dateStatusCount = {}    # {'날짜' : { 'status_code' : 'status_count'}, '날짜' : { 'status_code' : 'status_count'}, ...}
                    statusCount = {}
                    
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
                        statusCount[row['f_status']] = row['status_count']
                        dateStatusCount[row['f_date']] = copy.deepcopy(statusCount)
                        
                    for xDate in resultX:
                        for yStatusCode in resultStatusCode:
                            
                            if yStatusCode == '2' and yStatusCode in dateStatusCount[xDate] :
                                resultY_200.append(dateStatusCount[xDate][yStatusCode])
                            elif yStatusCode == '3' and yStatusCode in dateStatusCount[xDate] :
                                resultY_300.append(dateStatusCount[xDate][yStatusCode])
                            elif yStatusCode == '4' and yStatusCode in dateStatusCount[xDate] :
                                resultY_400.append(dateStatusCount[xDate][yStatusCode])
                            elif yStatusCode == '5' and yStatusCode in dateStatusCount[xDate] :
                                resultY_500.append(dateStatusCount[xDate][yStatusCode])
                            else:
                                #print('There is no available status code.')
                                pass
                            
                    print("== 전체 시간 : ", time.time() - start_time)
                        
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
                            resultY_time.append(row['yt'])
                    else:
                        pass        
                    
            response = {'message': 'linechartdata returned successfully', 'resultX': resultX, 'resultY': resultY, 'resultY_time': resultY_time, 'resultY_time_unit': resultY_time_unit, 'resultY_200': resultY_200, 'resultY_300': resultY_300, 'resultY_400': resultY_400, 'resultY_500': resultY_500}        
            return Response(response, status = status.HTTP_200_OK)
        
        except Exception as ex:
            print('Error Occured while creating chartdata...', ex)
                    
            response = {'message': 'chartdata creation failed.'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
     # For Statistics
    @action(methods=['post'], detail=False)
    def statistics(self, request, pk=None):
        
        try:
        
            #logfile_id = request.data['logfile_id']
            
            project_id = request.data['project_id']        
            # print('statistics project_id : ', project_id)
                        
            type = request.data['type']
            N = request.data['N']
            intN = int(N)
            strN = str(N)
            
            # print("** statistics : type --> ", type)
            # print("** statistics : N --> ", N)
                    
            # 검색 조건 적용
            if type != 0:
                queryset = self.get_queryset()
            else:
                queryset = self.queryset

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
            
            #type=0. 전체 처리량(건수)
            if type == 0:
                cnt = queryset.count()
                print("type0 : queryset.count() - ", cnt)
                results.append({"result" : 'Total', "result_count" : cnt})
            
            #type=1. Status Codes Top N       
            elif type == 1:
                topn_status = queryset.values('fstatus').annotate(fstatus_count=Count('fstatus')).order_by('-fstatus_count')[0:intN]                        
                rows = topn_status.values('fstatus','fstatus_count')
                
                for row in rows:
                    # print("type1 : TOP"+strN+" STATUS - ", row['fstatus'])
                    # print("type1 : TOP"+strN+" STATUS Count - ", row['fstatus_count'])
                    
                    results.append({"result" : row['fstatus'], "result_count" : row['fstatus_count']})                      
            
            #type=2. Requests Top N
            elif type == 2:
                topn_request = queryset.values('frequest').annotate(frequest_count=Count('frequest')).order_by('-frequest_count')[0:intN]
                rows = topn_request.values('frequest','frequest_count')
                
                for row in rows:
                    # print("type2 : TOP"+strN+"REQUEST - ", row['frequest'])
                    # print("type2 : TOP"+strN+"REQUEST Count - ", row['frequest_count'])
                    
                    results.append({"result" : row['frequest'], "result_count" : row['frequest_count']})   
                        
            #type=3. 최다 404 발생 URL Top5
            elif type == 3:
                topn_404_request = queryset.filter(fstatus__startswith='404').values('frequest').annotate(frequest_404_count=Count('frequest')).order_by('-frequest_404_count')[0:intN]
                rows = topn_404_request.values('frequest','frequest_404_count')
                
                if rows.count() > 0 :
                    for row in rows:
                        # print("type3 : TOP"+strN+" 404 REQUEST - ", row['frequest'])
                        # print("type3 : TOP"+strN+" 404 REQUEST Count - ", row['frequest_404_count'])
                        
                        results.append({"result" : row['frequest'], "result_count" : row['frequest_404_count']}) 
                else:
                    results.append({"result" : "-", "result_count" : "0" }) 
                
            #type=4. Time-taken Top5(오래 걸린시간)
            elif type == 4:
                topn_timetaken_request = queryset.order_by('-ftime_taken')[0:intN]
                rows = topn_timetaken_request.values('frequest','ftime_taken')
                
                for row in rows:
                    # print("type4 : TOP"+strN+" Timtaken REQUEST - ", row['frequest'])
                    # print("type4 : TOP"+strN+" Timtaken REQUEST Count - ", row['ftime_taken'])
                    
                    results.append({"result" : row['frequest'], "result_count" : row['ftime_taken'], "timetakenUnit" : timetakenUnit})
                    
            #type=5. Visitor(Unique IP) Top5
            elif type == 5:
                topn_visitor = queryset.values('fip').annotate(fip_count=Count('fip')).order_by('-fip_count')[0:intN]
                rows = topn_visitor.values('fip','fip_count')
                
                for row in rows:
                    # print("type5 : TOP"+strN+" VISITOR - ", row['fip'])
                    # print("type5 : TOP"+strN+" VISITOR Count - ", row['fip_count'])
                    
                    results.append({"result" : row['fip'], "result_count" : row['fip_count']})   
            
            #type=6. Referers Top N
            elif type == 6:
                topn_referer = queryset.values('freferer').annotate(freferer_count=Count('freferer')).order_by('-freferer_count')[0:intN]
                rows = topn_referer.values('freferer','freferer_count')
                
                for row in rows:
                    # print("type5 : TOP"+strN+" freferer - ", row['freferer'])
                    # print("type5 : TOP"+strN+" freferer Count - ", row['freferer_count'])
                    
                    results.append({"result" : row['freferer'], "result_count" : row['freferer_count']}) 
            
            #type=7. User Agent Top N               
            elif type == 7:
                topn_useragent = queryset.values('fuser_agent').annotate(fuser_agent_count=Count('fuser_agent')).order_by('-fuser_agent_count')[0:intN]
                rows = topn_useragent.values('fuser_agent','fuser_agent_count')
                
                for row in rows:
                    # print("type5 : TOP"+strN+" fuser_agent - ", row['fuser_agent'])
                    # print("type5 : TOP"+strN+" fuser_agent Count - ", row['fuser_agent_count'])
                    
                    results.append({"result" : row['fuser_agent'], "result_count" : row['fuser_agent_count']})  
                    
            #type=8. URI Total Byte Top N               
            elif type == 8:
                topn_byte = queryset.values('frequest').annotate(requestURL=F('frequest'), fbyte_sum=Sum('fbyte')).order_by('-fbyte_sum')[0:intN]
                rows = topn_byte.values('requestURL','fbyte_sum')
                
                for row in rows:
                    # print("type5 : TOP"+strN+" fuser_agent - ", row['fuser_agent'])
                    # print("type5 : TOP"+strN+" fuser_agent Count - ", row['fuser_agent_count'])
                    
                    results.append({"result" : row['requestURL'], "result_count" : row['fbyte_sum']})
                    
            #type=9. Static files Top N               
            elif type == 9:
                topn_static = queryset.values('fextension').annotate(fextension_count=Count('fextension')).order_by('-fextension_count')[0:intN]
                rows = topn_static.values('fextension','fextension_count')
                
                for row in rows:
                    # print("type5 : TOP"+strN+" fuser_agent - ", row['fuser_agent'])
                    # print("type5 : TOP"+strN+" fuser_agent Count - ", row['fuser_agent_count'])
                    
                    results.append({"result" : row['fextension'], "result_count" : row['fextension_count']})  
                    
            #type=10. URI Average Byte Top N               
            elif type == 10:
                topn_avgbyte = queryset.values('frequest').annotate(requestURL=F('frequest'), fbyte_avg=Avg('fbyte')).order_by('-fbyte_avg')[0:intN]
                rows = topn_avgbyte.values('requestURL','fbyte_avg')
                
                for row in rows:
                    # print("type5 : TOP"+strN+" fuser_agent - ", row['fuser_agent'])
                    # print("type5 : TOP"+strN+" fuser_agent Count - ", row['fuser_agent_count'])
                    
                    results.append({"result" : row['requestURL'], "result_count" : row['fbyte_avg']})
                    
            #type=11. URI Average Time-taken Top N
            elif type == 11:
                topn_avg_timetaken_request = queryset.values('frequest').annotate(requestURL=F('frequest'), ftime_taken_avg=Avg('ftime_taken')).order_by('-ftime_taken_avg')[0:intN]
                rows = topn_avg_timetaken_request.values('requestURL','ftime_taken_avg')
                
                for row in rows:
                    # print("type4 : TOP"+strN+" Timtaken REQUEST - ", row['frequest'])
                    # print("type4 : TOP"+strN+" Timtaken REQUEST Count - ", row['ftime_taken'])
                    
                    results.append({"result" : row['requestURL'], "result_count" : row['ftime_taken_avg'], "timetakenUnit" : timetakenUnit})
        
            print("== statistics (type="+str(type)+")걸린 시간 : ", time.time() - start_time)
            
            response = {'message': 'statistics returned', 'results': results}
            return Response(response, status = status.HTTP_200_OK)
        
        except Exception as ex:
            print('Error Occured while creating statistics...', ex)
                    
            response = {'message': 'statistics creation failed.'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    # For Filtering
    def get_queryset(self):
        
        # print("== LogDetailViewSet get_queryset!!")
        
        queryset = LogDetail.objects.all()
        
        # Request Method 확인
        method = ""
        for key in self.action_map:
            if self.action_map[key] == self.action:
                method = key
                break
        #print("method = ", method)
        
        dateFromValue = ""
        dateToValue = ""
        timeFromValue = ""
        timeToValue = ""
        ttFromValue = ""
        ttToValue = ""
        conditionValue = ""
        searchValue = ""
        project_id = ""        

        # 조건 적용(GET)
        if method == 'get' :
            dateFromValue = self.request.query_params.get('dateFromValue', None)
            dateToValue = self.request.query_params.get('dateToValue', None)
            timeFromValue = self.request.query_params.get('timeFromValue', None)
            timeToValue = self.request.query_params.get('timeToValue', None)
            
            ttFromValue = self.request.query_params.get('ttFromValue', None)
            ttToValue = self.request.query_params.get('ttToValue', None)
            
            conditionValue = self.request.query_params.get('conditionValue', None)
            searchValue = self.request.query_params.get('searchValue', None)
            
            project_id = self.request.query_params.get('project_id', None)
        
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
            
        # 관련 project만 가져온다. : multifile 처리
        if project_id is not None:        
            logfiles = LogFile.objects.filter(project_id=project_id).values('logfile_id')            
            list_logfile_id = []         
            
            # logfile id 가져오기
            for logfile in logfiles:
                list_logfile_id.append(str(logfile['logfile_id']))                
            
            queryset = queryset.filter(logfile_id__in=list_logfile_id)
        
        # Date, Time : Between
        if (dateFromValue is not None) and (dateToValue is not None) and (timeFromValue is not None) and (timeToValue is not None):
            start_datetime = dateFromValue + timeFromValue
            end_datetime = dateToValue + timeToValue
            queryset = queryset.filter(fdatetime__range=(start_datetime, end_datetime))
            #print('Date and Time applied!')
        
        # Time-taken : Between
        if (ttFromValue is not None) and (ttToValue is not None):        
            queryset = queryset.filter(ftime_taken__range=(ttFromValue, ttToValue))
            #print('Time-taken applied!')
            
        # conditionValue : Contain
        if conditionValue is not None :
            #print('conditionValue applied! (conditionValue) : ', conditionValue)
            #print('searchValue : ', searchValue)
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
        
        return queryset

    def create(self, request, *args, **kwargs):
        
        print("== LogDetailViewSet create!!")
        start = time.time()
        response = {}
      
        try:
            logfile_id = request.data['logfile_id']
            
            # 이미 생성되어 있는지 확인
            if LogDetail.objects.filter(logfile_id=logfile_id).count() > 0:
                response = {'message': 'logdetail already created.'}
                
            else:                  
                        
                logfile_model = LogFile.objects.get(logfile_id=logfile_id)   
                logfile = logfile_model.file_object.file    
                
                print("logfile :", logfile)     
                
                # [병렬처리] Log Parsing : postgresql copy 사용을 위해 csv파일 생성
                #result = self.parse_log(logfile, logfile_id)
                self.parse_log(logfile, logfile_id)
            
                # postgresql copy 실행
                LogDetail.objects.from_csv(logfile.name+'.csv', delimiter=',')        
                    
                print("To DB, Total Duration :", time.time() - start)
                
                response = {'message': 'logdetail created successfully.'}
                
            return Response(response, status = status.HTTP_200_OK)
        
        except Exception as ex: 
            print('Error Occured while creating logdetail...', ex)
            
            response = {'message': 'logdetail creation failed.'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def parse_log(self, logfile, logfile_id):

        log_lines = []
        result = []
        count = 0               
        start = time.time()
        
        # Fileformat 가져온다.(from logfile DB using logfile_id)
        # 예시 : log_format = '%h %l %u %t \"%r\" %>s %b'      
        format_model = LogFile.objects.get(logfile_id=logfile_id)
        log_format = format_model.file_format
        
        # format_kind : apache, nginx, IIS
        format_kind = format_model.format_kind        
        format_name = format_model.format_name
                
        # 임시 csv 파일생성 for copy to postgresql
        log_line_header = ['logdetail_id','log_line','fhour','fminute','fsecond','fip','freferer','fuser_agent',
                           'fstatus','ftime_taken','freserve1','freserve2','freserve3','created','logfile_id',
                           'frequest','fday','fmonth','fyear','fdate','ftime','fdatetime', 'fbyte', 'fextension']
        
        # pandas 활용 - 로그파일 읽기
        # TODO: %{X-Forwarded-For}i 의 경우 열의 개수가 늘어나는데...전처리를 어떻게 해야 하나? => 이거 일단 패스(error line 빼고 처리)
        df_logs = None
        try:
            df_logs = pd.read_csv(logfile.name, encoding="utf-8", error_bad_lines=False, header=None, delimiter=" ", escapechar="\\", na_filter=False, quotechar='"')
        except Exception as ex: 
            print('Error Occured while creating logdetail read_csv#1...', ex)
            raise ex
        
        # TODO: format_kind - Apache, Nginx, IIS를 구분해야 한다.
        
        # {'h': 0, 't': 3, 'r': 4, 's': 5} 이런 형태
        # 예시 : log_format = '%h %l %u %t \"%r\" %>s %b'
        format_index = self.get_logformat_index(log_format, format_kind)
        
        # 'log_line' : 그대로 들어가야 한다. - Delimiter가 없다.("@" 명시, @ 사용하지 않을 것임...오류나는지 확인필요, \t 이런걸로?)
        df_logs_all = None
        try:
            df_logs_all = pd.read_csv(logfile.name, encoding="utf-8", header=None, delimiter="\t", error_bad_lines=False, escapechar="\\", na_filter=False)
        except Exception as ex: 
            print('Error Occured while creating logdetail read_csv#2...', ex)
            raise ex
        
        df_logs['log_line'] = df_logs_all
        
        # 읽어들인 Dataframe에서 Merge하기 : 성능향상 목적(File에서 한번 더 읽는 것보다 빠르다.)
        #df_logs['log_line'] = df_logs[df_logs.columns[0:]].apply(lambda x: ' '.join(x.astype(str)), axis=1)              
                
        # if 'h' in log_format:
        if log_format.find('h') != -1:
            df_logs.rename(columns = {format_index['h'] : 'fip'}, inplace = True)
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
        if log_format.find('T') != -1:
            df_logs.rename(columns = {format_index['T'] : 'ftime_taken'}, inplace = True)
            time_taken_flag = True

        if (not time_taken_flag) & (log_format.find('D') != -1):
            df_logs.rename(columns = {format_index['D'] : 'ftime_taken'}, inplace = True)
        else:
            df_logs['ftime_taken'] = -1
        
        #'freserve1', 'freserve2', 'freserve3'
        df_logs['freserve1'] = ''
        df_logs['freserve2'] = ''
        df_logs['freserve3'] = ''
        
        #'created'
        datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        df_logs['created'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')
                
        #'logfile_id'
        df_logs['logfile_id'] = logfile_id
        
        #'fhour', #'fminute', #'fsecond', #'fday', #'fmonth', #'fyear'
        # 시간관련, dummy는 , 때문에
        time_index = format_index['t']
        df_datetime = df_logs[time_index].str.replace(pat='[\:\/\[]', repl= r' ', regex=True)
        series = df_datetime.str.split(' ')
        df_time = pd.DataFrame(series.tolist(), columns=['dummy','fday','fmonth','fyear','fhour','fminute','fsecond'])

        # TODO: Welstorymall Log Error - None인 경우 00으로??
        month_map = {
            'Jan' : '01', 'Feb' : '02', 'Mar' : '03', 'Apr' : '04', 'May' : '05', 'Jun' : '06',
            'Jul' : '07', 'Aug' : '08', 'Sep' : '09', 'Oct' : '10', 'Nov' : '11', 'Dec' : '12'
        }
        # TODO: Welstorymall Log Error
        df_time['fmonth'] = df_time['fmonth'].apply(lambda x : month_map[x])
        
        # Add Columns : fdate YYYYMMDD(fyear+fmonth+fday), ftime hhmmss(fhour+fminute+fsecond), fdatetime(YYYYMMDDhhmmss)
        df_time['fdate'] = df_time['fyear'] + df_time['fmonth'] + df_time['fday']
        df_time['ftime'] = df_time['fhour'] + df_time['fminute'] + df_time['fsecond']
        df_time['fdatetime'] = df_time['fdate']+df_time['ftime']
        
        # fbyte 처리 : - 를 0으로 처리
        df_logs['fbyte'] = df_logs['fbyte'].apply(lambda x : 0 if x == '-' else x )      
        
        # fextension 처리 : frequest로부터 처리한다.
        # 정적파일 추출 : js, html, ico, jpg, png, bmp, otf, css
        p = re.compile('(.js|.html|.ico|.jpg|.png|.bmp|.otf|.css)', re.DOTALL )
        df_logs['fextension'] = df_logs['frequest'].apply(lambda x: p.findall(x)[0][1:] if len(p.findall(x)) > 0 else '-')
        
        # Merge
        df_logs = df_logs.rename_axis('logdetail_id').reset_index()
        df_logs = pd.concat([df_logs, df_time], axis=1)
        
        # 'logdetail_id' : UUID 생성
        df_logs['logdetail_id'] = df_logs['logdetail_id'].apply(lambda x : uuid.uuid4())         
                        
        #firstRow = df_logs.iloc[0,] #.to_json(orient='index'), head() function       
        #lastRow = df_logs.iloc[-1,] #.to_json(orient='index'), head() function                        
                        
        # index 미사용  
        df_logs[log_line_header].to_csv(logfile.name+'.csv', index=False)
       
        print("Duration to create temporary csv :", time.time() - start)        
        
        #result.append({'firstRow' : firstRow, 'lastRow' : lastRow})
        
        #return result
        
    # def getStaticFileExtension(request):
        
    #     m = p.findall(request)
    #     return m[0][1:] if len(m(request)) > 0 else '-'

    def get_logformat_index(self, log_format, format_kind):
        format_index = {}
        index = 0
        for tmp in log_format.split(sep=' '):
            
            if format_kind == 'apache':
                if tmp.find('Referer') != -1:
                    format_index['Referer'] = index
                elif tmp.find('User-Agent') != -1:
                    format_index['User-Agent'] = index
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
                elif "%D" in tmp:
                    format_index['D'] = index
                elif "%T" in tmp:
                    format_index['T'] = index                
            
            # TODO : nginx, IIS                    
            elif format_kind == 'nginx':
                pass
            elif format_kind == 'IIS':
                pass
                
            index = index + 1 
            
        return format_index    

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
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]   

# TODO: Dynamic Model
class DynamicLogDetailViewSet(viewsets.ModelViewSet):
    
    # TODO: Paging 처리
    
    # For GridTable
    def retrieve(self, request, *args, **kwargs):
        
        print("== DynamicLogDetailViewSet retrieve!!")
        
        return super().retrieve(request, *args, **kwargs)
    
    def get_queryset(self):
         
        print("== DynamicLogDetailViewSet get_queryset!!")
         
        # TODO: 필터 조건 적용
         
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

        # 조건 적용(GET)
        if method == 'get' :
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
            detailsearchValue = self.request.query_params.get('detailsearchValue', None)
        
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
         
        print("get_queryset model_name :", model_name)
         
        LogDetail_dynamic = ModelSchema.objects.get(name=model_name).as_model()
        queryset = LogDetail_dynamic.objects.all()    
            
        # 관련 project만 가져온다. : multifile 처리
        if project_id is not None:        
            logfiles = LogFile.objects.filter(project_id=project_id).values('logfile_id')            
            list_logfile_id = []         
            
            # logfile id 가져오기
            for logfile in logfiles:
                list_logfile_id.append(str(logfile['logfile_id']))                
            
            queryset = queryset.filter(logfile_id__in=list_logfile_id)
        
        # Date, Time : Between
        if (dateFromValue is not None) and (dateToValue is not None) and (timeFromValue is not None) and (timeToValue is not None):
            start_datetime = dateFromValue + timeFromValue
            end_datetime = dateToValue + timeToValue
            queryset = queryset.filter(fdatetime__range=(start_datetime, end_datetime))
            #print('Date and Time applied!')
        
        # Time-taken : Between
        if (ttFromValue is not None) and (ttToValue is not None):        
            queryset = queryset.filter(ftime_taken__range=(ttFromValue, ttToValue))
            #print('Time-taken applied!')
            
        # conditionValue : Contain
        if conditionValue is not None :
            #print('conditionValue applied! (conditionValue) : ', conditionValue)
            #print('searchValue : ', searchValue)
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
                
        # conditionValue : statistic detailpopup
        if detailconditionValue is not None :
            #print('conditionValue applied! (conditionValue) : ', conditionValue)
            #print('searchValue : ', searchValue)
            if detailconditionValue == 'I':
                queryset = queryset.filter(fip__icontains=detailsearchValue)
            elif detailconditionValue == 'R':
                queryset = queryset.filter(frequest__icontains=detailsearchValue)
            elif detailconditionValue == 'E':
                queryset = queryset.filter(freferer__icontains=detailsearchValue)
            elif detailconditionValue == 'U':
                queryset = queryset.filter(fuser_agent__icontains=detailsearchValue)
            elif detailconditionValue == 'S':
                queryset = queryset.filter(fstatus__icontains=detailsearchValue)
            elif detailconditionValue == 'F':
                queryset = queryset.filter(fextension__icontains=detailsearchValue) 
        
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
         
        print("get_serializer_class model_name :", model_name)
         
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
        
    @action(methods=['post'], detail=False)
    def notice(self, request, pk=None):
        
        try:
            project_id = request.data['project_id']        
            print('notice project_id : ', project_id)
            
            logfiles = LogFile.objects.filter(project_id=project_id).values('logfile_id')
            list_logfile_id = []
            timetakenUnit = "" 
            
            tiemtakenResult = 0
            threshold = 0
            
            for logfile in logfiles:
                list_logfile_id.append(str(logfile['logfile_id']))
                timetakenUnit = self.getTimetakenUnit(str(logfile['logfile_id']))
                
            #CASE1 : TimeTaken 3초 이상 건수(%T : seconds, %D : microseconds)
            #TODO: Threshold 설정값 관리
            threshold = int(request.data['threshold'])
            
            if timetakenUnit is not None:
                #threshold = 3 if timetakenUnit == 'T' else 3*1000000
                threshold = threshold if timetakenUnit == 'T' else threshold*1000000   

                model_name = "logdetail_"+project_id
                LogDetail_dynamic = ModelSchema.objects.get(name=model_name).as_model()
            
                tiemtakenResult = LogDetail_dynamic.objects.filter(logfile_id__in=list_logfile_id).filter(ftime_taken__gt=threshold).count()
            else:
                tiemtakenResult = "N/A"
            
            response = {'message': 'notice returned successfully', 'tiemtakenResult': tiemtakenResult}        
            return Response(response, status = status.HTTP_200_OK)
            
        except Exception as ex:
            print('Error Occured while processing notice...', ex)
                    
            response = {'message': 'notice creation failed.'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
     
    @action(methods=['post'], detail=False)
    def start_end(self, request, pk=None):        
       
        try:
            project_id = request.data['project_id']        
            print('start_end project_id : ', project_id)
            
            logfiles = LogFile.objects.filter(project_id=project_id).values('logfile_id', 'file_name')
            list_logfile_id = []
            list_file_name = []
            
            for logfile in logfiles:
                list_logfile_id.append(str(logfile['logfile_id']))
                list_file_name.append(logfile['file_name'])
            
            model_name = "logdetail_"+project_id
            LogDetail_dynamic = ModelSchema.objects.get(name=model_name).as_model()
            tempset = LogDetail_dynamic.objects.filter(logfile_id__in=list_logfile_id).order_by('fdatetime')
            
            firstRow = tempset.first()
            lastRow = tempset.last()
            
            response = {'message': 'start_end returned successfully', 'start_date': firstRow.fdate, 'start_time': firstRow.ftime, 'end_date': lastRow.fdate, 'end_time': lastRow.ftime, 'file_names': list_file_name}        
            return Response(response, status = status.HTTP_200_OK)
            
        except Exception as ex:
            print('Error Occured while processing start_end...', ex)
                    
            response = {'message': 'start_end creation failed.'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    # For Statistics
    @action(methods=['post'], detail=False)
    def statistics(self, request, pk=None):
                
        print("== DynamicLogDetailViewSet statistics!!")
        
        try:       
           
            project_id = request.data['project_id']        
            # print('statistics project_id : ', project_id)
                        
            type = request.data['type']
            N = request.data['N']
            intN = int(N)
            strN = str(N)
            
            # print("** statistics : type --> ", type)
            # print("** statistics : N --> ", N)
            
            queryset = None
                                
            # 검색 조건 적용
            if type != 0:
                queryset = self.get_queryset()
            else:
                model_name = "logdetail_"+project_id
                LogDetail_dynamic = ModelSchema.objects.get(name=model_name).as_model()
                #queryset = self.queryset
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
            
            #type=0. 전체 처리량(건수)
            if type == 0:
                cnt = queryset.count()
                print("type0 : queryset.count() - ", cnt)
                results.append({"result" : 'Total', "result_count" : cnt})
            
            #type=1. Status Codes Top N       
            elif type == 1:
                topn_status = queryset.values('fstatus').annotate(fstatus_count=Count('fstatus')).order_by('-fstatus_count')[0:intN]                        
                rows = topn_status.values('fstatus','fstatus_count')
                
                for row in rows:
                    # print("type1 : TOP"+strN+" STATUS - ", row['fstatus'])
                    # print("type1 : TOP"+strN+" STATUS Count - ", row['fstatus_count'])
                    
                    results.append({"result" : row['fstatus'], "result_count" : row['fstatus_count']})                      
            
            #type=2. Requests Top N
            elif type == 2:
                topn_request = queryset.values('frequest').annotate(frequest_count=Count('frequest')).order_by('-frequest_count')[0:intN]
                rows = topn_request.values('frequest','frequest_count')
                
                for row in rows:
                    # print("type2 : TOP"+strN+"REQUEST - ", row['frequest'])
                    # print("type2 : TOP"+strN+"REQUEST Count - ", row['frequest_count'])
                    
                    results.append({"result" : row['frequest'], "result_count" : row['frequest_count']})   
                        
            #type=3. 최다 404 발생 URL Top5
            elif type == 3:
                topn_404_request = queryset.filter(fstatus__startswith='404').values('frequest').annotate(frequest_404_count=Count('frequest')).order_by('-frequest_404_count')[0:intN]
                rows = topn_404_request.values('frequest','frequest_404_count')
                
                if rows.count() > 0 :
                    for row in rows:
                        # print("type3 : TOP"+strN+" 404 REQUEST - ", row['frequest'])
                        # print("type3 : TOP"+strN+" 404 REQUEST Count - ", row['frequest_404_count'])
                        
                        results.append({"result" : row['frequest'], "result_count" : row['frequest_404_count']}) 
                else:
                    results.append({"result" : "-", "result_count" : "0" }) 
                
            #type=4. Time-taken Top5(오래 걸린시간)
            elif type == 4:
                topn_timetaken_request = queryset.order_by('-ftime_taken')[0:intN]
                rows = topn_timetaken_request.values('frequest','ftime_taken')
                
                for row in rows:
                    # print("type4 : TOP"+strN+" Timtaken REQUEST - ", row['frequest'])
                    # print("type4 : TOP"+strN+" Timtaken REQUEST Count - ", row['ftime_taken'])
                    
                    results.append({"result" : row['frequest'], "result_count" : row['ftime_taken'], "timetakenUnit" : timetakenUnit})
                    
            #type=5. Visitor(Unique IP) Top5
            elif type == 5:
                topn_visitor = queryset.values('fip').annotate(fip_count=Count('fip')).order_by('-fip_count')[0:intN]
                rows = topn_visitor.values('fip','fip_count')
                
                for row in rows:
                    # print("type5 : TOP"+strN+" VISITOR - ", row['fip'])
                    # print("type5 : TOP"+strN+" VISITOR Count - ", row['fip_count'])
                    
                    results.append({"result" : row['fip'], "result_count" : row['fip_count']})   
            
            #type=6. Referers Top N
            elif type == 6:
                topn_referer = queryset.values('freferer').annotate(freferer_count=Count('freferer')).order_by('-freferer_count')[0:intN]
                rows = topn_referer.values('freferer','freferer_count')
                
                for row in rows:
                    # print("type5 : TOP"+strN+" freferer - ", row['freferer'])
                    # print("type5 : TOP"+strN+" freferer Count - ", row['freferer_count'])
                    
                    results.append({"result" : row['freferer'], "result_count" : row['freferer_count']}) 
            
            #type=7. User Agent Top N               
            elif type == 7:
                topn_useragent = queryset.values('fuser_agent').annotate(fuser_agent_count=Count('fuser_agent')).order_by('-fuser_agent_count')[0:intN]
                rows = topn_useragent.values('fuser_agent','fuser_agent_count')
                
                for row in rows:
                    # print("type5 : TOP"+strN+" fuser_agent - ", row['fuser_agent'])
                    # print("type5 : TOP"+strN+" fuser_agent Count - ", row['fuser_agent_count'])
                    
                    results.append({"result" : row['fuser_agent'], "result_count" : row['fuser_agent_count']})  
                    
            #type=8. URI Total Byte Top N               
            elif type == 8:
                topn_byte = queryset.values('frequest').annotate(requestURL=F('frequest'), fbyte_sum=Sum('fbyte')).order_by('-fbyte_sum')[0:intN]
                rows = topn_byte.values('requestURL','fbyte_sum')
                
                for row in rows:
                    # print("type5 : TOP"+strN+" fuser_agent - ", row['fuser_agent'])
                    # print("type5 : TOP"+strN+" fuser_agent Count - ", row['fuser_agent_count'])
                    
                    results.append({"result" : row['requestURL'], "result_count" : row['fbyte_sum']})
                    
            #type=9. Static files Top N               
            elif type == 9:
                topn_static = queryset.values('fextension').annotate(fextension_count=Count('fextension')).order_by('-fextension_count')[0:intN]
                rows = topn_static.values('fextension','fextension_count')
                
                for row in rows:
                    # print("type5 : TOP"+strN+" fuser_agent - ", row['fuser_agent'])
                    # print("type5 : TOP"+strN+" fuser_agent Count - ", row['fuser_agent_count'])
                    
                    results.append({"result" : row['fextension'], "result_count" : row['fextension_count']})  
                    
            #type=10. URI Average Byte Top N               
            elif type == 10:
                topn_avgbyte = queryset.values('frequest').annotate(requestURL=F('frequest'), fbyte_avg=Avg('fbyte')).order_by('-fbyte_avg')[0:intN]
                rows = topn_avgbyte.values('requestURL','fbyte_avg')
                
                for row in rows:
                    # print("type5 : TOP"+strN+" fuser_agent - ", row['fuser_agent'])
                    # print("type5 : TOP"+strN+" fuser_agent Count - ", row['fuser_agent_count'])
                    
                    results.append({"result" : row['requestURL'], "result_count" : row['fbyte_avg']})
                    
            #type=11. URI Average Time-taken Top N
            elif type == 11:
                topn_avg_timetaken_request = queryset.values('frequest').annotate(requestURL=F('frequest'), ftime_taken_avg=Avg('ftime_taken')).order_by('-ftime_taken_avg')[0:intN]
                rows = topn_avg_timetaken_request.values('requestURL','ftime_taken_avg')
                
                for row in rows:
                    # print("type4 : TOP"+strN+" Timtaken REQUEST - ", row['frequest'])
                    # print("type4 : TOP"+strN+" Timtaken REQUEST Count - ", row['ftime_taken'])
                    
                    results.append({"result" : row['requestURL'], "result_count" : row['ftime_taken_avg'], "timetakenUnit" : timetakenUnit})
        
            print("== statistics (type="+str(type)+")걸린 시간 : ", time.time() - start_time)
            
            response = {'message': 'statistics returned', 'results': results}
            return Response(response, status = status.HTTP_200_OK)
        
        except Exception as ex:
            print('Error Occured while creating statistics...', ex)
                    
            response = {'message': 'statistics creation failed.'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    # For Statistics - chartdata    
    @action(methods=['post'], detail=False)
    def chartdata(self, request, pk=None):

        print("== DynamicLogDetailViewSet chartdata!!")
        
        try:        
            
            project_id = request.data['project_id']        
            print('**chartdata project_id : ', project_id) 
            
            type = request.data['type']
            kind = request.data['kind']
            print("** chartdata : type, kind --> ", type, kind)
            
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
                        resultY.append(row['y'])
                        
                elif(kind == 2):
                    
                    start_time = time.time()
                    
                    hhRequest = queryset.annotate(f_date=Concat('fdate','fhour'), f_status=Substr('fstatus',1,1)).values('f_date', 'f_status').annotate(status_count=Count('f_status')).order_by('f_date')
                    rows = hhRequest.values('f_date', 'f_status', 'status_count')
                    
                    dateStatusCount = {}    # {'날짜' : { 'status_code' : 'status_count'}, '날짜' : { 'status_code' : 'status_count'}, ...}
                    statusCount = {}
                    
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
                        statusCount[row['f_status']] = row['status_count']
                        dateStatusCount[row['f_date']] = copy.deepcopy(statusCount)
                        
                    for xDate in resultX:
                        for yStatusCode in resultStatusCode:
                            
                            if yStatusCode == '2' and yStatusCode in dateStatusCount[xDate] :
                                resultY_200.append(dateStatusCount[xDate][yStatusCode])
                            elif yStatusCode == '3' and yStatusCode in dateStatusCount[xDate] :
                                resultY_300.append(dateStatusCount[xDate][yStatusCode])
                            elif yStatusCode == '4' and yStatusCode in dateStatusCount[xDate] :
                                resultY_400.append(dateStatusCount[xDate][yStatusCode])
                            elif yStatusCode == '5' and yStatusCode in dateStatusCount[xDate] :
                                resultY_500.append(dateStatusCount[xDate][yStatusCode])
                            else:
                                print('There is no available status code.')
                            
                    print("== 전체 시간 : ", time.time() - start_time)
                    
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
                            resultY_time.append(row['yt'])
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
                        resultY.append(row['y'])
                                        
                    print("== 전체 시간 : ", time.time() - start_time)                    
                    
                elif(kind == 2):
                    
                    hhmmRequest = queryset.annotate(f_date=Concat('fdate','fhour', 'fminute'), f_status=Substr('fstatus',1,1)).values('f_date', 'f_status').annotate(status_count=Count('f_status')).order_by('f_date')
                    rows = hhmmRequest.values('f_date', 'f_status', 'status_count')
                    
                    dateStatusCount = {}    # {'날짜' : { 'status_code' : 'status_count'}, '날짜' : { 'status_code' : 'status_count'}, ...}
                    statusCount = {}
                    
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
                        statusCount[row['f_status']] = row['status_count']
                        dateStatusCount[row['f_date']] = copy.deepcopy(statusCount)
                        
                    for xDate in resultX:
                        for yStatusCode in resultStatusCode:
                            
                            if yStatusCode == '2' and yStatusCode in dateStatusCount[xDate] :
                                resultY_200.append(dateStatusCount[xDate][yStatusCode])
                            elif yStatusCode == '3' and yStatusCode in dateStatusCount[xDate] :
                                resultY_300.append(dateStatusCount[xDate][yStatusCode])
                            elif yStatusCode == '4' and yStatusCode in dateStatusCount[xDate] :
                                resultY_400.append(dateStatusCount[xDate][yStatusCode])
                            elif yStatusCode == '5' and yStatusCode in dateStatusCount[xDate] :
                                resultY_500.append(dateStatusCount[xDate][yStatusCode])
                            else:
                                #print('There is no available status code.')
                                pass
                            
                    print("== 전체 시간 : ", time.time() - start_time)
                        
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
                            resultY_time.append(row['yt'])
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
                    print("== 쿼리 시간 : ", time.time() - start_time)
                    rows = hhmmssRequest.values('x','y')
                    
                    for row in rows:
                        print("type3, kind3 : request(요청) 건수(count) x - ",row['x'])
                        resultX.append(row['x'])
                        resultY.append(row['y'])
                                        
                    print("== 전체 시간 : ", time.time() - start_time)
                    
                elif(kind == 2):
                    
                    hhmmssRequest = queryset.annotate(f_date=Concat('fdate','fhour', 'fminute','fsecond'), f_status=Substr('fstatus',1,1)).values('f_date', 'f_status').annotate(status_count=Count('f_status')).order_by('f_date')
                    rows = hhmmssRequest.values('f_date', 'f_status', 'status_count')
                    
                    dateStatusCount = {}    # {'날짜' : { 'status_code' : 'status_count'}, '날짜' : { 'status_code' : 'status_count'}, ...}
                    statusCount = {}
                    
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
                        statusCount[row['f_status']] = row['status_count']
                        dateStatusCount[row['f_date']] = copy.deepcopy(statusCount)
                        
                    for xDate in resultX:
                        for yStatusCode in resultStatusCode:
                            
                            if yStatusCode == '2' and yStatusCode in dateStatusCount[xDate] :
                                resultY_200.append(dateStatusCount[xDate][yStatusCode])
                            elif yStatusCode == '3' and yStatusCode in dateStatusCount[xDate] :
                                resultY_300.append(dateStatusCount[xDate][yStatusCode])
                            elif yStatusCode == '4' and yStatusCode in dateStatusCount[xDate] :
                                resultY_400.append(dateStatusCount[xDate][yStatusCode])
                            elif yStatusCode == '5' and yStatusCode in dateStatusCount[xDate] :
                                resultY_500.append(dateStatusCount[xDate][yStatusCode])
                            else:
                                #print('There is no available status code.')
                                pass
                            
                    print("== 전체 시간 : ", time.time() - start_time)
                        
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
                            resultY_time.append(row['yt'])
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
            print('Error Occured while creating chartdata...', ex)
                    
            response = {'message': 'chartdata creation failed.'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
             
    def create(self, request, *args, **kwargs):
            
        print("== DynamicLogDetailViewSet create!!")

        start = time.time()
        response = {}
        
        try:
            
            logfile_id = request.data['logfile_id']
            project_id = request.data['project_id']
            
            model_name = "logdetail_"+project_id
            
            print("create model_name :", model_name)
            
      
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
                
                # [병렬처리] Log Parsing : postgresql copy 사용을 위해 csv파일 생성
                id_startnum = 0
                if LogDetail_dynamic.objects.count() > 0:
                    id_startnum = LogDetail_dynamic.objects.all().order_by("-id")[0].id + 1
                
                self.parse_log(logfile, logfile_id, id_startnum)
            
                # postgresql copy 실행                
                LogDetail_dynamic.objects.model.objects = CopyManager()
                LogDetail_dynamic.objects.model = ModelSchema.objects.get(name=model_name).as_model()
                
                LogDetail_dynamic.objects.from_csv(logfile.name+'.csv', delimiter=',')        
                    
                print("To DB, Total Duration :", time.time() - start)
                
                response = {'message': 'logdetail created successfully.'}
                
            return Response(response, status = status.HTTP_200_OK)
        
        except Exception as ex: 
            print('Error Occured while creating logdetail...', ex)
            
            response = {'message': 'logdetail creation failed.'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def parse_log(self, logfile, logfile_id, existed_row_size):
    
        log_lines = []
        result = []
        count = 0               
        start = time.time()
        
        # Fileformat 가져온다.(from logfile DB using logfile_id)
        # 예시 : log_format = '%h %l %u %t \"%r\" %>s %b'      
        format_model = LogFile.objects.get(logfile_id=logfile_id)
        log_format = format_model.file_format
        
        # format_kind : apache, nginx, IIS
        format_kind = format_model.format_kind        
        format_name = format_model.format_name
                
        # 임시 csv 파일생성 for copy to postgresql
        # For dynamic : logdetail_id -> id
        log_line_header = ['id','log_line','fhour','fminute','fsecond','fip','freferer','fuser_agent',
                           'fstatus','ftime_taken','freserve1','freserve2','freserve3','created','logfile_id',
                           'frequest','fday','fmonth','fyear','fdate','ftime','fdatetime','fbyte', 'fextension']
        
        # pandas 활용 - 로그파일 읽기
        # TODO: %{X-Forwarded-For}i 의 경우 열의 개수가 늘어나는데...전처리를 어떻게 해야 하나? => 이거 일단 패스(error line 빼고 처리)
        # df_logs = pd.read_csv(logfile.name, encoding="utf-8", error_bad_lines=False, header=None, delimiter=" ", escapechar="\\", na_filter=False, dtype={'freferer':np.str})
                
        df_logs = None
        try:
            df_logs = pd.read_csv(logfile.name, encoding="utf-8", error_bad_lines=False, header=None, delimiter=" ", escapechar="\\", na_filter=False, quotechar='"')
            
        except UnicodeDecodeError as ude:
            
            print('UnicodeDecodeError Occured! Trying again with another encoding = cp1252 : ', ude)    
            
            try:
                df_logs = pd.read_csv(logfile.name, encoding="cp1252", error_bad_lines=False, header=None, delimiter=" ", escapechar="\\", na_filter=False, quotechar='"')
            except Exception as uex:
                print('UnicodeDecodeError Occured AGAIN!')
                raise uex            
            
        except Exception as ex: 
            print('Error Occured while creating logdetail read_csv#1...', ex)            
            raise ex
                        
        # TODO: format_kind - Apache, Nginx, IIS를 구분해야 한다.
        
        # {'h': 0, 't': 3, 'r': 4, 's': 5} 이런 형태
        # 예시 : log_format = '%h %l %u %t \"%r\" %>s %b'
        format_index = self.get_logformat_index(log_format, format_kind)
        
        # 'log_line' : 그대로 들어가야 한다. - Delimiter가 없다.("@" 명시, @ 사용하지 않을 것임...오류나는지 확인필요, \t 이런걸로?)
        
        df_logs_all = None
        try:
            df_logs_all = pd.read_csv(logfile.name, encoding="utf-8", header=None, delimiter="\t", error_bad_lines=False, escapechar="\\", na_filter=False)
            
        except UnicodeDecodeError as ude:
            
            print('UnicodeDecodeError Occured! Trying again with another encoding = cp1252 : ', ude)    
            
            try:
                df_logs_all = pd.read_csv(logfile.name, encoding="cp1252", header=None, delimiter="\t", error_bad_lines=False, escapechar="\\", na_filter=False)
            except Exception as uex:
                print('UnicodeDecodeError Occured AGAIN!')
                raise uex            
            
        except Exception as ex: 
            print('Error Occured while creating logdetail read_csv#2 whole lines...', ex)            
            raise ex
        
        df_logs['log_line'] = df_logs_all
        
        # 읽어들인 Dataframe에서 Merge하기 : 성능향상 목적(File에서 한번 더 읽는 것보다 빠르다.)
        #df_logs['log_line'] = df_logs[df_logs.columns[0:]].apply(lambda x: ' '.join(x.astype(str)), axis=1)              
                
        # if 'h' in log_format:
        if log_format.find('h') != -1:
            df_logs.rename(columns = {format_index['h'] : 'fip'}, inplace = True)
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
        if log_format.find('T') != -1:
            df_logs.rename(columns = {format_index['T'] : 'ftime_taken'}, inplace = True)
            time_taken_flag = True

        if (not time_taken_flag) & (log_format.find('D') != -1):
            df_logs.rename(columns = {format_index['D'] : 'ftime_taken'}, inplace = True)
        else:
            df_logs['ftime_taken'] = -1
        
        #'freserve1', 'freserve2', 'freserve3'
        df_logs['freserve1'] = ''
        df_logs['freserve2'] = ''
        df_logs['freserve3'] = ''
        
        #'created'
        datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        df_logs['created'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')
                
        #'logfile_id'
        df_logs['logfile_id'] = logfile_id
        
        #'fhour', #'fminute', #'fsecond', #'fday', #'fmonth', #'fyear'
        # 시간관련, dummy는 , 때문에
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
        p = re.compile('(.js|.html|.ico|.jpg|.png|.bmp|.otf|.css)', re.DOTALL )
        df_logs['fextension'] = df_logs['frequest'].apply(lambda x: p.findall(x)[0][1:] if len(p.findall(x)) > 0 else '-')
        
        # Merge : logdetail_id -> id
        # ID 기존의 개수 + 1 만큼 + 해주어야 한다. 0부터 시작이므로        
        df_logs = df_logs.rename_axis('id').reset_index()
        df_logs['id'] = df_logs['id'] + existed_row_size
        
        df_logs = pd.concat([df_logs, df_time], axis=1)
        
        # 보완로직2 - 결측치 제거 : None있으면 해당 row 제거
        df_logs.dropna(axis=0, inplace=True)
                        
        # index 미사용  
        df_logs[log_line_header].to_csv(logfile.name+'.csv', index=False)
       
        print("Duration to create temporary csv :", time.time() - start)
    
    def get_logformat_index(self, log_format, format_kind):
        format_index = {}
        index = 0
        for tmp in log_format.split(sep=' '):
            
            if format_kind == 'apache':
                if tmp.find('Referer') != -1:
                    format_index['Referer'] = index
                elif tmp.find('User-Agent') != -1:
                    format_index['User-Agent'] = index
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
                elif "%D" in tmp:
                    format_index['D'] = index
                elif "%T" in tmp:
                    format_index['T'] = index                
            
            # TODO : nginx, IIS                    
            elif format_kind == 'nginx':
                pass
            elif format_kind == 'IIS':
                pass
                
            index = index + 1 
            
        return format_index    

        
    
    

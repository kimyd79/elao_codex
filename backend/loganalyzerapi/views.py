from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import viewsets, status
from rest_framework.renderers import JSONRenderer
from loganalyzerapi.models import LogMaster, LogFile, LogDetail, LogFormat, LogFormatString
from loganalyzerapi.serializers import LogMasterSerializer, LogDetailSerializer, LogFileSerializer, LogFormatSerializer, LogFormatStringSerializer, UserSerializer
import time, uuid, re, csv, io
from datetime import datetime, timezone
from rest_framework.response import Response
from django.db import transaction
import pandas as pd
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum, Max, Min, Avg
from django.db.models.functions import Concat, Coalesce, Substr
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

import copy

# for test
from django.core import serializers
from django.db import connection, transaction

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
    
    @action(methods=['post'], detail=False)
    def notice(self, request, pk=None):
        logfile_id = request.data['logfile_id']
        
        print('notice logfile_id : ', logfile_id)
        
        tempset = LogDetail.objects.filter(logfile_id=logfile_id).order_by('fdatetime')
        
        firstRow = tempset.first()
        lastRow = tempset.last()
        
        response = {'message': 'start_end returned successfully', 'start_date': firstRow.fdate, 'start_time': firstRow.ftime, 'end_date': lastRow.fdate, 'end_time': lastRow.ftime }        
        return Response(response, status = status.HTTP_200_OK)
    
    @action(methods=['post'], detail=False)
    def start_end(self, request, pk=None):
        logfile_id = request.data['logfile_id']
        
        print('start_end logfile_id : ', logfile_id)
        
        tempset = LogDetail.objects.filter(logfile_id=logfile_id).order_by('fdatetime')
        
        firstRow = tempset.first()
        lastRow = tempset.last()
        
        response = {'message': 'start_end returned successfully', 'start_date': firstRow.fdate, 'start_time': firstRow.ftime, 'end_date': lastRow.fdate, 'end_time': lastRow.ftime }        
        return Response(response, status = status.HTTP_200_OK)
        
    
    # For Statistics - chartdata    
    @action(methods=['post'], detail=False)
    def chartdata(self, request, pk=None):
        logfile_id = request.data['logfile_id']
        
        type = request.data['type']
        kind = request.data['kind']
        print("** chartdata : type, kind --> ", type, kind)
        
        # 검색 조건 적용
        queryset = self.get_queryset()
        
        #1. TODO : 기본 조건 적용(file_id) -> Multi-file 일 경우 project_id까지 봐야한다.
        queryset = queryset.filter(logfile_id__exact=logfile_id)        
        
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

        # Type1 : 시(HH)기준
        #   Kind1 : request(요청) 건수(count)        
        #   Kind2 : status code 건수(count)
        #   Kind3 : time-taken 시간(max, min, count)
        
        start_time = time.time()
        
        #type=1. 시(HH)기준
        if type == '1':          

            if(kind == 1):
                
                hhRequest = queryset.values('fdate','fhour').order_by('fdate', 'fhour').annotate(x=Concat('fdate', 'fhour'), y=Count('frequest'))
                rows = hhRequest.values('x','y')
                              
                for row in rows:
                    print("type1, kind1 : request(요청) 건수(count) x - ",row['x'])
                    print("type1, kind1 : request(요청) 건수(count) y - ",row['y'])
                    
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
                    print("type1, kind2 : status code 건수(count) x - ",row['f_date'])
                    print("type1, kind2 : status code 건수(count) y - ",row['f_status'])
                    print("type1, kind2 : status code 건수(count) y - ",row['status_count'])
                    
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
                        
                        if yStatusCode == '2':
                            resultY_200.append(dateStatusCount[xDate][yStatusCode])
                        elif yStatusCode == '3':
                            resultY_300.append(dateStatusCount[xDate][yStatusCode])
                        elif yStatusCode == '4':
                            resultY_400.append(dateStatusCount[xDate][yStatusCode])
                        elif yStatusCode == '5':
                            resultY_500.append(dateStatusCount[xDate][yStatusCode])
                        else:
                            print('There is no available status code.')
                           
                print("== 전체 시간 : ", time.time() - start_time)
                
            elif(kind == 3):
                # Step1 : logfile_id 로 Logfile 에서 Format 찾아서 %D나 %T 있는지 확인하고
                # Step2 : 있으면 단위까지 리턴한다. 없으면 비어있는 결과로 리턴한다.
                file_format = LogFile.objects.get(logfile_id=logfile_id).file_format
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
                        print("type1, kind3 : request(요청) 건수(count) x - ",row['x'])
                        print("type1, kind3 : request(요청) 건수(count) y - ",row['y'])
                        print("type1, kind3 : time-taken(요청) 건수(count) y - ",row['yt'])
                        
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
                print("== 쿼리 시간 : ", time.time() - start_time)
                rows = hhmmRequest.values('x','y')
                
                for row in rows:
                    print("type2, kind1 : request(요청) 건수(count) x - ",row['x'])
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
                    print("type1, kind2 : status code 건수(count) x - ",row['f_date'])
                    print("type1, kind2 : status code 건수(count) y - ",row['f_status'])
                    print("type1, kind2 : status code 건수(count) y - ",row['status_count'])
                    
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
                file_format = LogFile.objects.get(logfile_id=logfile_id).file_format
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
                        print("type2, kind3 : request(요청) 건수(count) x - ",row['x'])
                        print("type2, kind3 : request(요청) 건수(count) y - ",row['y'])
                        print("type2, kind3 : time-taken(요청) 건수(count) y - ",row['yt'])
                        
                        resultX.append(row['x'])
                        resultY.append(row['y'])
                        resultY_time.append(row['yt'])
                else:
                    pass
                
        response = {'message': 'linechartdata returned successfully', 'resultX': resultX, 'resultY': resultY, 'resultY_time': resultY_time, 'resultY_time_unit': resultY_time_unit, 'resultY_200': resultY_200, 'resultY_300': resultY_300, 'resultY_400': resultY_400, 'resultY_500': resultY_500}        
        return Response(response, status = status.HTTP_200_OK)
    
    
    # For Statistics - top1
    @action(methods=['post'], detail=False)
    def statistics_top1(self, request, pk=None):
    
        logfile_id = request.data['logfile_id']
        
        type = request.data['type']
        print("** statistics_top1 : type --> ", type)
        
        # 결과 처리
        result = []
        
        # 검색 조건 적용
        queryset = self.get_queryset()
        
        #0. TODO: 기본 조건 적용(file_id) -> Multi-file 일 경우 project_id까지 봐야한다.
        queryset = queryset.filter(logfile_id__exact=logfile_id)
        
        #2. TODO: 아래 결과 key 동일하게 맞추기 - for 화면처리 
        
        start_time = time.time()
       
        #type=1. 전체 처리량(건수)
        if type == 1:
            cnt = queryset.count()
            print("type1 : queryset.count() - ", cnt)
            result.append({"result" : 'Total', "result_count" : cnt})
               
        #type=2. 최다접속 IP주소
        elif type == 2:
            top_ip = queryset.values('fip').annotate(fip_count=Count('fip')).order_by('-fip_count').values('fip', 'fip_count')[0]
            print("type2 : TOP IP - ", top_ip['fip'])
            print("type2 : TOP IP Count - ", top_ip['fip_count'])
            result.append({"result" : top_ip['fip'], "result_count" : top_ip['fip_count']})
        
        #type=3. 최다접속 사용자 요청(request)
        elif type == 3:
            top_request =  queryset.values('frequest').annotate(frequest_count=Count('frequest')).order_by('-frequest_count').values('frequest', 'frequest_count')[0]
            print("type3 : TOP REQUEST - ", top_request['frequest'])
            print("type3 : TOP REQUEST Count - ", top_request['frequest_count'])
            result.append({"result" :  top_request['frequest'], "result_count" : top_request['frequest_count']})
            
        #type=4. 최다 404 발생 URL
        elif type == 4:
            
            try:
                top_404_request = queryset.filter(fstatus__startswith='404').values('frequest').annotate(frequest_404_count=Count('frequest')).order_by('-frequest_404_count').values('frequest', 'frequest_404_count')[0]
            
                print("type4 : TOP 404 REQUEST - ", top_404_request['frequest'])
                print("type4 : TOP 404 REQUEST Count - ", top_404_request['frequest_404_count'])
                result.append({"result" :  top_404_request['frequest'], "result_count" : top_404_request['frequest_404_count']})
            except :
                print("Error occured!")
                result.append({"result" : "-", "result_count" : "0"})                           
        
        print("== statistics_top1 (type="+str(type)+")걸린 시간 : ", time.time() - start_time) 
                            
        response = {'message': 'statistics returned', 'results': result}
        return Response(response, status = status.HTTP_200_OK)
    
     # For Statistics - top5
    @action(methods=['post'], detail=False)
    def statistics_top5(self, request, pk=None):
        
        logfile_id = request.data['logfile_id']
                       
        type = request.data['type']
        print("** statistics_top5 : type --> ", type)
                
        # 검색 조건 적용
        queryset = self.get_queryset()
        
        #1. TODO : 기본 조건 적용(file_id) -> Multi-file 일 경우 project_id까지 봐야한다.
        queryset = queryset.filter(logfile_id__exact=logfile_id)        
                
        results = []
        
        start_time = time.time()
        
        #type=1. Status Codes Top5        
        if type == 1:
            top5_status = queryset.values('fstatus').annotate(fstatus_count=Count('fstatus')).order_by('-fstatus_count')[0:5]                        
            rows = top5_status.values('fstatus','fstatus_count')
            
            for row in rows:
                print("type1 : TOP5 STATUS - ", row['fstatus'])
                print("type1 : TOP5 STATUS Count - ", row['fstatus_count'])
                
                results.append({"result" : row['fstatus'], "result_count" : row['fstatus_count']})                      
        
        #type=2. Requests Top5
        elif type == 2:
            top5_request = queryset.values('frequest').annotate(frequest_count=Count('frequest')).order_by('-frequest_count')[0:5]
            rows = top5_request.values('frequest','frequest_count')
            
            for row in rows:
                print("type2 : TOP5 REQUEST - ", row['frequest'])
                print("type2 : TOP5 REQUEST Count - ", row['frequest_count'])
                
                results.append({"result" : row['frequest'], "result_count" : row['frequest_count']})   
                    
        #type=3. 최다 404 발생 URL Top5
        elif type == 3:
            top5_404_request = queryset.filter(fstatus__startswith='404').values('frequest').annotate(frequest_404_count=Count('frequest')).order_by('-frequest_404_count')[0:5]
            rows = top5_404_request.values('frequest','frequest_404_count')
            
            if rows.count() > 0 :
                for row in rows:
                    print("type3 : TOP5 404 REQUEST - ", row['frequest'])
                    print("type3 : TOP5 404 REQUEST Count - ", row['frequest_404_count'])
                    
                    results.append({"result" : row['frequest'], "result_count" : row['frequest_404_count']}) 
            else:
                results.append({"result" : "-", "result_count" : "0" }) 
            
        #type=4. Time-taken Top5(오래 걸린시간)
        elif type == 4:
            top5_timetaken_request = queryset.order_by('-ftime_taken')[0:5]
            rows = top5_timetaken_request.values('frequest','ftime_taken')
            
            for row in rows:
                print("type3 : TOP5 Timtaken REQUEST - ", row['frequest'])
                print("type3 : TOP5 Timtaken REQUEST Count - ", row['ftime_taken'])
                
                results.append({"result" : row['frequest'], "result_count" : row['ftime_taken']})             
                
        #type=5. Visitor(Unique IP) Top5
        elif type == 5:
            top5_visitor = queryset.values('fip').annotate(fip_count=Count('fip')).order_by('-fip')[0:5]
            rows = top5_visitor.values('fip','fip_count')
            
            for row in rows:
                print("type2 : TOP5 VISITOR - ", row['fip'])
                print("type2 : TOP5 VISITOR Count - ", row['fip_count'])
                
                results.append({"result" : row['fip'], "result_count" : row['fip_count']})   
        
        #type=6. Search Terms Top5     
        
        
        print("== statistics_top1 (type="+str(type)+")걸린 시간 : ", time.time() - start_time)
        
        # TODO : 결과값을 생성해서 보내야 한다 & Exception 처리
        response = {'message': 'statistics returned', 'results': results}
        return Response(response, status = status.HTTP_200_OK)
        
        
    
    # For Filtering
    def get_queryset(self):
        
        print("== LogDetailViewSet get_queryset!!")
        
        queryset = LogDetail.objects.all()
        
        # Request Method 확인
        method = ""
        for key in self.action_map:
            if self.action_map[key] == self.action:
                method = key
                break
        print("method = ", method)
        
        dateFromValue = ""
        dateToValue = ""
        timeFromValue = ""
        timeToValue = ""
        ttFromValue = ""
        ttToValue = ""
        conditionValue = ""
        searchValue = ""        

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
        
        elif method == 'post':
            
            dateFromValue = self.request.data['filter']['dateFromValue'] if self.request.data['filter']['dateFromValue'] != '' else None
            dateToValue = self.request.data['filter']['dateToValue'] if self.request.data['filter']['dateToValue'] != '' else None
            timeFromValue = self.request.data['filter']['timeFromValue'] if self.request.data['filter']['timeFromValue'] != '' else None
            timeToValue = self.request.data['filter']['timeToValue'] if self.request.data['filter']['timeToValue'] != '' else None

            ttFromValue = self.request.data['filter']['ttFromValue'] if self.request.data['filter']['ttFromValue'] != '' else None
            ttToValue = self.request.data['filter']['ttToValue'] if self.request.data['filter']['ttToValue'] != '' else None

            conditionValue = self.request.data['filter']['conditionValue'] if self.request.data['filter']['conditionValue'] != '' else None
            searchValue = self.request.data['filter']['searchValue'] if self.request.data['filter']['searchValue'] != '' else None
        
        # Date, Time : Between
        if (dateFromValue is not None) and (dateToValue is not None) and (timeFromValue is not None) and (timeToValue is not None):
            start_datetime = dateFromValue + timeFromValue
            end_datetime = dateToValue + timeToValue
            queryset = queryset.filter(fdatetime__range=(start_datetime, end_datetime))
            print('Date and Time applied!')
        
        # Time-taken : Between
        if (ttFromValue is not None) and (ttToValue is not None):        
            queryset = queryset.filter(ftime_taken__range=(ttFromValue, ttToValue))
            print('Time-taken applied!')
            
        # conditionValue : Contain
        if conditionValue is not None :
            print('conditionValue applied! (conditionValue) : ', conditionValue)
            print('searchValue : ', searchValue)
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
        
        # For UI
        logfile_id = request.data['logfile']
                
        logfile_model = LogFile.objects.get(logfile_id=logfile_id)   
        logfile = logfile_model.file_object.file    
        
        print("logfile :", logfile)     
        
        # [병렬처리] Log Parsing : postgresql copy 사용을 위해 csv파일 생성
        result = self.parse_log(logfile, logfile_id)      
     
        # postgresql copy 실행
        LogDetail.objects.from_csv(logfile.name+'.csv', delimiter=',')        
            
        print("To DB, Total Duration :", time.time() - start)
        
        response = {'message': 'logdetail created', 'start_date': result[0]['firstRow'].fdate, 'start_time': result[0]['firstRow'].ftime, 'end_date': result[0]['lastRow'].fdate, 'end_time': result[0]['lastRow'].ftime }
        return Response(response, status = status.HTTP_200_OK)

    def parse_log(self, logfile, logfile_id):

        log_lines = []
        result = []
        count = 0               
        start = time.time()
        
        # Fileformat 가져온다.(from logfile DB using logfile_id)
        # 예시 : log_format = '%h %l %u %t \"%r\" %>s %b'      
        log_format = LogFile.objects.get(logfile_id=logfile_id).file_format
        
        # format_kind : apache, nginx, IIS
        format_kind = LogFile.objects.get(logfile_id=logfile_id).format_kind        
        format_name = LogFile.objects.get(logfile_id=logfile_id).format_name
                
        # 임시 csv 파일생성 for copy to postgresql
        log_line_header = ['logdetail_id','log_line','fhour','fminute','fsecond','fip','freferer','fuser_agent',
                           'fstatus','ftime_taken','freserve1','freserve2','freserve3','created','logfile_id',
                           'frequest','fday','fmonth','fyear','fdate','ftime','fdatetime']
        
        # pandas 활용 - 로그파일 읽기
        # TODO : %{X-Forwarded-For}i 의 경우 열의 개수가 늘어나는데...전처리를 어떻게 해야 하나? => 이거 일단 패스(error line 빼고 처리)
        df_logs = pd.read_csv(logfile.name, encoding="utf-8", error_bad_lines=False, header=None, delimiter=" ", escapechar="\\", na_filter=False)
                
        # TODO : format_kind - Apache, Nginx, IIS를 구분해야 한다.
        
        # {'h': 0, 't': 3, 'r': 4, 's': 5} 이런 형태
        # 예시 : log_format = '%h %l %u %t \"%r\" %>s %b'
        format_index = self.get_logformat_index(log_format, format_kind)
        
        # 'log_line' : 그대로 들어가야 한다. - Delimiter가 없다.("@" 명시, @ 사용하지 않을 것임...오류나는지 확인필요, \t 이런걸로?)
        df_logs_all = pd.read_csv(logfile.name, encoding="utf-8", header=None, delimiter="\t", error_bad_lines=False, escapechar="\\", na_filter=False)                
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

        month_map = {
            'Jan' : '01', 'Feb' : '02', 'Mar' : '03', 'Apr' : '04', 'May' : '05', 'Jun' : '06',
            'Jul' : '07', 'Aug' : '08', 'Sep' : '09', 'Oct' : '10', 'Nov' : '11', 'Dec' : '12',
        }

        df_time['fmonth'] = df_time['fmonth'].apply(lambda x : month_map[x])
        
        # Add Columns : fdate YYYYMMDD(fyear+fmonth+fday), ftime hhmmss(fhour+fminute+fsecond), fdatetime(YYYYMMDDhhmmss)
        df_time['fdate'] = df_time['fyear'] + df_time['fmonth'] + df_time['fday']
        df_time['ftime'] = df_time['fhour'] + df_time['fminute'] + df_time['fsecond']
        df_time['fdatetime'] = df_time['fdate']+df_time['ftime']
        
        # Merge
        df_logs = df_logs.rename_axis('logdetail_id').reset_index()
        df_logs = pd.concat([df_logs, df_time], axis=1)
        
        # 'logdetail_id' : UUID 생성
        df_logs['logdetail_id'] = df_logs['logdetail_id'].apply(lambda x : uuid.uuid4())         
                        
        firstRow = df_logs.iloc[0,] #.to_json(orient='index'), head() function       
        lastRow = df_logs.iloc[-1,] #.to_json(orient='index'), head() function                        
                        
        # index 미사용  
        df_logs[log_line_header].to_csv(logfile.name+'.csv', index=False)
       
        print("Duration to create temporary csv :", time.time() - start)        
        
        result.append({'firstRow' : firstRow, 'lastRow' : lastRow})
        
        return result
    
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

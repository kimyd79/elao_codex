from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import viewsets, status
from rest_framework.renderers import JSONRenderer
from loganalyzerapi.models import LogMaster, LogFile, LogDetail, LogFormat, LogFormatString
from loganalyzerapi.serializers import LogMasterSerializer, LogDetailSerializer, LogFileSerializer, LogFormatSerializer, LogFormatStringSerializer
import time, uuid, re, csv
from datetime import datetime, timezone
from rest_framework.response import Response
from django.db import transaction
import pandas as pd
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Max, Min, Avg
from django.db.models.functions import Concat


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
    filter_backends = [filters.SearchFilter]
    search_fields = ['file_name']
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
    
    # For Statistics - top1
    @action(methods=['post'], detail=False)
    def chartdata(self, request, pk=None):
        logfile_id = request.data['logfile_id']
        
        type = request.data['type']
        kind = request.data['kind']
        print("** chartdata : type, kind --> ", type, kind)
        
        #0. TODO : 검색 조건 적용(공통항목으로 Extract) - 확인필요
        queryset = self.get_queryset()
        
        #1. TODO : 기본 조건 적용(file_id) -> Multi-file 일 경우 project_id까지 봐야한다.
        queryset = queryset.filter(logfile_id__exact=logfile_id)        
        
        #2. TODO : 아래 결과 key 동일하게 맞추기 - for 화면처리 
        
        # 결과 처리
        resultX = []
        resultY = []        

        # Type1 : 시(HH)기준
        #   Kind1 : request(요청) 건수(count)
        #   Kind2 : time-taken 시간(max, min, count)
        
        #type=1. 시(HH)기준
        if type == '1':
            hhRequest = queryset.values('fdate','fhour').order_by('fdate', 'fhour').annotate(x=Concat('fdate', 'fhour'), y=Count('frequest'))

            if(kind == '1'):
                for idx in range(0,hhRequest.count()):
                    print("type1, kind1 : request(요청) 건수(count) x - ", hhRequest[idx]['x'])
                    print("type1, kind1 : request(요청) 건수(count) y - ", hhRequest[idx]['y'])            
                    
                    resultX.append(hhRequest[idx]['x'])
                    resultY.append(hhRequest[idx]['y'])
            elif(kind =='2'):
                # TODO : time-taken 존재여부 Check
                pass
        
        # Type2 : 시분(HHMM)기준                    
        #   Kind1 : request(요청) 건수(count)
        #   Kind2 : time-taken 시간(max, min, count) 
        elif type == '2':          
                           
            if(kind == '1'):
                
                hhmmRequest = queryset.values('fdate','fhour','fminute').order_by('fdate','fhour','fminute').annotate(x=Concat('fdate','fhour','fminute'), y=Count('frequest'))
                
                for idx in range(0,hhmmRequest.count()):
                    print("type2, kind1 : request(요청) 건수(count) x - ", hhmmRequest[idx]['x'])
                    print("type2, kind1 : request(요청) 건수(count) y - ", hhmmRequest[idx]['y'])            
                    
                    resultX.append(hhmmRequest[idx]['x'])
                    resultY.append(hhmmRequest[idx]['y'])
            elif(kind == '2'):
                # TODO : time-taken 존재여부 Check
                pass
        
        
        response = {'message': 'chartdata returned successfully', 'resultX': resultX, 'resultY': resultY}
        return Response(response, status = status.HTTP_200_OK)
    
    
    # For Statistics - top1
    @action(methods=['post'], detail=False)
    def statistics_top1(self, request, pk=None):
    
        logfile_id = request.data['logfile_id']
        
        type = request.data['type']
        print("** statistics_top1 : type --> ", type)
        
        # 결과 처리
        result = []
        
        #0. TODO : 기본 조건 적용(file_id) -> Multi-file 일 경우 project_id까지 봐야한다.
        queryset = LogDetail.objects.filter(logfile_id__exact=logfile_id)
        
        #1. TODO : 검색 조건 적용(공통항목으로 Extract)
        
        #2. TODO : 아래 결과 key 동일하게 맞추기 - for 화면처리 
        
        #type=1. 전체 처리량(건수)
        if type == '1':
            print("type1 : queryset.count() - ", queryset.count())
            result.append({"result" : 'Total', "result_count" : queryset.count()})
               
        #type=2. 최다접속 IP주소
        elif type == '2':
            top_ip = queryset.values('fip').annotate(fip_count=Count('fip')).order_by('-fip_count')
            print("type2 : TOP IP - ", top_ip[0]['fip'])
            print("type2 : TOP IP Count - ", top_ip[0]['fip_count'])
            result.append({"result" : top_ip[0]['fip'], "result_count" : top_ip[0]['fip_count']})
        
        #type=3. 최다접속 사용자 요청(request)
        elif type == '3':
            top_request =  queryset.values('frequest').annotate(frequest_count=Count('frequest')).order_by('-frequest_count')
            print("type3 : TOP REQUEST - ", top_request[0]['frequest'])
            print("type3 : TOP REQUEST Count - ", top_request[0]['frequest_count'])
            result.append({"result" :  top_request[0]['frequest'], "result_count" : top_request[0]['frequest_count']})
            
        #type=4. 최다 404 발생 URL
        elif type == '4':
            top_404_request = queryset.filter(fstatus__startswith='404').values('frequest').annotate(frequest_404_count=Count('frequest')).order_by('-frequest_404_count')
            print("type4 : TOP 404 REQUEST - ", top_404_request[0]['frequest'])
            print("type4 : TOP 404 REQUEST Count - ", top_404_request[0]['frequest_404_count'])
            result.append({"result" :  top_404_request[0]['frequest'], "result_count" : top_404_request[0]['frequest_404_count']})
                    
        response = {'message': 'statistics returned', 'results': result}
        return Response(response, status = status.HTTP_200_OK)
    
     # For Statistics - top5
    @action(methods=['post'], detail=False)
    def statistics_top5(self, request, pk=None):
        
        logfile_id = request.data['logfile_id']
                       
        type = request.data['type']
        print("** statistics_top5 : type --> ", type)
        
        #0. TODO : 검색 조건 적용(공통항목으로 Extract) - 확인필요
        #queryset = get_queryset(self)
        
        #1. TODO : 기본 조건 적용(file_id) -> Multi-file 일 경우 project_id까지 봐야한다.
        queryset = LogDetail.objects.filter(logfile_id__exact=logfile_id)        
        
        #2. TODO : 아래 결과 key 동일하게 맞추기 - for 화면처리 
        
        results = []
        
        #type=1. Status Codes Top5
        if type == '1':
            top5_status = queryset.values('fstatus').annotate(fstatus_count=Count('fstatus')).order_by('-fstatus_count')[0:5]
            for idx in range(0,5):
                print("type1 : TOP5 STATUS - ", top5_status[idx]['fstatus'])
                print("type1 : TOP5 STATUS Count - ", top5_status[idx]['fstatus_count'])
                
                results.append({"result" : top5_status[idx]['fstatus'], "result_count" : top5_status[idx]['fstatus_count']})
        
        #type=2. Requests Top5
        elif type == '2':
            top5_request =  queryset.values('frequest').annotate(frequest_count=Count('frequest')).order_by('-frequest_count')[0:5]
            for idx in range(0,5):
                print("type2 : TOP5 REQUEST - ", top5_request[idx]['frequest'])
                print("type2 : TOP5 REQUEST Count - ", top5_request[idx]['frequest_count'])
                
                results.append({"result" : top5_request[idx]['frequest'], "result_count" : top5_request[idx]['frequest_count']})     
        
        #type=3. 최다 404 발생 URL Top5
        elif type == '3':
            top5_404_request = queryset.filter(fstatus__startswith='404').values('frequest').annotate(frequest_404_count=Count('frequest')).order_by('-frequest_404_count')
            for idx in range(0,5):
                print("type4 : TOP 404 REQUEST - ", top5_404_request[idx]['frequest'])
                print("type4 : TOP 404 REQUEST Count - ", top5_404_request[idx]['frequest_404_count']) 
                
                results.append({"result" : top5_404_request[idx]['frequest'], "result_count" : top5_404_request[idx]['frequest_404_count']})      
            
         #type=4. Search Terms Top5     
        
        # TODO : 결과값을 생성해서 보내야 한다 & Exception 처리
        
        response = {'message': 'statistics returned', 'results': results}
        return Response(response, status = status.HTTP_200_OK)
        
        
    
    # For Gridtable Filtering
    def get_queryset(self):
        
        print("== LogDetailViewSet get_queryset!!")
        
        queryset = LogDetail.objects.all()

        # 조건 적용
        dateFromValue = self.request.query_params.get('dateFromValue', None)
        dateToValue = self.request.query_params.get('dateToValue', None)
        timeFromValue = self.request.query_params.get('timeFromValue', None)
        timeToValue = self.request.query_params.get('timeToValue', None)
        
        ttFromValue = self.request.query_params.get('ttFromValue', None)
        ttToValue = self.request.query_params.get('ttToValue', None)
        
        conditionValue = self.request.query_params.get('conditionValue', None)
        searchValue = self.request.query_params.get('searchValue', None)
        
        # Date, Time : Between
        if (dateFromValue is not None) and (dateToValue is not None) and (timeFromValue is not None) and (timeToValue is not None):
            start_datetime = dateFromValue + timeFromValue
            end_datetime = dateToValue + timeToValue
            queryset = queryset.filter(fdatetime__range=(start_datetime, end_datetime))
        
        # Time-taken : Between
        if (ttFromValue is not None) and (ttToValue is not None):        
            queryset = queryset.filter(ftime_taken__range=(ttFromValue, ttToValue))
            
        # conditionValue : Contain
        if conditionValue is not None :
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
        
        # For Basic
        #data = request.data.dict()
        #logfile_id = data["logfile"]        
        
        # For UI
        logfile_id = request.data['logfile']
                
        logfile_model = LogFile.objects.get(logfile_id=logfile_id)   
        logfile = logfile_model.file_object.file         
        
        # Log Parsing : postgresql copy 사용을 위해 csv파일 생성
        firstRow = self.parse_log(logfile, logfile_id)      
        
        # postgresql copy 실행
        LogDetail.objects.from_csv(logfile.name+'.csv', delimiter=',')        
            
        print("To DB, Total Duration :", time.time() - start)
        
        # print("==serializer.data : ", serializer.data)        
        # 건수만 리턴하자. 
        #response = {'message': 'logdetail created', 'result': len(serializer.data)}
        response = {'message': 'logdetail created', 'result': firstRow}
        return Response(response, status = status.HTTP_200_OK)

    def parse_log(self, logfile, logfile_id):

        log_lines = []
        count = 0               
        start = time.time()
        
        # TODO : Fileformat 가져오기(from DB)
        log_format = '%h %l %u %t \"%r\" %>s %b'      
        
        # 임시 csv 파일생성 for copy to postgresql
        log_line_header = ['logdetail_id','log_line','fhour','fminute','fsecond','fip','freferer','fuser_agent','fstatus','ftime_taken','freserve1','freserve2','freserve3','created','logfile_id','frequest','fday','fmonth','fyear','fdate','ftime','fdatetime']
        
        # TODO : Log Body생성 - pandas 활용
        # 
        df_logs = pd.read_csv(logfile.name, header=None, delimiter=" ",)
        
        # {'h': 0, 't': 3, 'r': 4, 's': 5} 이런 형태
        format_index = self.get_logformat_index(log_format)
        
        #'log_line' : 그대로 들어가야 한다.
        df_logs_all = pd.read_csv(logfile.name, header=None)
        df_logs['log_line'] = df_logs_all
        
        if 'h' in log_format:
            df_logs.rename(columns = {format_index['h'] : 'fip'}, inplace = True)
        else:
            df_logs['fip'] = 'NA' 
            
        if 'r' in log_format:
            df_logs.rename(columns = {format_index['r'] : 'frequest'}, inplace = True)
        else:
            df_logs['frequest'] = 'NA'    

        if 's' in log_format:
            df_logs.rename(columns = {format_index['s'] : 'fstatus'}, inplace = True)
        else:
            df_logs['fstatus'] = 'NA'

        if 'Referer' in log_format:
            df_logs.rename(columns = {format_index['Referer'] : 'freferer'}, inplace = True)
        else:
            df_logs['freferer'] = 'NA'
            
        if 'User-agent' in log_format:
            df_logs.rename(columns = {format_index['User-agent'] : 'fuser_agent'}, inplace = True)
        else:
            df_logs['fuser_agent'] = 'NA'

        time_taken_flag = False    
        if 'T' in log_format:
            df_logs.rename(columns = {format_index['T'] : 'ftime_taken'}, inplace = True)
            time_taken_flag = True

        if (not time_taken_flag) & ('D' in log_format):
            df_logs.rename(columns = {format_index['D'] : 'ftime_taken'}, inplace = True)
        else:
            df_logs['ftime_taken'] = -1
        
        #'freserve1'
        #'freserve2'
        #'freserve3'
        df_logs['freserve1'] = ''
        df_logs['freserve2'] = ''
        df_logs['freserve3'] = ''
        
        #'created'
        datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        df_logs['created'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')
                
        #'logfile_id'
        df_logs['logfile_id'] = logfile_id
        
        #'fhour' 
        #'fminute'
        #'fsecond'
        #'fday'
        #'fmonth'
        #'fyear'
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
        
        # 합치기
        df_logs = df_logs.rename_axis('logdetail_id').reset_index()
        df_logs = pd.concat([df_logs, df_time], axis=1)
        
        firstRow = df_logs.iloc[0,] #.to_json(orient='index')
        
        #'logdetail_id' : UUID 생성로직 필요        
        df_logs['logdetail_id'] = df_logs['logdetail_id'].apply(lambda x : uuid.uuid4()) 
        
                        
        # index 미사용  
        df_logs[log_line_header].to_csv(logfile.name+'.csv', index=False)
       
               # TODO : 시간이 좀 걸린다. 확인해볼것
        print("Duration to create temporary csv :", time.time() - start)        
        
        # 화면에서 사용할 정보(시작시간 등)를 리턴하기 위해 1라인을 결과로 뽑는다.
        return firstRow
    
    def get_logformat_index(self, log_format):
        format_index = {}
        index = 0
        for tmp in log_format.split(sep=' '):
            #print(tmp)
            if "h" in tmp:
                format_index['h'] = index
            elif "t" in tmp:
                format_index['t'] = index
                index = index + 1 # 하나 더 세야 한다.
            elif "r" in tmp:
                format_index['r'] = index
            elif "s" in tmp:
                format_index['s'] = index
            elif "D" in tmp:
                format_index['D'] = index
            elif "T" in tmp:
                format_index['T'] = index
            elif "Referer" in tmp:
                format_index['Referer'] = index
            elif "User-agent" in tmp:
                format_index['User-agent'] = index
                
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
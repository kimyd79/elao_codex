from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import viewsets, status
from loganalyzerapi.models import LogMaster, LogFile, LogDetail
from loganalyzerapi.serializers import LogMasterSerializer, LogDetailSerializer, LogFileSerializer
import time, uuid, re, csv
from datetime import datetime, timezone
from rest_framework.response import Response
from django.db import transaction
import pandas as pd
from rest_framework import filters

# 기본 CRUD생성
class LogMasterViewSet(viewsets.ModelViewSet):
    queryset = LogMaster.objects.all()
    serializer_class = LogMasterSerializer
    
    # TODO : 미사용시 settings.py에서 DjangoFilterBackend 삭제
    #filterset_fields = ['project_name', 'uploader']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    # Multiple Search
    # http://127.0.0.1:8000/logmaster/?search=aa,22
    search_fields = ['project_name', 'project_description', 'uploader']
    
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
    
    # Pagination : LimitOffsetPagination
    # http://127.0.0.1:8000/logdetail/?limit=10&offset=20
    
    def create(self, request, *args, **kwargs):
        
        print("== LogDetailViewSet create!!")
        start = time.time()
        
        data = request.data.dict()
        logfile_id = data["logfile"]        
                
        logfile_model = LogFile.objects.get(logfile_id=logfile_id)   
        logfile = logfile_model.file_path.file         
        
        # Log Parsing : postgresql copy 사용을 위해 csv파일 생성
        self.parse_log(logfile, logfile_id)      
        
        # postgresql copy 실행
        LogDetail.objects.from_csv(logfile.name+'.csv', delimiter=',')        
            
        print("To DB, Total Duration :", time.time() - start)
        
        # print("==serializer.data : ", serializer.data)        
        # 건수만 리턴하자. 
        #response = {'message': 'logdetail created', 'result': len(serializer.data)}
        response = {'message': 'logdetail created', 'result': 'TEST'}
        return Response(response, status = status.HTTP_200_OK)

    def parse_log(self, logfile, logfile_id):

        log_lines = []
        count = 0               
        start = time.time()
        
        # TODO : Fileformat 가져오기(from DB)
        log_format = '%h %l %u %t \"%r\" %>s %b'      
        
        # 임시 csv 파일생성 for copy to postgresql
        log_line_header = ['logdetail_id','log_line','fhour','fminute','fsecond','fip','freferrer','fuser_agent','fstatus','ftime_taken','freserve1','freserve2','freserve3','created','logfile_id','frequest','fday','fmonth','fyear']
        
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
            df_logs.rename(columns = {format_index['Referer'] : 'freferrer'}, inplace = True)
        else:
            df_logs['freferrer'] = 'NA'
            
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
            'Jan' : 1, 'Feb' : 2, 'Mar' : 3, 'Apr' : 4, 'May' : 5, 'Jun' : 6,
            'Jul' : 7, 'Aug' : 8, 'Sep' : 9, 'Oct' : 10, 'Nov' : 11, 'Dec' : 12,
        }

        df_time['fmonth'] = df_time['fmonth'].apply(lambda x : month_map[x])       
        
        # 합치기
        df_logs = df_logs.rename_axis('logdetail_id').reset_index()
        df_logs = pd.concat([df_logs, df_time], axis=1)
        
        #'logdetail_id' : UUID 생성로직 필요        
        df_logs['logdetail_id'] = df_logs['logdetail_id'].apply(lambda x : uuid.uuid4()) 
                
        # index 미사용  
        df_logs[log_line_header].to_csv(logfile.name+'.csv', index=False)
       
       
        # TODO : 시간이 좀 걸린다. 확인해볼것
        print("Duration to create temporary csv :", time.time() - start)        
    
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
           

    
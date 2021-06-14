import pandas as pd
import numpy as np
import re
from datetime import datetime


#logfile = "C:\\git_workspace\\loganalyzer\\ACSError1.txt"
#logfile = "F:\\loganalyzerMedia\\logsample\\1_Apache\\3_ACS 시스템_Custom\\access-itct-20200702.log"

# Test
date_time_str = '2018-06-29 08:15:27.243'
date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
print(date_time_obj)
type(date_time_obj)

###########################################################################################################
# 시간 Adjust 기능 : 시간 +, -
# 완료
#
from datetime import datetime, timedelta
import time

datetime.now()
datetime.today().strftime('%Y-%m-%d').split('-')

datetime.now()+timedelta(seconds=5)

start = time.time()
logfile = "F:\\loganalyzerMedia\\logsample\\3_Tomcat_Access\\SSVC_access_log.2021-05-04.log"
df_logs = pd.read_csv(logfile, encoding="utf-8", error_bad_lines=False, header=None, delimiter=" ", na_filter=False)
temp_time = df_logs[3].map(lambda x: x.lstrip('[').rstrip(']'))
temp_time

# 변환 datetime
processed_time = pd.to_datetime(temp_time, format='%d/%b/%Y:%H:%M:%S')
processed_time


# 시간연산
manipulated_time = pd.DatetimeIndex(processed_time) + timedelta(hours=9)
df_datetime = pd.DataFrame(manipulated_time, dtype="str")
df_datetime
#df_datetime[3] = 100
df_datetime = df_datetime[3].str.replace(pat='[\:\/\[-]', repl= r' ', regex=True)
series = df_datetime.str.split(' ')
series
df_time = pd.DataFrame(series.tolist(), columns=['fday','fmonth','fyear','fhour','fminute','fsecond'])
df_time['fdate'] = df_time['fyear'] + df_time['fmonth'] + df_time['fday']
df_time['fdate']
df_time['ftime'] = df_time['fhour'] + df_time['fminute'] + df_time['fsecond']
df_time['ftime']
df_time['fdatetime'] = df_time['fdate']+df_time['ftime']
df_time['fdatetime']

print ("Total Duration : %s sec" % (time.time() - start))


# 기존로직 수정
start = time.time()
logfile = "F:\\loganalyzerMedia\\logsample\\3_Tomcat_Access\\SSVC_access_log.2021-05-04.log"
df_logs = pd.read_csv(logfile, encoding="utf-8", error_bad_lines=False, header=None, delimiter=" ", na_filter=False)

# 추가로직 부분 - Access Log
temp_time = df_logs[3].map(lambda x: x.lstrip('[').rstrip(']'))
temp_time


# TODO: df_time['fdatetime'] 에서 시작
# 변환 datetime
df_logs['processed_time'] = pd.to_datetime(temp_time, format='%d/%b/%Y:%H:%M:%S')

# 초단위로 환산
df_logs['processed_time']

df_logs['processed_time_shift'] = processed_time.shift(1)
df_logs['processed_time_shift']

df_logs

df_logs['max_time'] = np.where((df_logs['processed_time'] >= df_logs['processed_time_shift']) , df_logs['processed_time'], df_logs['processed_time_shift'])

# 추정 Timetaken : max_end_time - start_time
df_logs['may_time_taken'] = df_logs['max_time'] - df_logs['processed_time']
df_logs

df_logs['may_time_taken'].dt.total_seconds()


df_datetime = pd.DataFrame(processed_time, dtype="str")

df_datetime = df_datetime[3].str.replace(pat='[\:\/\[-]', repl= r' ', regex=True)
series = df_datetime.str.split(' ')
series
df_time = pd.DataFrame(series.tolist(), columns=['fday','fmonth','fyear','fhour','fminute','fsecond'])
df_time['fdate'] = df_time['fyear'] + df_time['fmonth'] + df_time['fday']
df_time['fdate']
df_time['ftime'] = df_time['fhour'] + df_time['fminute'] + df_time['fsecond']
df_time['ftime']
df_time['fdatetime'] = df_time['fdate']+df_time['ftime']
df_time['fdatetime']

print ("Total Duration : %s sec" % (time.time() - start))



# 기존로직
start = time.time()
logfile = "F:\\loganalyzerMedia\\logsample\\3_Tomcat_Access\\SSVC_access_log.2021-05-04.log"
df_logs = pd.read_csv(logfile, encoding="utf-8", error_bad_lines=False, header=None, delimiter=" ", na_filter=False)
df_logs


df_datetime = df_logs[3].str.replace(pat='[\:\/\[]', repl= r' ', regex=True)
df_datetime
series = df_datetime.str.split(' ')
df_time = pd.DataFrame(series.tolist(), columns=['dummy','fday','fmonth','fyear','fhour','fminute','fsecond'])

df_time.dropna(axis=0, inplace=True)

month_map = {
    'Jan' : '01', 'Feb' : '02', 'Mar' : '03', 'Apr' : '04', 'May' : '05', 'Jun' : '06',
    'Jul' : '07', 'Aug' : '08', 'Sep' : '09', 'Oct' : '10', 'Nov' : '11', 'Dec' : '12',
}

df_time['fmonth'] = df_time['fmonth'].apply(lambda x : month_map[x]) 

df_time['fdate'] = df_time['fyear'] + df_time['fmonth'] + df_time['fday']
df_time['fdate']
df_time['ftime'] = df_time['fhour'] + df_time['fminute'] + df_time['fsecond']
df_time['ftime']
df_time['fdatetime'] = df_time['fdate']+df_time['ftime']
df_time['fdatetime']

print ("Total Duration : %s sec" % (time.time() - start))



# 미사용
# 시간이 오래 걸린다.
fyear = manipulated_time.strftime('%Y')
fmonth = manipulated_time.strftime('%d')
fday = manipulated_time.strftime('%m')
fdate = fyear + fmonth + fday
fdate
fhour = manipulated_time.strftime('%H')
fminute = manipulated_time.strftime('%M')
fsecond = manipulated_time.strftime('%S')
ftime = fhour + fminute + fsecond
ftime
fdatetime = fdate + ftime
fdatetime

manipulated_time.year
manipulated_time.month
manipulated_time.day
manipulated_time.date
manipulated_time.time

# 2자리로 만드는 빠른 방법은? .apply(lambda x : str(x).zfill(2))  
manipulated_time
manipulated_time.hour
manipulated_time.minute
manipulated_time.second

# 확인완료 - read_csv에서 time parsing : parse_dates, date_parser
# Format : https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
# [ 제거가 필요하다.
dateparser = lambda x: pd.datetime.strptime(x, '%d/%b/%Y:%H:%M:%S')

# Which makes your read command:
pd.read_csv(logfile, encoding="utf-8", error_bad_lines=False, header=None, delimiter=" ", parse_dates=[3], date_parser=dateparser)

# Or combine two columns into a single DateTime column
pd.read_csv(logfile, parse_dates={'datetime': ['date', 'time']}, date_parser=dateparser)

###########################################################################################################
# (완료) 전처리 기능 : [] 등으로  둘러싸인 부분을 제거하는 것
#               [걸린시간] -> 걸린시간
#               [%T/%D] -> -%T %D -> %D
# 언제 처리할 것인가? 입력값 원래 Format, 변경 Format, 원래 Log파일, 변경 Log파일
# [0.001] -> 0.001
# \[([0-9.]+)\] -> \1 (정규식 그룹)
# Dataframe으로 처리

# TEST CASE : [0.001] -> 0.001  ms precision : OK
logfile = "F:\\loganalyzerMedia\\logsample\\3_Tomcat_Access\\SSVC_access_log.2021-05-04.log"
df_logs = pd.read_csv(logfile, encoding="utf-8", error_bad_lines=False, header=None, delimiter="\0", na_filter=False)
df_logs[0][4]

targetRE = '\[([0-9.]+)\]'
targetRE = ' '+targetRE
grpN = 1
repl = lambda m: ' '+m.group(grpN)
df_logs_re = df_logs[0].str.replace(targetRE, repl)
df_logs_re[4]

# TEST CASE : %T/%D : 0/223 -> %D : 223
logfile = "F:\\loganalyzerMedia\\logsample\\3_Tomcat_Access\\EDM_access.log.2021031516"
df_logs = pd.read_csv(logfile, encoding="utf-8", error_bad_lines=False, header=None, delimiter="\0", na_filter=False)
df_logs[0][0] 

# Isuue : Request 부분의 숫자/숫자 가 같이 치환됨
# 앞에 공백이 하나씩 필요
targetRE = '([0-9]+)/([0-9]+)'
targetRE = ' '+targetRE
grpN = 2
repl = lambda m: ' '+m.group(grpN)
df_logs_re = df_logs[0].str.replace(targetRE, repl)
df_logs_re[0]

np.savetxt(logfile+"_preprocessed", df_logs_re.values, fmt="%s")

# Test : millisecond 제거
logfile = "C:\\Users\\Leehs\\Desktop\\6_LogViewer_Lhs\\20210510_WAS로그적용\\one-policy.0.log"
df_logs = pd.read_csv(logfile, encoding="utf-8", error_bad_lines=False, header=None, delimiter="\0", na_filter=False)
df_logs

targetRE = '.([0-9]{3})'
targetRE = targetRE+' '
grpN = 1
#repl = lambda m: ' '+m.group(grpN)
repl = ' '
df_logs_re = df_logs[0].str.replace(targetRE, repl)
df_logs_re[0]

np.savetxt(logfile+"_preprocessed", df_logs_re.values, fmt="%s", encoding='utf-8')

###########################################################################################################
# Time-Taken 유추기능 : 서버에서 구현하기 
# 

# 기존 로직
logfile = "F:\\loganalyzerMedia\\logsample\\1_Apache\\3_ACS 시스템_Custom\\access-itct-20200701.log"
df_logs = pd.read_csv(logfile, encoding="utf-8", error_bad_lines=False, header=None, delimiter=" ", na_filter=False)
df_logs

df_datetime = df_logs[3].str.replace(pat='[\:\/\[]', repl= r' ', regex=True)
df_datetime
series = df_datetime.str.split(' ')
df_time = pd.DataFrame(series.tolist(), columns=['dummy','fday','fmonth','fyear','fhour','fminute','fsecond'])

df_time.dropna(axis=0, inplace=True)

month_map = {
    'Jan' : '01', 'Feb' : '02', 'Mar' : '03', 'Apr' : '04', 'May' : '05', 'Jun' : '06',
    'Jul' : '07', 'Aug' : '08', 'Sep' : '09', 'Oct' : '10', 'Nov' : '11', 'Dec' : '12',
}

df_time['fmonth'] = df_time['fmonth'].apply(lambda x : month_map[x]) 

df_time['fdate'] = df_time['fyear'] + df_time['fmonth'] + df_time['fday']
df_time['fdate']
df_time['ftime'] = df_time['fhour'] + df_time['fminute'] + df_time['fsecond']
df_time['ftime']
df_time['fdatetime'] = df_time['fdate']+df_time['ftime']
df_time['fdatetime']    # yyyymmddhhss 20200702000027

# Step1 : temp_end_time 컬럼 생성 => start_time(로깅시간)에서 shift(1) 값
#         https://stackoverflow.com/questions/27474921/compare-two-columns-using-pandas

# 시간 연산을 위해 변환
df_logs['start_time'] = pd.to_datetime(df_time['fdatetime'], format='%Y%m%d%H%M%S')
df_logs['start_time']

df_logs['temp_end_time'] = df_logs['start_time'].shift(1)
df_logs['temp_end_time']

# 앞에 밀린거 1칸 채우기(뒤의 갚으로) : NaN 제거
df_logs['temp_end_time'].fillna(method='bfill', inplace=True)
df_logs['temp_end_time']
df_logs

# Step2 : end_time 컬럼 생성 => MAX(start_time, temp_end_time) 값 : 코드 확인(가능)
df_logs['end_time'] = np.where((df_logs['start_time'] >= df_logs['temp_end_time']) , df_logs['start_time'], df_logs['temp_end_time'])
df_logs['end_time']

# Step3 : tiem-taken(기존 컬럼) 값(초단위만 가능) 계산 => end_time(Step2 계산 값) - start_time(로깅시간)
# 추정 time-taken : Second 까지만 환산 가능
#df_logs['time_taken'] = -1
df_logs['time_taken'] = (df_logs['end_time'] - df_logs['start_time']).dt.total_seconds().astype(int)
df_logs['time_taken']

###########################################################################################################
# (완료): Log4j/App Log : 시간 Adjust 기능 : 시간 +, - 
# Access Log보다 어렵다. 
from datetime import datetime, timedelta
import time

# CASE1 : 시간만 있는 경우 - 완료 : 기존 로직과 비교
logfile = "C:\\Users\\Leehs\\Desktop\\6_LogViewer_Lhs\\20210510_WAS로그적용\\one-policy.0.log_preprocessed_issue_sample"
df_logs = pd.read_csv(logfile, encoding="utf-8", error_bad_lines=False, header=None, delimiter="\0", na_filter=False)
df_logs

p = re.compile('[0-9]{2}:[0-9]{2}:[0-9]{2}', re.DOTALL )
df_logs_time  = df_logs[0].apply(lambda x: p.findall(x)[0] if len(p.findall(x)) > 0 else np.NaN)
df_logs_time

df_logs_time.fillna(method='ffill', inplace=True)
df_logs_time

# 연월일이 어차피 있어야 한다. 없어도 1900-01-01 기준으로 생성한다.
default_date = datetime.today().strftime('%Y:%m:%d')
default_date

df_logs_time = default_date + ':' + df_logs_time
df_logs_time

processed_time = pd.to_datetime(df_logs_time, format='%Y:%m:%d:%H:%M:%S')
processed_time

# 시간연산
time_diff = -9
manipulated_time = pd.DatetimeIndex(processed_time) + timedelta(hours=time_diff)
manipulated_time

df_datetime = pd.DataFrame(manipulated_time, dtype="str")
df_datetime

p = re.compile('([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2})', re.DOTALL )
df_logs_time  = df_datetime[0].apply(lambda x: p.findall(x)[0] if len(p.findall(x)) > 0 else np.NaN)
df_logs_time

df_logs_time = pd.DataFrame(df_logs_time.tolist(), columns=['fyear','fmonth','fday','fhour','fminute','fsecond'])
df_logs_time
# CASE1 : 완료

# CASE2 : 연월일 시간 있는 경우
logfile = "C:\\Users\\Leehs\\Desktop\\6_LogViewer_Lhs\\20210510_WAS로그적용\\one-policy.0.log_preprocessed_issue_sample.date_added"
df_logs = pd.read_csv(logfile, encoding="utf-8", error_bad_lines=False, header=None, delimiter="\0", na_filter=False)
df_logs

p = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', re.DOTALL )
df_logs[0]
df_logs_time  = df_logs[0].apply(lambda x: p.findall(x)[0] if len(p.findall(x)) > 0 else np.NaN)
df_logs_time

df_logs_time.fillna(method='ffill', inplace=True)
df_logs_time

# 공통 : 시간연산
processed_time = pd.to_datetime(df_logs_time, format='%Y-%m-%d %H:%M:%S')
processed_time

# 시간연산
time_diff = -9
manipulated_time = pd.DatetimeIndex(processed_time) + timedelta(hours=time_diff)
manipulated_time

df_datetime = pd.DataFrame(manipulated_time, dtype="str")
df_datetime

p = re.compile('([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2})', re.DOTALL )
df_logs_time  = df_datetime[0].apply(lambda x: p.findall(x)[0] if len(p.findall(x)) > 0 else np.NaN)
df_logs_time

df_logs_time = pd.DataFrame(df_logs_time.tolist(), columns=['fyear','fmonth','fday','fhour','fminute','fsecond'])
df_logs_time
# CASE2 : 완료

###########################################################################################################
# Log4j/App Log : 서버에서 구현하기 
# 
# Database Schema 확인필요
# _preprocessed 로 millisecond를 제거한다.
logfile = "C:\\Users\\Leehs\\Desktop\\6_LogViewer_Lhs\\20210510_WAS로그적용\\one-policy.0.log_preprocessed_issue_sample.date_added"
df_logs = pd.read_csv(logfile, encoding="utf-8", error_bad_lines=False, header=None, delimiter="\0", na_filter=False)
df_logs

# Log4j/App Log : 시간추출
# 기존
p = re.compile('([0-9]{2}):([0-9]{2}):([0-9]{2})', re.DOTALL )
df_logs_time  = df_logs[0].apply(lambda x: p.findall(x)[0] if len(p.findall(x)) > 0 else np.NaN)
df_logs_time

df_logs_time.fillna(method='ffill', inplace=True)
df_logs_time

df_logs_time = pd.DataFrame(df_logs_time.tolist(), columns=['fhour','fminute','fsecond'])
df_logs_time

# 'fyear','fday','fmonth'         
# 년월일이 없으면 일단 오늘 날짜로 한다.
default_date = datetime.today().strftime('%Y-%m-%d').split('-')
df_logs_time['fyear'] = default_date[0]
df_logs_time['fmonth'] = default_date[1]
df_logs_time['fday'] = default_date[2]

df_logs_time

# Test - time_format_2
# %d -> %d{DEFAULT} : 예) 2012-11-02 14:34:02,123
# %d{yyyy-MM-dd HH:mm:ss}
# %d{yyyy-MM-dd HH:mm:ss.SSS} 도 가능한가?
# 패턴으로 접근한다. : ([1-9]{4}):([0-9]{2}):([0-9]{2})\s+([0-9]{2}):([0-9]{2}):([0-9]{2})
# TODO: 입력으로 처리할 수 있는가? Management 기능으로?

# Sample 데이터 생성필요 - date_added
logfile = "C:\\Users\\Leehs\\Desktop\\6_LogViewer_Lhs\\20210510_WAS로그적용\\one-policy.0.log_preprocessed_issue_sample.date_added"
df_logs = pd.read_csv(logfile, encoding="utf-8", error_bad_lines=False, header=None, delimiter="\0", na_filter=False)
df_logs

p = re.compile('([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2})', re.DOTALL )
df_logs[0]
df_logs_time  = df_logs[0].apply(lambda x: p.findall(x)[0] if len(p.findall(x)) > 0 else np.NaN)
df_logs_time

df_logs_time.fillna(method='ffill', inplace=True)
df_logs_time

df_logs_time = pd.DataFrame(df_logs_time.tolist(), columns=['fyear','fmonth','fday','fhour','fminute','fsecond'])
df_logs_time

df_logs_time['fyear'] = '2021'
df_logs_time['fmonth'] = '06'
df_logs_time['fday'] = '02'
df_logs_time

df_logs_time.isna() # None Check 가능

# 결측값 처리 : TODO: Process time 추정로직 추가와 연관
# 결측값을 앞 방향 혹은 뒷 방향으로 채우기 (fill gaps forward or backward)
# fillna(method='ffill' or 'pad'), fillna(method='bfill' or 'backfill')
df_logs_time.fillna(method='ffill', inplace=True)
df_logs_time

df_logs_time['fsecond_lag'] = df_logs_time['fsecond'].shift(1)
df_logs_time

df_logs_time['max_value'] = np.where((df_logs_time['fsecond'] >= df_logs_time['fsecond_lag'])
                     , df_logs_time['fsecond'], df_logs_time['fsecond_lag']) #np.nan)
df_logs_time[0:200]

'''
def my_max(x, y):
    return max(x,y)

str_exp = "@my_max(fsecond, fsecond_lag)"
df_logs_time['max_value'] = df_logs_time.query(str_exp)
df_logs_time
'''

df_logs = pd.concat([df_logs_time, df_logs], axis=1)
df_logs

# shift로 처리불가
df_logs_time['fmillis_lag'] = df_logs_time['fmillis'].shift(1)
df_logs_time

df_logs[df_logs_time['fhour']!='-']

# 시간 비어있는 부분에 대해서는 후처리가 필요하다.? -> 아니어도 된다.
# Lookup에서는 rowid(순서)대로 나타낸다. where 부분은 시간으로 검색 후 rowid를 찾아서 between 처리
df_logs[df_logs_time['fhour']=='-']

###########################################################################################################
# URL 패턴 추출하기 : 화면에서 구현하기 -> Javascript로 구현필요 - 2021.05.24 구현적용
# GET /qhub/search/getSearchResultWordAjax.do HTTP/1.1
# GET /restservice/mx_host/host_name/sedw6011/ip/70.2.180.150/ HTTP/1.1
# GET /api/file/agent/v1/patch/files/windows/6.0.3.1/_install.json HTTP/1.1
# GET /restservice/messageReceive?smsUrl=93MIYQ2H0JO75E660MA3 HTTP/1.1
# GET /common/js/overpass/searchDiver/overpass.searchDiver.search.js?ver=20200527000002 HTTP/1.1
# GET /common/js/overpass/searchDiver/overpass.searchDiver.search.js?ver=20200527000002 HTTP/1.1
# GET /personal/card/limit/UHPPMM0801M0.jsp?appvi=30049808302&useAppTitle=Y&click=1app_my_main_limit HTTP/1.1"
urlstr = "GET /svc/hpFaqApi/faqServiceList?page=1&pageSize=10&menuId=10511&symptomSeq=&contentType=&keyword=&reKeyword=&sorting=&_siteId=ssvc HTTP/1.0"

urionly = urlstr.split(' ')[1]

p = re.compile('[/?&]', re.DOTALL )
delimiters = p.findall(urionly)
delimiters
delimiter_count = urionly.count('/')+urionly.count('?')+urionly.count('&');

resultList = []
startIdx = 0
endIdx = 0
for pos in range(delimiter_count):
    
    kind = delimiters[pos]
    print(kind)
    
    endIdx = urionly.index(kind, startIdx + endIdx)
    
    print(0, endIdx)
    print(urionly[startIdx:endIdx])
    
    endIdx = endIdx+1
    
    if pos > 0:
        resultList.append(urionly[startIdx:endIdx-1])

resultList.append(urionly)

resultList
#########################################################################################################
import 

line = u'01:06:08 [TraceId=ac8b03947f56a033,SpanId=9993d62bc2a1b73b,ParentSpanId=ac8b03947f56a033,SpanExport=false] WARN  --- [http-nio-0.0.0.0-16018-exec-2681] c.s.o.c.e.OneExceptionHandler : handleOneException 네트워크 서비스 에러 -  '
line

line = line.encode("euckr")
line = line.encode("utf-8")

str(line.encode("utf-8"))[2:-1]

line.decode("euckr")
line.decode("utf-8")

line.encode("euckr").decode("utf-8")

u"NadÃ¨ge".encode("latin-1").decode("utf-8")

#========================================================
# file encode 오류 처리(for 한글)
logfile = "C:\\Users\\Leehs\\Desktop\\6_LogViewer_Lhs\\20210510_WAS로그적용\\one-policy.0.log_preprocessed_issue_sample" #_oneline"

df_logs = pd.read_csv(logfile, encoding="utf-8", error_bad_lines=False, header=None, delimiter="\0", na_filter=False)

df_logs

# 변환 : 한글부분만 --> 유니코드
p = re.compile(u'[\u3130-\u318F\uAC00-\uD7A3]+', re.DOTALL )
df_logs = df_logs[0].apply(lambda x: str(x.encode("utf-8"))[2:-1] if len(p.findall(x)) > 0 else x) 

import csv
df_logs.to_csv(logfile+"_mod", mode='w', header=False, index=False, quoting=csv.QUOTE_NONE, escapechar=' ')


# Decoding
log_line = '2021-05-31 04:22:04 182.193.0.150 POST /api/v1/smartoffice/checkcap - 6443 {"Profile":{"Account":"ken.lee","Name":"\xec\x9d\xb4\xea\xb7\xbc\xec\x97\xb4","NameEn":"KeunYeol+Lee","CelPhone":"+82-10-3377-9782","CompanyName":"\xec\x82\xbc\xec\x84\xb1SDS","CompanyNameEn":"SAMSUNG+SDS","CompanyCode":"C60","CompanyUuid":"6B75533D-4D8E-4215-B246-7CE667E3B030","DepartmentName":"\xea\xb8\xb0\xec\x88\xa0\xec\xa7\x80\xec\x9b\x90\xea\xb7\xb8\xeb\xa3\xb9(S-ERP)" 182.193.0.16 Mozilla/5.0+(compatible;+MSIE+10.0;+Windows+NT+6.2;+Trident/6.0) https://smartoffice.samsung.net/ko-kr/Home/Index 200 0 0 218 168.126.147.60'

# 문제현상
print(log_line)
print('\xec\x9d\xb4\xea\xb7\xbc\xec\x97\xb4')

'제일기획'.encode('utf-8')

## 정상 값
test_log = '2021-05-31 04:22:04 182.193.0.150 POST /api/v1/vdi/getlaunchstatus - 6443 {"Profile":{"Account":"ken.lee","Name":"이근열","NameEn":"KeunYeol+Lee","CelPhone":"+82-10-3377-9782","CompanyName":"삼성SDS","CompanyNameEn":"SAMSUNG+SDS","CompanyCode":"C60","CompanyUuid":"6B75533D-4D8E-4215-B246-7CE667E3B030","DepartmentName":"기술지원그룹(S-ERP)" 182.193.0.16 Mozilla/5.0+(compatible;+MSIE+10.0;+Windows+NT+6.2;+Trident/6.0) https://smartoffice.samsung.net/ko-kr/Home/Index 200 0 0 749 168.126.147.60'

#test_log.encode('utf-8').decode("utf-8")

test_log_utf8 = test_log.encode('utf-8')
test_log_utf8

type(test_log_utf8)
type(str(test_log_utf8))

str(test_log_utf8).encode('utf-8')

## 테스트 값
# b'2021-05-31 04:22:04 182.193.0.150 POST /api/v1/vdi/getlaunchstatus - 6443 {"Profile":{"Account":"ken.lee","Name":"\xec\x9d\xb4\xea\xb7\xbc\xec\x97\xb4","NameEn":"KeunYeol+Lee","CelPhone":"+82-10-3377-9782","CompanyName":"\xec\x82\xbc\xec\x84\xb1SDS","CompanyNameEn":"SAMSUNG+SDS","CompanyCode":"C60","CompanyUuid":"6B75533D-4D8E-4215-B246-7CE667E3B030","DepartmentName":"\xea\xb8\xb0\xec\x88\xa0\xec\xa7\x80\xec\x9b\x90\xea\xb7\xb8\xeb\xa3\xb9(S-ERP)" 182.193.0.16 Mozilla/5.0+(compatible;+MSIE+10.0;+Windows+NT+6.2;+Trident/6.0) https://smartoffice.samsung.net/ko-kr/Home/Index 200 0 0 749 168.126.147.60'

## 작성된 값
test_log = u'2021-05-31 04:22:04 182.193.0.150 POST /api/v1/vdi/getlaunchstatus - 6443 {"Profile":{"Account":"ken.lee","Name":"\xec\x9d\xb4\xea\xb7\xbc\xec\x97\xb4","NameEn":"KeunYeol+Lee","CelPhone":"+82-10-3377-9782","CompanyName":"\xec\x82\xbc\xec\x84\xb1SDS","CompanyNameEn":"SAMSUNG+SDS","CompanyCode":"C60","CompanyUuid":"6B75533D-4D8E-4215-B246-7CE667E3B030","DepartmentName":"\xea\xb8\xb0\xec\x88\xa0\xec\xa7\x80\xec\x9b\x90\xea\xb7\xb8\xeb\xa3\xb9(S-ERP)" 182.193.0.16 Mozilla/5.0+(compatible;+MSIE+10.0;+Windows+NT+6.2;+Trident/6.0) https://smartoffice.samsung.net/ko-kr/Home/Index 200 0 0 749 168.126.147.60'

type(test_log)

print(test_log)

bytes(test_log, 'utf-8').decode("utf-8")
bytes(test_log, 'utf-8').decode("cp1252")


#########################################################################
# 압축 필요시...
# compression test
compression_opt = {'method' : 'zip', 'archive_name' :'one-policy.0.log_preprocessed_issue_sample_mod.csv'}
#compression_opt = dict(method = 'zip', archive_name = logfile+"_mod")

# 파일 이름만 필요
df_logs.to_csv(logfile+"_mod.zip", mode='w', compression=compression_opt, header=False, index=False, quoting=csv.QUOTE_NONE, escapechar=' ')


# 기존로직에 영향?
#df_logs = pd.read_csv(logfile, encoding="utf-8", error_bad_lines=False, header=None, delimiter="\s+", #na_filter=False, escapechar="\\", quotechar='"')
#########################################################################

# CASE1 : encoding 오류 수정
# %h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" \"%{Cookie}i\"
#logfile = "F:\\loganalyzerMedia\\logsample\\1_Apache\\3_ACS 시스템_Custom\\access-itct-20200702.log"
#df_logs = pd.read_csv(logfile, encoding="cp1252", error_bad_lines=False, header=None, delimiter=" ", escapechar="\\", na_filter=False, quotechar='"')

#df_logs[1] = 0
# #df_logs[1] = df_logs[1] + 100

# CASE2 : %{X-Forwarded-For}i 
#logfile = "F:\\loganalyzerMedia\\logsample\\1_Apache\\6_jira_confluence\\web2_access_log-20190928\\split\\access_log-20190928_000001"
logfile = "F:\\loganalyzerMedia\\logsample\\1_Apache\\4_삼성카드 홈페이지_Custom\\HOM1-W-F11_XForwardedFor_Error.log"
# Delimiter 추가 : " " 공백 + ", " 추가필요

# Step1 : 전체 받기, 전체 읽기가 선행되어야 함
#df_logs = pd.read_csv(logfile, encoding="utf-8", error_bad_lines=False, header=None, delimiter="\t", escapechar="\\", na_filter=False, quotechar='"')
df_logs = pd.read_csv(logfile, encoding="utf-8", error_bad_lines=False, header=None, delimiter="\t", na_filter=False, quotechar='"')
df_logs
list(df_logs.columns)
# Step2 : 패턴 변경하기 IP, IP --> IP,IP
# (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\,\ 
# Virtual Host의 경우 %v, 이런 경우 - 그 외의 경우는 드물다.
#df_logs = df_logs[0].str.replace(pat=', ', repl= r',', regex=True)
repl = lambda m: m.group(0)[:-1:]
df_logs_re = df_logs[0].str.replace(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(\, )+', repl)
df_logs_re
# Step3 : 기존 파일처럼 만들기
# csv 파일 만들면 안됨
#df_logs_re.to_csv(logfile+'_temp.log', index=False, header=None, sep=" ")
np.savetxt(logfile+'_temp_np.log', df_logs_re.values, fmt="%s", encoding="utf-8")

# Step4 : 다시 읽어들이기(기존 로직 활용)
df_logs_re_result = pd.read_csv(logfile+'_temp_np.log', encoding="utf-8", error_bad_lines=False, header=None, delimiter=" ", escapechar="\\", na_filter=False, quotechar='"')
df_logs_re_result

#  %{X-Forwarded-For}i의 맨 앞은 사용자 IP
# %{X-Forwarded-For}i의 index 중요 - File Format에서 가져올 것
# 기존 get_logformat_index 함수에 추가 - X-Forwarded-For

# 로그포맷 : %{X-Forwarded-For}i %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"
index = 0
df_logs_re_result[index].str.split(',').str[0]

num = 13.456
num

round(num,1)

test = "GET /anysign/AnySign4PC/img/icon_hdd_disabled.png HTTP/1.1"
fname = test.split(' ')
fname[1]

#test.split(' ')[1]

#########################################################################
# IIS cs-username 에 AD-JOIN 정보 존재하는 경우
# compression test
#logfile = "C:\\Users\\Leehs\\Desktop\\6_LogViewer_Lhs\\20210607_IIS_로그_VDI관련\\Error_Sample_DMZUser01_u_ex210529_x.log_only"

df_logs = pd.read_csv(logfile, encoding="utf-8", error_bad_lines=False, header=None, comment='#', delimiter="\s+", escapechar="\\", skiprows=None, nrows=None, na_filter=False, quotechar='"')

df_logs

df_logs[7]
df_logs[8]


import re

# TODO: 날짜가 들어간 부분을 어떻게 처리할 것인가? 숫자 나타나기 전 까지를 파일명으로 보고 매칭한다.(뱔도 로직)
logfile_name = "access_log"
confile_path = "F:\\loganalyzerMedia\\logsample\\1_Apache\\0_fileformat_recognition\\httpd.conf"

# 주석패턴 : #
pcom = re.compile(r'\s*[#].+', re.DOTALL)

# 로그패턴
plog = re.compile(r'.*LOG.*', re.IGNORECASE | re.MULTILINE )

line_cnt = 0
result = []

# 파일 읽기 - Edit으로?
with open(confile_path, "r") as f:
    lines = f.readlines()
    for line in lines:
                
        if len(pcom.findall(line)) == 0:            
            if len(plog.findall(line)) != 0:
                line_cnt = line_cnt + 1
                result.append(line.lstrip(' ').rstrip('\n'))
                #print("result:"+line)
       
print(line_cnt)
print(result)

# 파일명 패턴 찾기
logformat = ""
for temp in result:
    if temp.find(logfile_name) != -1: 
        print(temp)
        logformat = temp.split()[2]        
        break;

# common, combinedio ...        
print(logformat)

logpattern = ""
for temp in result:
    if temp.find('LogFormat') != -1 and temp.find(logformat) != -1: 
        print(temp)
        logpattern = temp.replace('LogFormat','').replace(logformat,'').strip(' ').strip('"')
        break;

# 결과
print(logpattern)   
print('==========')

# 주석빼고, LOG 들어간 패턴
#pall = re.compile(r'(?!(\s*)#).*LOG.*', re.IGNORECASE)

#with open(confile_path, "r") as f:
#    lines = f.readlines()
#    for line in lines:
#        if pall.search(line) is None:
#            print(pall.search(line).group())
        #if len(pall.search(line)) != 0:
        #    print(line)

########################################################################
# Nginx의 경우 
# 주석패턴 : #
pcom = re.compile(r'\s*[#].+')

# 로그패턴
# re.compile(r'\s*log_format.*;$', re.IGNORECASE | re.MULTILINE )

# TODO: Multiline일 경우에 첫음과 끝 문자로 패턴매칭 하기
#plog = re.compile(r".*log_format.*\s*.*\s*.*;", re.MULTILINE) 
plog = re.compile(r".*log_format[$a-zA-Z_ '-\[\]\"\t\r\n]*", re.MULTILINE) 

logfile_name = "access_log"
confile_path = "F:\\loganalyzerMedia\\logsample\\4_Nginx\\0_fileformat_recognition\\nginx.conf"

results = ""
line_cnt = 0

log_format = {}
lp = re.compile(r"(log_format)\s+([A-Za-z0-9]*)\s+([$].+)")

# 파일 읽기 -> Sweetalert textarea
with open(confile_path, "r") as f:
    lines = f.read()
    
    print("=== lines : ", lines)
       
    results = plog.findall(lines)
    result = results[0].split(';')
    print(result)
    print("LEN: ", len(result))
    
    for tmp in result:
        if tmp.find('log_format') != -1:
            
            tmp_line = tmp.replace('\'','').lstrip().rstrip().replace('\n','')            
            tmp_line = ' '.join(tmp_line.split())
            
            format_name = lp.search(tmp_line).group(2)
            format = lp.search(tmp_line).group(3)
            
            print('# All :', tmp_line)
            print('# format_name :', format_name)
            print('# format :', format)
            
            
            log_format[format_name] = format
            
print("== Result")
print(log_format['main'])
print(log_format['test'])

# dictionary key:value
print(log_format)

# Possible Format
for key, value in log_format.items():
    print(key, ":", value)
    
# Another Method    
for key in log_format:
    print(key, ":", log_format[key])            
            
    
    #results = plog.finditer(lines)
    
    #print(results)
    #print("LEN: ", len(results))
    #for r in results: print("cnt:",line_cnt, "- ", r.group())
 
#print(results[0].split(';'))
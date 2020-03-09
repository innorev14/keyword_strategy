import os
import sys
import urllib.request

from config import settings

client_id = settings.CLIENT_ID
client_secret = settings.CLIENT_SECRET
encText = urllib.parse.quote("사과")
'''
블로그 요청변수
query(str) : (필수)검색을 원하는 문자열로서 UTF-8로 인코딩한다
display(int) : 검색 결과 출력 건수 지정 / 10(기본값), 100(최대값)
start(int) : 검색 시작 위치로 최대 1000개 까지 까능 / 1(기본값), 1000(최대값)
sort(str) : 정렬옵션 : sim(유사도순/기본), date(날짜순)
'''
# 블로그
# url = "https://openapi.naver.com/v1/search/blog?query=" + encText # json 결과
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과

'''
카페 요청변수
query(str) : (필수)검색을 원하는 문자열로서 UTF-8로 인코딩한다
display(int) : 검색 결과 출력 건수 지정 / 10(기본값), 100(최대값)
start(int) : 검색 시작 위치로 최대 1000개 까지 까능 / 1(기본값), 1000(최대값)
sort(str) : 정렬옵션 : sim(유사도순/기본), date(날짜순)
'''
# 카페
# url = "https://openapi.naver.com/v1/search/cafearticle?query=" + encText # json 결과

'''
지식iN 요청변수
query(str) : (필수)검색을 원하는 문자열로서 UTF-8로 인코딩한다
display(int) : 검색 결과 출력 건수 지정 / 10(기본값), 100(최대값)
start(int) : 검색 시작 위치로 최대 1000개 까지 까능 / 1(기본값), 1000(최대값)
sort(str) : 정렬옵션 : sim(유사도순/기본), date(날짜순), asc(가격오른차순), dsc(가격내림차순)
'''
# 지식iN
# url = "https://openapi.naver.com/v1/search/kin?query=" + encText # json 결과

'''
지역 요청변수
query(str) : (필수)검색을 원하는 문자열로서 UTF-8로 인코딩한다
display(int) : 검색 결과 출력 건수 지정 / 10(기본값), 30(최대값)
start(int) : 검색 시작 위치로 최대 1000개 까지 까능 / 1(기본값), 1000(최대값)
sort(str) : 정렬옵션 : random(유사도순/기본), comment(카페/블로그 리뷰 개수 순)
'''
# 지역
# url = "https://openapi.naver.com/v1/search/local?query=" + encText # json 결과

'''
웹문서 요청변수
query(str) : (필수)검색을 원하는 문자열로서 UTF-8로 인코딩한다
display(int) : 검색 결과 출력 건수 지정 / 10(기본값), 100(최대값)
start(int) : 검색 시작 위치로 최대 1000개 까지 까능 / 1(기본값), 1000(최대값)
'''
# 웹문서
url = "https://openapi.naver.com/v1/search/webkr?query=" + encText # json 결과

'''
쇼핑 요청변수
query(str) : (필수)검색을 원하는 문자열로서 UTF-8로 인코딩한다
display(int) : 검색 결과 출력 건수 지정 / 10(기본값), 100(최대값)
start(int) : 검색 시작 위치로 최대 1000개 까지 까능 / 1(기본값), 1000(최대값)
sort(str) : 정렬옵션 : sim(유사도순/기본), date(날짜순), asc(가격오른차순), dsc(가격내림차순)
'''
# 쇼핑
url = "https://openapi.naver.com/v1/search/shop?query=" + encText # json 결과

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)
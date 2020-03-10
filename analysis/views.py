import json
import urllib
from datetime import date
from pprint import pprint

from django.shortcuts import render
from django.views.generic import ListView

from config import settings
from naver_ads_api import SearchAdsSession
from naver_keyword_strategy import KeywordInfoAPI
from naver_trend_api import NaverTrendAPI
from .models import MonthAnalysis


class IndexView(ListView):
    template_name = 'analysis/insdex.html'

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        qq = "{}".format(q)
        encText = urllib.parse.quote("{}".format(q))

        rel_data = KeywordInfoAPI().rel_keyword_list(qq)
        pprint(rel_data)
        time_series_data = NaverTrendAPI().trend_graph(qq)
        pprint(time_series_data)

        # sorted_view = sorted(rel_data['relCurView'], reverse=True)

        if 'relGenderCount' in rel_data:
            ## 성별 비율 계산
            sum_female = sum(rel_data['relGenderCount']['f'].values())
            sum_male = sum(rel_data['relGenderCount']['m'].values())
            total_gender = sum_male + sum_female
            female_ratio = round(sum_female/total_gender*100)
            male_ratio = round(sum_male/total_gender*100)

            ## 연령별
            sum_fage = sum(rel_data['relGenderCount']['f'].values())
            fage = list()
            fage.append(round(rel_data['relGenderCount']['f']['0-12']/sum_fage*100))
            fage.append(round(rel_data['relGenderCount']['f']['13-19']/sum_fage*100))
            fage.append(round(rel_data['relGenderCount']['f']['20-24']/sum_fage*100))
            fage.append(round(rel_data['relGenderCount']['f']['25-29']/sum_fage*100))
            fage.append(round(rel_data['relGenderCount']['f']['30-39']/sum_fage*100))
            fage.append(round(rel_data['relGenderCount']['f']['40-49']/sum_fage*100))
            fage.append(round(rel_data['relGenderCount']['f']['50-']/sum_fage*100))

            sum_mage = sum(rel_data['relGenderCount']['m'].values())
            mage = list()
            mage.append(round(rel_data['relGenderCount']['m']['0-12']/sum_mage*100))
            mage.append(round(rel_data['relGenderCount']['m']['13-19']/sum_mage*100))
            mage.append(round(rel_data['relGenderCount']['m']['20-24']/sum_mage*100))
            mage.append(round(rel_data['relGenderCount']['m']['25-29']/sum_mage*100))
            mage.append(round(rel_data['relGenderCount']['m']['30-39']/sum_mage*100))
            mage.append(round(rel_data['relGenderCount']['m']['40-49']/sum_mage*100))
            mage.append(round(rel_data['relGenderCount']['m']['50-']/sum_mage*100))

            graph_label = time_series_data['period']
            graph_data = time_series_data['ratio']

            context = {
                'q': q,
                'reldata': rel_data,
                'f_ratio': female_ratio,
                'm_ratio': male_ratio,
                'f_age': fage,
                'm_age': mage,
                'labels': graph_label,
                'data': graph_data,
                # 'results': data,
            }
        else:
            context = {
                'reldata': rel_data,
            }

        return render(request, 'analysis/index.html', context=context)


class Trend(ListView):
    template_name = 'analysis/trend.html'

    def get(self, request, *args, **kwargs):
        client_id = settings.CLIENT_ID
        client_secret = settings.CLIENT_SECRET

        q = request.GET.get('q')
        qq = "{}".format(q)
        encText = urllib.parse.quote("{}".format(q))
        url = "https://openapi.naver.com/v1/datalab/search"

        startdate = "2016-01-01"
        today = date.today()
        enddate = today.strftime("%Y-%m-%d")
        # keyword = "사과"

        body_dict = {
            "startDate": startdate,
            "endDate": enddate,
            "timeUnit": "month",
            "keywordGroups": [{
                "groupName": qq,
                "keywords": [qq]
            }],
        #    "device": "",
        #    "ages": [""],
        #    "gender": "",
        }
        body = json.dumps(body_dict)
        trend_request = urllib.request.Request(url)
        trend_request.add_header("X-Naver-Client-Id",client_id)
        trend_request.add_header("X-Naver-Client-Secret",client_secret)
        trend_request.add_header("Content-Type","application/json")
        response = urllib.request.urlopen(trend_request, data=body.encode("utf-8"))

        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            result = json.loads(response_body.decode('utf-8'))
            items = result.get('results')[0]
            data_set = result.get('results')[0]
            data = data_set.get('data')
            # pprint(result)  # request를 예쁘게 출력해볼 수 있다.
            # pprint(items)
            a = KeywordInfoAPI()
            total_pc = a.rel_keyword_list(qq)
            context = {
                'items': items,
                'total_pc': total_pc,
                # 'results': data,
            }

            # {'endDate': '2020-03-04',
            #  'results': [{'data': [{'period': '2016-01-01', 'ratio': 80.98636}],
            #               'keywords': ['사과'],
            #               'title': '사과'}],
            #  'startDate': '2016-01-01',
            #  'timeUnit': 'month'}

            return render(request, 'analysis/trend.html', context=context)
        else:
            pprint("Error Code:" + rescode)

class Search(ListView):
    template_name = 'analysis/search.html'

    def get(self, request, *args, **kwargs):
        '''
         네이버 광고시스템 > 키워드 도구
         연관키워드 조회
         usage :
                 api = SearchAdsAPI()
                 get_api = api.get_Info('검색어')
                 print(get_api)
         '''

        # 네이버 검색 광고 API를 이용하기 위한 key와 id
        _BASE_URL = 'https://api.naver.com'
        _API_KEY = settings.ADS_API_KEY
        _SECRET_KEY = settings.ADS_SECRET_KEY
        _CUSTOMER_ID = settings.ADS_CUSTOMER_ID

        def __init__(self):
            pass

        def _signature(self, timestamp, method, uri):
            message = "{}.{}.{}".format(timestamp, method, uri)
            hash = hmac.new(bytes(self._SECRET_KEY, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)
            hash.hexdigest()
            return base64.b64encode(hash.digest())

        def _get_header(self, method, uri, api_key):
            timestamp = str(round(time.time() * 1000))
            signature = self._signature(timestamp, method, uri)
            return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': api_key,
                    'X-Customer': str(self._CUSTOMER_ID), 'X-Signature': signature}

        def _getRelateByNaverAPI(self, params: dict) -> dict:
            # param params: {'hintkeywords':<your-keyword>,'showDetail':1,'includeHintKeywords':0}
            uri = '/keywordstool'
            method = 'GET'

            r = requests.get(self._BASE_URL + uri, params=params, headers=self._get_header(method, uri, self._API_KEY))
            json_data = r.json()

            return json_data

        def get_Info(self, word):
            params = {'hintKeywords': [word.replace(' ', '')], 'showDetail': 1}

            status_code = ''
            keywords = []

            try:
                status_code = self._getRelateByNaverAPI(params)
                if status_code is None or status_code['status'] == 'BAD_REQUEST':
                    return []
            except Exception as e:
                pass

            try:
                keywords = status_code['keywordList']
            except Exception as e:
                return []

            ret = []
            head = ['name', 'pc', 'mobile', 'pc_ads_click', 'mobile_ads_click']
            for keyword in keywords:
                tmp = dict()
                for idx, key in enumerate(keyword.keys()):
                    if idx > 4:
                        break
                    tmp[head[idx]] = keyword[key]
                ret.append(tmp)
            return ret

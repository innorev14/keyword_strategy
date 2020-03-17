import json, requests, time
import base64, hashlib, hmac, csv
from datetime import datetime

from config import settings


def curDate():
    now = datetime.today()
    return now.year, now.month, now.day


def Error_Log(func, e):
    with open('../../error_log.csv', 'a') as f:
        wr = csv.writer(f)
        try:
            year, month, day = curDate()
            wr.writerow(["{}-{}-{}".format(year, month, day) + ' ' + func + ' ' + e])
        except Exception as e:
            pass


class SearchAdsAPI:
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


class SearchAdsSession:
    '''
    네이버 광고시스템 > 키워드 상세
    월별 검색수 추이, 월간 검색 수 사용자 통계
    Usage :
            search = SearchAdsSession()
            rel_count = search.getViewCount("검색어")
            monthly_count = search.getGraphData("검색어")
            print(rel_count)
            print(monthly_count)
    '''

    def __init__(self):
        self.count = 0
        self.Login()

    def Login(self):
        self.session = requests.Session()

        loginUrl = 'https://searchad.naver.com/auth/login'
        loginHeaders = {
            'Connection': 'keep-alive',
            'Content-Length': '42',
            'Content-Type': 'application/json',
            'DNT': '1',
            'TE': 'Trailers',
        }

        userName = 'eszett'
        password = 'eszett77'

        payload = {"loginId": "{}".format(userName), "loginPwd": "{}".format(password)}

        response = self.session.post(loginUrl, headers=loginHeaders, json=payload)

        if (response.status_code == 200):
            self.isLogin = True
            self.token = json.loads(response.content)['token']
        else:
            self.isLogin = False
            Error_Log('SearchAdsSession Login', 'Login Error')

    def getViewCount(self, keyword):
        if self.isLogin is False:
            Error_Log('SearchAdsSession getViewCount', 'Login Error')
            return

        if self.count > 50:
            self.Login()

        keyword = keyword.encode('utf-8').decode('utf-8').strip()

        relatedKeyWordsUrl = (
            'https://manage.searchad.naver.com/keywordstool?format=json&hintKeywords={}&includeHintKeywords=0&siteId=&biztpId=&month=&event=&showDetail=1&keyword='.format(
                keyword)).encode('utf-8')

        keyHeaders = {
            'authority': 'manage.searchad.naver.com',
            'method': 'GET',
            'path': (
                '/keywordstool?format=json&hintKeywords={}&includeHintKeywords=0&siteId=&biztpId=&month=&event=&showDetail=1&keyword='.format(
                    keyword).encode('utf-8')),
            'scheme': 'https',
            'authorization': 'Bearer {}'.format(self.token),
            'referer': 'https://manage.searchad.naver.com/customers/1515006/tool/keyword-planner?keywords=',
        }

        relHead = ['relKeyword', 'monthlyPcQcCnt', 'monthlyMobileQcCnt', 'monthlyAvePcClkCnt', 'monthlyAveMobileClkCnt',
                   'monthlyAvePcCtr', 'monthlyAveMobileCtr', 'plAvgDepth', 'compIdx']

        items = dict()
        dictHead = ['relkeyword', 'pcClick', 'mobileClick', 'pcAdsClick', 'mobileAdsClick', 'pcPercentage',
                    'mobilePercentage', 'AvgDepth', 'compIdx']

        for head in dictHead:
            items[head] = []

        try:
            response = self.session.get(relatedKeyWordsUrl, headers=keyHeaders)

            keywordList = json.loads(response.content)['keywordList']

            for word in keywordList:
                for idx, head in enumerate(dictHead):
                    items[head].append(word[relHead[idx]])

            time.sleep(1)
            return items
        except Exception as e:
            Error_Log('SearchAdsSession getViewCount', e)

    def getGraphData(self, keyword):
        if self.isLogin is False:
            Error_Log('SearchAdsSession getGraphData', 'Login Error')
            return

        time.sleep(1)

        self.count += 1
        if self.count > 50:
            self.Login()

        graphUrl = (
            'https://manage.searchad.naver.com/keywordstool?format=json&hintKeywords=&includeHintKeywords=0&siteId=&biztpId=&month=&event=&showDetail=1&keyword={}'.format(
                keyword)).encode('utf-8')

        keyHeaders = {
            'authority': 'manage.searchad.naver.com',
            'method': 'GET',
            'path': (
                '/keywordstool?format=json&hintKeywords={}&includeHintKeywords=0&siteId=&biztpId=&month=&event=&showDetail=1&keyword='.format(
                    keyword)).encode('utf-8'),
            'scheme': 'https',
            'authorization': 'Bearer {}'.format(self.token),
            'referer': 'https://manage.searchad.naver.com/customer/1515006/tool/keyword-planner?keywords='
        }

        try:
            response = self.session.get(graphUrl, headers=keyHeaders)
            graphdataList = json.loads(response.content)['keywordList'][0]

            return graphdataList['userStat'], graphdataList['monthlyProgressList']

        except Exception as e:
            Error_Log('SearchAdsSession getGraphData', e)


class AdsParsing:

    def __init__(self):
        self.year, self.month, self.day = curDate()
        self.month -= 1

        if self.month == 0:
            self.year -= 1
            self.month = 12

    def getDate(self):
        return (self.year, self.month)

    def ParsingKeyword(self, word, view):
        if view is None:
            return None

        head = ['monthlyPcQcCnt', 'monthlyMobileQcCnt', 'genderType', 'ageGroup']
        ageList = ['0-12', '13-19', '20-24', '25-29', '30-39', '40-49', '50-']
        gender = ['m', 'f']
        view_count = {'year': self.year, 'month': self.month, 'name': word, gender[0]: dict(), gender[1]: dict()}

        for age in ageList:
            view_count[gender[0]][age] = 0
            view_count[gender[1]][age] = 0

        try:
            for idx, gen in enumerate(view[head[2]]):
                age = view[head[3]][idx]
                view_count[gen][age] += (view[head[0]][idx] + view[head[1]][idx])

        except Exception as e:
            Error_Log('AdsParsing ParsingKeyword', e)

        return view_count


if __name__ == "__main__":
    search = SearchAdsSession()
    a, b = search.getGraphData('피부과')
    print(a)
    print('\n' * 4)
    print(b)

import os
import sys
import urllib.request
import json
from datetime import date

from config import settings


def curDate():
    now = date.today()
    return now.year, now.month, now.day


class NaverTrendAPI:

    def __init__(self):
        self.result = {}

    def trend_graph(self, keyword):
        try:
            _client_id = settings.CLIENT_ID
            _client_secret = settings.CLIENT_SECRET
            _url = "https://openapi.naver.com/v1/datalab/search"

            startdate = "2016-01-01"
            today = date.today()
            enddate = today.strftime("%Y-%m-%d")
            # keyword = "사과"

            body_dict = {
                "startDate": startdate,
                "endDate": enddate,
                "timeUnit": "month",
                "keywordGroups": [{
                    "groupName": keyword,
                    "keywords": [keyword]
                }],
            #    "device": "",
            #    "ages": [""],
            #    "gender": "",
            }
            body = json.dumps(body_dict)
            request = urllib.request.Request(_url)
            request.add_header("X-Naver-Client-Id",_client_id)
            request.add_header("X-Naver-Client-Secret",_client_secret)
            request.add_header("Content-Type","application/json")
            response = urllib.request.urlopen(request, data=body.encode("utf-8"))


            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                result = response_body.decode('utf-8')
                jresult = json.loads(result)
                data = jresult['results'][0]['data']
                time_data = []
                ratio_data = []
                result_dict = {}
                for n in range(len(data)):
                    time_data.append(data[n]['period'])
                    ratio_data.append(data[n]['ratio'])
                result_dict['period'] = time_data
                result_dict['ratio'] = ratio_data

                return result_dict
            elif(rescode==400):
                print("Error Code:" + rescode)
            else:
                print("Error Code:" + rescode)
        except:
            print('error')


if __name__ == "__main__":
    a = NaverTrendAPI()
    a.trend_graph("사과")
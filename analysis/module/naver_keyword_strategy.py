from pprint import pprint

from analysis.module.naver_ads_api import SearchAdsSession, AdsParsing, SearchAdsAPI
#from naver_trend_api import NaverTrendAPI


class KeywordInfoAPI:

    def __init__(self):
        self.cur_item = []
        self.total_pc = 0
        self.total_mobile = 0
        self.cur_pc = 0
        self.cur_mobile = 0
        self.rel_pc = 0
        self.rel_mobile = 0
        self.rel_total = 0
        self.result = {}
        self.rel_data = []

    def rel_keyword_list(self, keyword):
        ads = SearchAdsAPI()
        get_api = ads.get_Info(keyword)
        self.result['keyword'] = keyword
        self.result['relData'] = list()

        for n in range(len(get_api)):

            if keyword == get_api[n]['name']:  # 키위드에 메인 키워드가 들어가는 경우만 리스트에 담는다
                if isinstance(get_api[n]['pc'], int):
                    self.cur_pc += get_api[n]['pc']
                    self.result['curPC'] = self.cur_pc
                else:
                    self.cur_pc += 1
                    self.result['curPC'] = self.cur_pc
                if isinstance(get_api[n]['mobile'], int):
                    self.cur_mobile += get_api[n]['mobile']
                    self.result['curMobile'] = self.cur_mobile
                else:
                    self.cur_mobile += 1
                    self.result['curMobile'] = self.cur_mobile

            if isinstance(get_api[n]['pc'], int):
                self.rel_pc = get_api[n]['pc']
            else:
                self.rel_pc = 1
            if isinstance(get_api[n]['mobile'], int):
                self.rel_mobile = get_api[n]['mobile']
            else:
                self.rel_mobile = 1
            self.rel_total = self.rel_pc + self.rel_mobile


            if isinstance(get_api[n]['pc'], int):
                self.total_pc += get_api[n]['pc']
                self.result['totalPC'] = self.total_pc
            else:
                self.total_pc += 1
                self.result['totalPC'] = self.total_pc
            if isinstance(get_api[n]['mobile'], int):
                self.total_mobile += get_api[n]['mobile']
                self.result['totalMobile'] = self.total_mobile
            else:
                self.total_mobile += 1
                self.result['totalMobile'] = self.total_mobile

            self.cur_item.append(get_api[n]['name'])
            dic = {'relKeyword': get_api[n]['name'], 'relCurView': self.rel_total}
            self.result['relData'].append(dic)

        # print(self.total_pc, self.total_mobile)
        # print(self.cur_pc, self.cur_mobile)

        search = SearchAdsSession()
                # monthly_count = search.getGraphData(keyword)
                # rel_count = search.getViewCount(keyword)
        parsing = AdsParsing()

        # 키워드의 연관 키워드를 하나씩 조회한다.
        try:
            # (성별, 월별 조회수), (Pc, Mobile 조회수) 데이터를 얻어온다.
            statView, monthlyView = search.getGraphData(keyword)
            # print(item, monthlyView)
            # print(" ")
            self.result['relViewCount'] = monthlyView

            # (성별, 월별 조회수)의 길이가 0이라면 사용할 수 있는 데이터가 없다는 뜻
            if len(statView['ageGroup']) is not 0:
                # 데이터를 Parsing 하여 view_count_gender_age 테이블에 넣어준다.
                view_count = parsing.ParsingKeyword(keyword, statView)
                # print(view_count)
                self.result['relGenderCount'] = view_count

        except Exception as e:
            pass
        pprint(self.result)
        return self.result


if __name__ == '__main__':
    a =KeywordInfoAPI()
    print(a.rel_keyword_list("사과"))





'''
        search = SearchAdsSession()
                # monthly_count = search.getGraphData(keyword)
                # rel_count = search.getViewCount(keyword)
        parsing = AdsParsing()

        for idx in tqdm(range(len(self.cur_item[:3]))):
            item = self.cur_item[idx]

            # 키워드의 연관 키워드를 하나씩 조회한다.
            try:
                # (성별, 월별 조회수), (Pc, Mobile 조회수) 데이터를 얻어온다.
                statView, monthlyView = search.getGraphData(item)
                # print(item, monthlyView)
                # print(" ")
                self.result['relViewCount'] = monthlyView

                # (성별, 월별 조회수)의 길이가 0이라면 사용할 수 있는 데이터가 없다는 뜻
                if len(statView['ageGroup']) is not 0:
                    # 데이터를 Parsing 하여 view_count_gender_age 테이블에 넣어준다.
                    view_count = parsing.ParsingKeyword(item, statView)
                    # print(view_count)
                    self.result['relGenderCount'] = view_count

            except Exception as e:
                pass
'''


import json
import urllib
from datetime import date
from pprint import pprint

from django.shortcuts import render
from django.views.generic import ListView

from config import settings
from naver_ads_api import SearchAdsSession
from naver_keyword_strategy import KeywordInfoAPI
from naver_main_crawling import NaverCrawl
from naver_trend_api import NaverTrendAPI
from .models import MonthAnalysis


class IndexView(ListView):
    template_name = 'analysis/index.html'

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        qq = "{}".format(q)
        encText = urllib.parse.quote("{}".format(q))

        rel_data = KeywordInfoAPI().rel_keyword_list(qq)
        time_series_data = NaverTrendAPI().trend_graph(qq)

        # sorted_view = sorted(rel_data['relCurView'], reverse=True)

        if 'relGenderCount' in rel_data:
            ## 성별 비율 계산
            sum_female = sum(rel_data['relGenderCount']['f'].values())
            sum_male = sum(rel_data['relGenderCount']['m'].values())
            total_gender = sum_male + sum_female
            female_ratio = round(sum_female/total_gender*100)
            male_ratio = round(sum_male/total_gender*100)

            ## 연령별 비율 계산
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

class InsideView(ListView):
    template_name = 'analysis/inside.html'

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        qq = "{}".format(q)
        encText = urllib.parse.quote("{}".format(q))

        rel_data = KeywordInfoAPI().rel_keyword_list(qq)
        time_series_data = NaverTrendAPI().trend_graph(qq)

        # sorted_view = sorted(rel_data['relCurView'], reverse=True)

        if 'relGenderCount' in rel_data:
            ## 성별 비율 계산
            sum_female = sum(rel_data['relGenderCount']['f'].values())
            sum_male = sum(rel_data['relGenderCount']['m'].values())
            total_gender = sum_male + sum_female
            female_ratio = round(sum_female/total_gender*100)
            male_ratio = round(sum_male/total_gender*100)

            ## 연령별 비율 계산
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
        if q:
            crawl = NaverCrawl()
            pc = crawl.do_crawl(qq)

            context['pc'] = pc

        return render(request, 'analysis/inside.html', context=context)

class ExposurePC(ListView):
    template_name = 'analysis/exppc.html'

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        qq = "{}".format(q)

        if q:
            crawl = NaverCrawl()
            pc = crawl.do_crawl(qq)

            context = {
                'pc': pc,
            }
        else:
            context = {}
        return render(request, 'analysis/exppc.html', context=context)

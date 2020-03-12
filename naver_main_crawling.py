from pprint import pprint

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

from config import settings


class NaverCrawl:
    def do_crawl(self, keyword):
        # Selenium으로 브라우저 구동
        driver = webdriver.Chrome('./analysis/module/chromedriver.exe')
        # driver.implicitly_wait(3)  # seconds
        driver.get('http://naver.com')  # 지정 주소의 웹페이지 방문
        try:
            # 현재 페이지 내에서 name=query 요소 찾고 검색어 입력 후에, form submit
            field = driver.find_element_by_name('query')
            field.send_keys(keyword)
            field.submit()
            print('wait 2 secens...')

            driver.save_screenshot(settings.MEDIA_ROOT+"naver_main.png")
            driver.execute_script("window.scrollTo(0, 660);")
            driver.save_screenshot(settings.MEDIA_ROOT+"naver_main2.png")
            driver.execute_script("window.scrollTo(0, 660*2);")
            driver.save_screenshot(settings.MEDIA_ROOT+"naver_main3.png")
            driver.execute_script("window.scrollTo(0, 660*3);")
            driver.save_screenshot(settings.MEDIA_ROOT+"naver_main4.png")
            driver.execute_script("window.scrollTo(0, 660*4);")
            driver.save_screenshot(settings.MEDIA_ROOT+"naver_main5.png")
            driver.execute_script("window.scrollTo(0, 660*5);")
            driver.save_screenshot(settings.MEDIA_ROOT+"naver_main6.png")
            driver.execute_script("window.scrollTo(0, 660*6);")
            driver.save_screenshot(settings.MEDIA_ROOT+"naver_main7.png")
            driver.execute_script("window.scrollTo(0, 660*7);")
            driver.save_screenshot(settings.MEDIA_ROOT+"naver_main8.png")

            # 검색결과를 보여주기 위해, 페이지 전환이 발생할 텐데
            # 찾고자 하는 요소가 렌더링이 될 때까지, 최대 2초 대기
            condition = EC.presence_of_all_elements_located((By.CLASS_NAME, 'section_head'))
            WebDriverWait(driver, 2).until(condition)
            print('loaded.')

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            naver_crawl = dict()
            idx = 0

            if soup.find_all('li', 'sh_blog_top'):
                '''
                블로그
                '''
                blogs = soup.find_all('li', 'sh_blog_top')
                blog_list = list()
                for blog in blogs:
                    idx += 1
                    date = blog.find('dd')
                    info = blog.find(class_='sh_blog_title')
                    writer = blog.find(class_='inline').find('a')
                    blog_list.append(
                        {'idx': idx, 'date': date.get_text(), 'title': info['title'], 'url': info['href'],
                         'writer': writer.get_text()})
                naver_crawl['blog'] = blog_list
            if soup.find_all('li', 'sh_cafe_top'):
                '''
                카페
                '''
                cafes = soup.find_all('li', 'sh_cafe_top')
                cafe_list = list()
                for cafe in cafes:
                    idx += 1
                    date = cafe.find('dd')
                    info = cafe.find(class_='sh_cafe_title')
                    writer = cafe.find(class_='inline').find('a')
                    cafe_list.append({'idx': idx, 'date': date.get_text(), 'title': info.get_text(), 'url': info['href'],
                                 'writer': writer.get_text()})
                naver_crawl['cafe'] = cafe_list
            if soup.find(class_='kinn section _kinBase'):
                '''
                지식in
                '''
                qnas = soup.find(class_='kinn section _kinBase').find_all('li')
                kin_list = list()
                for qna in qnas:
                    idx += 1
                    date = qna.find('dd')
                    title = qna.find('a')
                    url = qna.find(class_='question').find('a')
                    writer = qna.find(class_='inline')
                    kin_list.append({'idx': idx, 'date': date.get_text(), 'title': title.get_text(), 'url': url['href'],
                                 'writer': writer.get_text()[4:]})
                naver_crawl['kin'] = kin_list
            if soup.find(class_='sp_post section'):
                '''
                포스트
                '''
                posts = soup.find(class_='sp_post section').find_all('li')
                post_list = list()
                for post in posts:
                    idx += 1
                    date = post.find('dd')
                    info = post.find('dt').find('a')
                    writer = post.find('dd', class_='post_info')
                    post_list.append({'idx': idx, 'date': date.get_text(), 'title': info.get_text(), 'url': info['href'],
                                 'writer': writer.get_text()})
                naver_crawl['post'] = post_list
        except TimeoutException:
            return "Loading took too much Time!"
        finally:
            driver.quit()
            pprint(naver_crawl)
        if naver_crawl == {}:
            return "노출된 항목이 없습니다"
        elif naver_crawl:
            return naver_crawl

    def show_crawl(self, keyword):
        headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'),
            'Referer': 'http://www.naver.com',
        }
        res = requests.get('http://www.naver.com/', headers=headers)
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        naver_crawl = dict()
        idx = 0

        if soup.find_all('li', 'sh_blog_top'):
            '''
            블로그
            '''
            blogs = soup.find_all('li', 'sh_blog_top')
            blog_list = list()
            for blog in blogs:
                idx += 1
                date = blog.find('dd')
                info = blog.find(class_='sh_blog_title')
                writer = blog.find(class_='inline').find('a')
                blog_list.append(
                    {'idx': idx, 'date': date.get_text(), 'title': info['title'], 'url': info['href'],
                     'writer': writer.get_text()})
            naver_crawl['blog'] = blog_list
        if soup.find_all('li', 'sh_cafe_top'):
            '''
            카페
            '''
            cafes = soup.find_all('li', 'sh_cafe_top')
            cafe_list = list()
            for cafe in cafes:
                idx += 1
                date = cafe.find('dd')
                info = cafe.find(class_='sh_cafe_title')
                writer = cafe.find(class_='inline').find('a')
                cafe_list.append({'idx': idx, 'date': date.get_text(), 'title': info.get_text(), 'url': info['href'],
                                  'writer': writer.get_text()})
            naver_crawl['cafe'] = cafe_list
        if soup.find(class_='kinn section _kinBase'):
            '''
            지식in
            '''
            qnas = soup.find(class_='kinn section _kinBase').find_all('li')
            kin_list = list()
            for qna in qnas:
                idx += 1
                date = qna.find('dd')
                title = qna.find('a')
                url = qna.find(class_='question').find('a')
                writer = qna.find(class_='inline')
                kin_list.append({'idx': idx, 'date': date.get_text(), 'title': title.get_text(), 'url': url['href'],
                                 'writer': writer.get_text()[4:]})
            naver_crawl['kin'] = kin_list
        if soup.find(class_='sp_post section'):
            '''
            포스트
            '''
            posts = soup.find(class_='sp_post section').find_all('li')
            post_list = list()
            for post in posts:
                idx += 1
                date = post.find('dd')
                info = post.find('dt').find('a')
                writer = post.find('dd', class_='post_info')
                post_list.append({'idx': idx, 'date': date.get_text(), 'title': info.get_text(), 'url': info['href'],
                                  'writer': writer.get_text()})
            naver_crawl['post'] = post_list

if __name__ == "__main__":
    a = NaverCrawl()
    print(a.do_crawl("확진자"))
    # print(a.show_crawl("확진자"))
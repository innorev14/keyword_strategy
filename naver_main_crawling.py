from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

# Selenium으로 브라우저 구동
driver = webdriver.Chrome('./analysis/module/chromedriver.exe')
try:
    # driver.set_window_size(1920, 5060)      #the trick
    driver.get('http://naver.com') # 지정 주소의 웹페이지 방문

    # 현재 페이지 내에서 name=query 요소 찾고 검색어 입력 후에, form submit
    field = driver.find_element_by_name('query')
    field.send_keys('확진자')
    field.submit()
    print('wait 2 secens...')


    # 검색결과를 보여주기 위해, 페이지 전환이 발생할 텐데
    # 찾고자 하는 요소가 렌더링이 될 때까지, 최대 2초 대기
    condition = EC.presence_of_all_elements_located((By.CLASS_NAME, 'sh_blog_title'))
    WebDriverWait(driver, 2).until(condition)
    print('loaded.')

    # driver.save_screenshot("./media/naver_main.png")
    # driver.execute_script("window.scrollTo(0, 660);")
    # driver.save_screenshot("./media/naver_main2.png")
    # driver.execute_script("window.scrollTo(0, 660*2);")
    # driver.save_screenshot("./media/naver_main3.png")
    # driver.execute_script("window.scrollTo(0, 660*3);")
    # driver.save_screenshot("./media/naver_main4.png")
    # driver.execute_script("window.scrollTo(0, 660*4);")
    # driver.save_screenshot("./media/naver_main5.png")
    # driver.execute_script("window.scrollTo(0, 660*5);")
    # driver.save_screenshot("./media/naver_main6.png")
    # driver.execute_script("window.scrollTo(0, 660*6);")
    # driver.save_screenshot("./media/naver_main7.png")
    # driver.execute_script("window.scrollTo(0, 660*7);")
    # driver.save_screenshot("./media/naver_main8.png")

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    naver_crawl = dict()
    if soup.find_all('li', 'sh_blog_top'):
        '''
        블로그
        '''
        blogs = soup.find_all('li', 'sh_blog_top')
        blog_list = list()
        idx = 0
        for blog in blogs:
            idx += 1
            date = blog.find('dd')
            info = blog.find(class_='sh_blog_title')
            writer = blog.find(class_='inline').find('a')
            blog_list.append({'idx':idx ,'date':date.get_text(), 'title': info['title'], 'url':info['href'], 'writer':writer.get_text()})
        naver_crawl['blog'] = blog_list
    if soup.find_all('li', 'sh_cafe_top'):
        '''
        카페
        '''
        cafe_list = list()
        idx = 0
        cafes = soup.find_all('li', 'sh_cafe_top')
        for cafe in cafes:
            idx += 1
            date = cafe.find('dd')
            info = cafe.find(class_='sh_cafe_title')
            writer = cafe.find(class_='inline').find('a')
            cafe_list.append({'idx':idx ,'date':date.get_text(), 'title': info.get_text(), 'url':info['href'], 'writer':writer.get_text()})
        naver_crawl['cafe'] = cafe_list
    if soup.find(class_='kinn section _kinBase').find_all('li'):
        '''
        지식in
        '''
        kin_list = list()
        idx = 0
        qnas = soup.find(class_='kinn section _kinBase').find_all('li')
        for qna in qnas:
            idx += 1
            date = qna.find('dd')
            title = qna.find('a')
            url = qna.find(class_='question').find('a')
            writer = qna.find(class_='inline')
            kin_list.append({'idx':idx ,'date':date.get_text(), 'title': title.get_text(), 'url':url['href'], 'writer':writer.get_text()[4:]})
        naver_crawl['kin'] = kin_list
    if soup.find(class_='sp_post section').find_all('li'):
        '''
        포스트
        '''
        post_list = list()
        idx = 0
        posts = soup.find(class_='sp_post section').find_all('li')
        for post in posts:
            idx += 1
            date = post.find('dd')
            info = post.find('dt').find('a')
            writer = post.find('dd', class_='post_info')
            post_list.append({'idx':idx ,'date':date.get_text(), 'title': info.get_text(), 'url': info['href'], 'writer':writer.get_text()})
        naver_crawl['post'] = post_list

    pprint(naver_crawl)
finally:
    driver.quit()
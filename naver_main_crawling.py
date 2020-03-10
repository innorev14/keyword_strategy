from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

# Selenium으로 브라우저 구동
driver = webdriver.Chrome('./analysis/module/chromedriver.exe')
try:
    driver.get('http://naver.com') # 지정 주소의 웹페이지 방문

    # 현재 페이지 내에서 name=query 요소 찾고 검색어 입력 후에, form submit
    field = driver.find_element_by_name('query')
    field.send_keys('파이썬')
    field.submit()
    print('wait 2 secens...')


    # 검색결과를 보여주기 위해, 페이지 전환이 발생할 텐데
    # 찾고자 하는 요소가 렌더링이 될 때까지, 최대 2초 대기
    condition = EC.presence_of_all_elements_located((By.CLASS_NAME, 'sh_blog_title'))
    WebDriverWait(driver, 2).until(condition)
    print('loaded.')

    driver.save_screenshot("./naver_main.png")
    driver.execute_script("window.scrollTo(0, 660);")
    driver.save_screenshot("./naver_main2.png")
    driver.execute_script("window.scrollTo(0, 660*2);")
    driver.save_screenshot("./naver_main3.png")
    driver.execute_script("window.scrollTo(0, 660*3);")
    driver.save_screenshot("./naver_main4.png")
    driver.execute_script("window.scrollTo(0, 660*4);")
    driver.save_screenshot("./naver_main5.png")
    driver.execute_script("window.scrollTo(0, 660*5);")
    driver.save_screenshot("./naver_main6.png")
    driver.execute_script("window.scrollTo(0, 660*6);")
    driver.save_screenshot("./naver_main7.png")
    driver.execute_script("window.scrollTo(0, 660*7);")
    driver.save_screenshot("./naver_main8.png")



    # 방법1) 지정 태그요소 찾기
    # for tag in driver.find_elements_by_css_selector('.sh_blog_title'):
        # print(tag.text, tag.get_attribute('href'))

    # 방법2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    tag_list = soup.select('.sh_blog_title')
    for tag in tag_list:
        print(tag['href'])
finally:
    driver.quit()
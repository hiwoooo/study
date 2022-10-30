from selenium.webdriver.common.by import By
from time import sleep
import math 
import pandas as pd
import Chrome_driver
import Keesung_logging
import datetime as dt
import os
import sys

def base_data():
    '''    
    Returns
    -------
    crawling Dict.

    '''
    
    global url
    global category
    global product
    global company
    global price1
    global price2
    global introduction
    global ingredients
    global skinType
    global product1
    global colors_text
    
    base_dict = {
        'timestamp' : dt.datetime.now().strftime('%Y%m%d_%H%M%S'),
        'category' : category,
        'productName' : product,
        'urlProduct' : url,
        'brand' : company,
        'productName.1' : product1,
        'price1' : price1,
        'price2' : price2,
        'Color' : colors_text,
        'ingredients' : ingredients,
        'skinType' : skinType,
        'username' : '_alchera_none_',
        'datePublished' : '_alcheras_none_',
        'reviewText' : '_alchera_none_',
        'score' : '_alchera_none_',
        'reviewerSkinType' : '_alchera_none_'
        }
    return base_dict

# 사용자명과 평점 수집 함수 정의 - 쿠팡용, 수정 전
def get_page_data():
    '''
    base_data를 불러와 username, rating, review를 크롤링 한다.
    
    '''
    datas = driver.find_element(By.CSS_SELECTOR, '.inner_list')
    id_datas = datas.find_elements(By.CSS_SELECTOR, '.info')
    review_datas = datas.find_elements(By.CSS_SELECTOR, '.review_cont')

    for id_data, review_data in zip(id_datas, review_datas):
        if len(data_list) == 200: # 목표 리뷰 갯수
            break
        user = id_data.find_element(By.CLASS_NAME, 'id').text.strip()
        rating = review_data.find_element(By.CSS_SELECTOR, '.point').text.split(' ')[1].replace('점','')
        date = review_data.find_element(By.CSS_SELECTOR, '.date').text
        review = review_data.find_element(By.CSS_SELECTOR, '.txt_inner').text
        review = review.strip()
        try:
            reviewerSkintype = id_data.find_element(By.CLASS_NAME, 'tag').text
            reviewerSkintype = reviewerSkintype.replace('\n', ';')
        except:
            reviewerSkintype = '_alchera_none_'
        tmp_dict = base_data()
        tmp_dict['username'] = user
        tmp_dict['score'] = int(rating)
        tmp_dict['datePublished'] = date
        tmp_dict['reviewText'] = review
        tmp_dict['reviewerSkinType'] = reviewerSkintype
        data_list.append(tmp_dict)
        
interval = 1
logger = Keesung_logging.my_logger()
driver = Chrome_driver.auto_chrome_driver(1)
input("Press enter to start operations...")
windows = sorted(driver.window_handles)
driver.switch_to.window(windows[1])

if os.path.exists('Result') == False:
    os.mkdir('Result')
    
_, csv_filename = sys.argv
# csv_filename = 'C:/Users/user/Desktop/Git/_project/Seongwook.Chun/Oliveyong_url/url데이터/쉐이딩_컨투어링.csv'
save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Result')
csv_file = pd.read_csv(csv_filename)

for product, url in zip(csv_file['product_name'], csv_file['product_url']):
    start_time = dt.datetime.now()
    data_list = []  # 모든 데이터 담는 리스트
    try:
        save_product = product.replace('/', '_').replace('\\', '_')
        if os.path.isfile(f"Result/{save_product}.csv"):
            logger.info(f'{product} 크롤링 파일이 이미 존재합니다.')
            continue
        driver.get(url)
        sleep(3)
        
        # 리뷰 갯수 따오기
        review_total = driver.find_element(By.CSS_SELECTOR, '.goods_reputation').find_element(By.TAG_NAME, 'span').text[1:-1]
        review_total = int(review_total.replace(',',''))
        review_total = min(review_total, 400) # 400개 까지만 추출
        review_per_page = 10
        total_page = review_total / review_per_page
        total_page = math.ceil(total_page)

        # 카테고리 추출
        category = os.path.splitext(os.path.split(csv_filename)[1])[0]
        category = category.replace('_', '/')
        
        # 색상 옵션 선택
        try:
            colors = driver.find_element(By.CSS_SELECTOR, '.sel_option').click()
            sleep(1)
            colors = driver.find_elements(By.CSS_SELECTOR, '.option_value')
            colors_text = ';'.join([x.text.split('\n')[0].strip() for x in colors])
        except:
            colors = []
            colors_text = '_alchera_none_'
            
        # 제조회사
        company = driver.find_element(By.ID, 'moveBrandShop').text
        
        # 성분 추출, 피부타입
        driver.find_element(By.CSS_SELECTOR, '.goods_buyinfo').click()
        sleep(2)
        info_list = driver.find_elements(By.CSS_SELECTOR, '.detail_info_list')
        ingredients = '_alchera_none_'
        skinType = '_alchera_none_'
        for info in info_list:
            if info.find_element(By.TAG_NAME, 'dt').text == '화장품법에 따라 기재해야 하는 모든 성분':
                ingredients = info.find_element(By.TAG_NAME, 'dd').text
                ingredients = ingredients.split('\n\n')[0]
            elif info.find_element(By.TAG_NAME, 'dt').text == '제품 주요 사양':
                skinType = info.find_element(By.TAG_NAME, 'dd').text

        # 소개
        introduction = '_alchera_none_'
        
        # 제품 이름
        product1 = driver.find_element(By.CSS_SELECTOR, '.prd_name').text
        
        # 할인 가격
        price2 = driver.find_element(By.CSS_SELECTOR, '.price-2').find_element(By.TAG_NAME, 'strong').text
        price2 = int(price2.replace(',', ''))
        # 기존 가격
        try:
            price1 = driver.find_element(By.CSS_SELECTOR, '.price-1').find_element(By.TAG_NAME, 'strike').text
            price1 = int(price1.replace(',', ''))
        except:
            price1 = price2
    
        driver.find_element(By.CSS_SELECTOR, '.goods_reputation').click()
        sleep(2)
        
        # 첫 페이지 수집하고 시작
    
        get_page_data() 
        page = 1
        logger.info('1 page 수집 끝')
        # 버튼을 눌러서 페이지를 이동해 가면서 계속 수집.
        # 예외처리를 해줘야 함. 하지 않으면 중지됨.
        for page in range(2, total_page+1):
            try:
                if len(data_list) >= 200: # 목표 리뷰 갯수
                    break
                #1 0page 수집이 끝나서 11로 넘어가기 위해서는 > 버튼을 눌러야 함.
                if(page % 10 == 1):
                    driver.find_element(By.CSS_SELECTOR, '.pageing').find_element(By.CSS_SELECTOR, '.next').click()
                    sleep(2)
                else:
                    if page <= 10:
                        button_index = page % 10 - 2
                    else:
                        button_index = page % 10 - 1
                        
                    # 데이터 수집이 끝난 뒤 다음 페이지 버튼을 클릭
                    pages = driver.find_element(By.CSS_SELECTOR, '.pageing').find_elements(By.TAG_NAME, 'a')
                    pages[button_index].click()
                    sleep(2)
        
                # 해당 페이지 데이터 수집 
                get_page_data()
                logger.info(f'{page} page 수집 끝')
            except Exception as e:
                logger.error(f'{page} page 수집 에러  - {e}')
        
        print(str(page) + " page 수집 끝")
        logger.info('수집 종료')
            
        df = pd.DataFrame(data_list)
        
        # 엑셀로 저장
        save_path = os.path.join(save_dir, f"{save_product}.csv")
        df.to_csv(save_path)
        logger.info(f'{save_path} 저장 완료')
        
    except Exception as e:
        logger.error(f'{product} - {url} - {e}')
    logger.info(dt.datetime.now() - start_time)
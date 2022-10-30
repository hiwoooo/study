# -*- coding: utf-8 -*-

"""
Created on Wed Sep 28 10:08:45 2022

@author: user
"""
import os
from selenium import webdriver
import subprocess
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

def auto_chrome_driver(interval, chrome_path=f'''
                       "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"
                       ''' ):
    subprocess.Popen(chrome_path.strip()) # 디버거 크롬 구동
    # subprocess.Popen(f'''"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"''') # 디버거 크롬 구동
    
    option = Options()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    
    try:
        driver = webdriver.Chrome(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{chrome_ver}/chromedriver.exe'), options=option)
    except:
        chromedriver_autoinstaller.install(True, path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{chrome_ver}/chromedriver.exe'))
        driver = webdriver.Chrome(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{chrome_ver}/chromedriver.exe'), options=option)
    driver.implicitly_wait(interval)
    return driver
    
if __name__ == "__main__":
    driver = auto_chrome_driver(1)


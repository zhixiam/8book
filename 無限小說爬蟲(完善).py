# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 16:47:46 2023

@author: mot66
"""

import requests
from bs4 import BeautifulSoup
import time
import re

if __name__ == "__main__":

    headers = {
        'Cookie':'CFFPCKUUID=4840-ijLiPxcJ27Dvoib0allPuZLykw9Mg4bK; CFFPCKUUIDMAIN=7072-nFBRAoPcpuyXYq6NwMf5dffz4ytLBrUm; FPUUID=7072-a95a512f5c20d8ffa2d4a1657320b58bea3cc469009842f2575b0731bbdfb289',
        'Referer':'https://8book.com/novelbooks/190388/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }

# 要爬取的網站的URL
    url = 'https://8book.com/novelbooks/190388/'  # 你想要解析的網站

# 發送HTTP請求獲取網頁內容
    response = requests.get(url,headers = headers)

# 檢查是否成功獲取網頁
    if response.status_code == 200:
        # 使用Beautiful Soup解析HTML內容
        soup = BeautifulSoup(response.text, 'html.parser')
    
        # 找到小說的標題
        title_element = soup.find('title')
        try:
            title_element = title_element.encode('iso-8859-1').decode('utf-8')#解碼
        except UnicodeDecodeError:
            pass
        # 找到所有的章節名稱和連結        
        chapters = soup.find_all('a', class_='episode_li')    
        filename = re.sub(r'[^\u4e00-\u9fa5]+', '', title_element)#只留下中文
        filename = f'./{filename}.txt'
        print(f'小說標題: {filename}')
        fp = open(filename,'w',encoding='utf-8')
        for chapter in chapters:
            chapter_title = chapter.text.strip()
            try:
                chapter_title = chapter_title.encode('iso-8859-1').decode('utf-8')
            except UnicodeDecodeError:
                pass
            chapter_link = 'https://8book.com'+chapter['href']
            print(f'章節名稱: {chapter_title}')
            
            
            #開始解析
            #使用正則表達式來取得href裡的數字(如:/read/176997/?19893782)
            real_link = chapter['href']
            
            match = re.search(r'/(\d+)/\?(\d+)', real_link)

            if match:
                extracted_number = match.group(2)#只取(如:19893782)
                
            #開始計算變量          
            ca0g1s8 = extracted_number
            # 定義所需的變數(固定)
            b7y404w = 3
            wq__17kjr1 = 100
            mr2d75 = 5
            # 計算參數索引值(固定)
            index = (int(ca0g1s8) * b7y404w) % wq__17kjr1 

            # input_string 是一個用調用index來取其中[index:end_index]參數
            # input_string 每次拉取不同的小說都需更新(如:176997/?19893782)放置參數的位置
            input_string = "557971111492887538355986363477935263918856221937962892966171874446772563959877544541623321783718387525551995218864734383"
            end_index = index + 5
            desired_digits = input_string[index:end_index]#帶入到url裡

            # 構建最終的URL 
            # 將章節?以後的數值ca0g1s8與desired_digits
            url = f"https://8book.com/txt/8/190388/{ca0g1s8}{desired_digits}.html"
            print(url)
            # url = f"https://8book.com/txt/8/190388/928490836347.html" 進入到未編譯內文
            # 再次發送GET請求訪問URL
            response = requests.get(url)              
            # 處理響應
            if response.status_code == 200:
                # 成功訪問URL，可以繼續處理頁面內容
                page_content = response.text.encode('iso-8859-1').decode('utf-8')
                soup = BeautifulSoup(page_content,'html.parser')
                # 在這裡處理頁面內容
                page_content = soup.get_text()#編譯後的內文
                cleaned_text = re.sub(r'[^\u4e00-\u9fa5，。？！、]+', '', page_content)#用正規表示法去除多餘的防盜流水
                character_count = len(cleaned_text)#計算字數
                print(f'爬取成功,字數為{character_count}')
                
                # 寫入的text檔案
                fp.write(f"章節名稱: {chapter_title}\n")
                fp.write(f"{cleaned_text}\n")
                time.sleep(3)


    else:
        print('無法獲取網頁內容')

                
        
        
        
        
        
        
        
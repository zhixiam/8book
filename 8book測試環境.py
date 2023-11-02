# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 20:17:19 2023

@author: mot66
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from bs4 import BeautifulSoup
import time
import re

if __name__ == "__main__":

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }

    data = input('小說名:')
    # 目标URL
    url = 'https://8book.com/'
    
    # 创建一个会话
    session = requests.Session()
    
    # 发送GET请求以获取搜索页面

    response = session.get(url)
    
    # 解析页面内容
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 找到搜索表单
    search_form = soup.find('form', class_='search-box-main')
    
    # 构建搜索数据
    search_data = {
        'key': data,  # 将关键词替换为你想要搜索的内容
    }
    
    # 提交搜索请求
    search_url = url + 'search/'  # 替换为实际的搜索URL
    response = session.get(search_url, params=search_data)
    
    # 解析搜索结果
    search_results = BeautifulSoup(response.content, 'html.parser')
    
    # 处理搜索结果，提取所需的信息
    # 你可以使用Beautiful Soup来解析搜索结果页面，并提取你需要的信息
    
    # 例如，输出搜索结果的标题
    
    title = search_results.find_all('div',class_='row p-1 mx-1')

    for i in title:
        #取得小說編號/novelbooks/122216
        link = i.find('a',class_='w-100 nowraphide').get('href')
        match = re.search(r'/(\d+)', link)
        if match:
            link = match.group(1)#只取(如:122216)

        
# 要爬取該小說的網站URL
    url2 = f'https://8book.com/novelbooks/{link}'  # 你想要解析的網站
# 發送HTTP請求獲取網頁內容
    response = requests.get(url2,headers = headers)

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
        name = re.sub(r'[^\u4e00-\u9fa5]+', '', title_element)#只留下中文
        print(f'小說標題: {name}')
        filename = f'./{name}.txt'
        fp = open(filename,'w',encoding='utf-8')
        # 找到所有的章節名稱和連結
        chapters = soup.find_all('a', class_='episode_li')
        for chapter in chapters:
            chapter_title = chapter.text.strip()
            try:
                chapter_title = chapter_title.encode('iso-8859-1').decode('utf-8')
            except UnicodeDecodeError:
                pass
            chapter_link = 'https://8book.com'+chapter['href']
            print(f'章節名稱: {chapter_title}')
            #爬取script的var變量取得小說計算參數
            url3 = chapter_link
            response = requests.get(url3,headers = headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script')
            # 使用正则表达式来匹配变量
            pattern = r"var (\w+)=\"(\d+(?:,\d+)*)\"\.split\('\s*,\s*'\);"
            matches = []
            for script in scripts:
                script_text = script.text
                matches.extend(re.findall(pattern, script_text, re.DOTALL))
                # 使用正则表达式查找匹配
                if matches:
                    for match in matches:
                        variable_name = match
                        pattern = r"(\d+)$"
                        # 再次使用正則表達式來從元組取得最後的參數
                        matches = re.search(pattern, variable_name[1])                           
                        if matches:
                            last_group_of_numbers = matches.group(1)
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
            #input_string = "557971111492887538355986363477935263918856221937962892966171874446772563959877544541623321783718387525551995218864734383"
            input_string = last_group_of_numbers 
            end_index = index + 5
            desired_digits = input_string[index:end_index]#帶入到url裡
            start_num = 1
            end_num = 8
            num_to_test = start_num
            found_valid_url = False
            valid_url = None
            expected_character_count = 500
            # 構建最終的URL 
            # 將num_to_test循環驗證章節?以後的數值ca0g1s8與desired_digits
            while num_to_test <= end_num:
                if not valid_url:
                    url = f"https://8book.com/txt/{num_to_test}/{link}/{ca0g1s8}{desired_digits}.html"
                    # url = f"https://8book.com/txt/8/190388/928490836347.html" 進入到未編譯內文
                            

                    try:
                        response = requests.get(url)              
                        # 處理響應
                        if response.status_code == 200:

                            valid_url = url
                            found_valid_url = True  # 找到有效的 URL 后标记为 True
                                  # 获取页面内容
                            page_content = response.text.encode('iso-8859-1').decode('utf-8')
                            soup = BeautifulSoup(page_content, 'html.parser')
                                  # 在这里处理页面内容
                            page_content = soup.get_text()  # 编译后的内文
                            cleaned_text = re.sub(r'[^\u4e00-\u9fa5，。？！、]+', '', page_content)  # 用正规表示法去除多余的防盗流水
                            character_count = len(cleaned_text)  # 计算字数

                                    
                            # 验证已爬取的字数是否符合预期
                            if character_count >= expected_character_count:
                                pass                                        
                            else:
                                valid_url = None
                        else:
                            print(f"URL {url} 是无效的") 
                    except requests.exceptions.RequestException as e:
                        print(f"URL {url} 请求发生异常: {e}")
                num_to_test += 1
                
            if valid_url:       
                response = requests.get(valid_url)
                # 处理页面内容
                if response.status_code == 200:
                    page_content = response.text.encode('iso-8859-1').decode('utf-8')
                    soup = BeautifulSoup(page_content, 'html.parser')
                    # 在这里处理页面内容
                    page_content = soup.get_text()  # 编译后的内文
                    cleaned_text = re.sub(r'[^\u4e00-\u9fa5，。？！、]+', '', page_content)  # 用正规表示法去除多余的防盗流水
                    character_count = len(cleaned_text)  # 计算字数
                    print(f'爬取成功 字数为{character_count}')
                    print(f'連結 {valid_url}')
                    # 写入的text文件
                    fp.write(f"章節名稱: {chapter_title}\n")
                    fp.write(f"{cleaned_text}\n")
                    time.sleep(3)
                    
    else:
        print('無法獲取網頁內容')
fp.close()

    
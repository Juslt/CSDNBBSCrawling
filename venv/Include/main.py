#!/usr/bin/env python
# encoding=utf-8

import requests
from bs4 import BeautifulSoup
import codecs
import xlwt

BASE_URL = "https://bbs.csdn.net"
CSDN_URL = "https://bbs.csdn.net/tech_hot_topics"


def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(url, headers=headers)
    return data.content


def parse_detail_html(html):

    post_names =[] # 当前帖子下的顶贴人名的集合
    soup = BeautifulSoup(html)
    head_div =soup.find('div',attrs={'class':'mod_topic_wrap post topic'})
    name = head_div.find('div',attrs={'class':'nick_name'}).find('a').getText() # 发帖人的名字

    post_divs = soup.findAll('div',attrs={'class':'mod_topic_wrap post'})
    for post_div in post_divs:
        post_name = post_div.find('div',attrs={'class':'nick_name'}).find('a').getText() # 顶贴人的名字
        post_names.append(post_name)

    print("head_name:"+name)

    if(len(post_names)==0):
        return name, None
    else:
        return name,post_names

def parse_html(html):
    soup = BeautifulSoup(html)

    list_1 = soup.find('div', attrs={'class': 'list_1'})
    ul = list_1.find('ul')
    list_list = ul.findAll('li')

    heads_names=[] # 发帖人名集合
    head_dic = {} # 发帖人对应得字典

    filter_post_names = []
    for li_item in list_list:
        title_url = li_item.find('a')['href']
        title_detail_url = BASE_URL + title_url
        detail_html = download_page(title_detail_url)
        head_name, post_names = parse_detail_html(detail_html)
        if(post_names==None):
            continue

        heads_names.append(head_name)
        filter_post_names.extend(post_names)

        post_dic = {}  # 顶帖人对应的字典
        nameSet = set(post_names)
        for item in nameSet:
            post_dic[item] = post_names.count(item)
            print("the %s has found %d" % (item, post_names.count(item)))

        head_dic[head_name] = post_dic


    return heads_names,filter_post_names,head_dic

    # next_page = soup.find('a',attrs={'class':'next'})
    # if(next_page):
    #     end_string = next_page['href'].split('?')
    #     return title_url_list,CSDN_URL+"?"+end_string[1]
    # return title_url_list,None

def writeExcel(heads_names,all_post_names,head_dic1,head_dic2,head_dic3,head_dic4):
    print("")
    # 实例化一个Workbook()对象(即excel文件)
    wbk = xlwt.Workbook()
    # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)

    # 初始化列表
    for column in range(len(heads_names) + 1):
        for row in range(len(all_post_names) + 1):
            if (column == 0 and row == 0):
                sheet.write(row, column, "")
            else:
                sheet.write(row, column, 0)

    # 填入所有的发帖人
    for i in range(len(heads_names)):
        sheet.write(0, i + 1, heads_names[i])

    # 填入所有的回帖人
    for j in range(len(all_post_names)):
        sheet.write(j + 1, 0, all_post_names[j])

    # 填入有数据的内容
    for key, value in head_dic1.items():
        column = heads_names.index(key) + 1
        for key_2, value_2 in value.items():
            row = all_post_names.index(key_2) + 1
            sheet.write(row, column, value_2)

    for key, value in head_dic2.items():
        column = heads_names.index(key) + 1
        for key_2, value_2 in value.items():
            row = all_post_names.index(key_2) + 1
            sheet.write(row, column, value_2)

    for key, value in head_dic3.items():
        column = heads_names.index(key) + 1
        for key_2, value_2 in value.items():
            row = all_post_names.index(key_2) + 1
            sheet.write(row, column, value_2)

    for key, value in head_dic4.items():
        column = heads_names.index(key) + 1
        for key_2, value_2 in value.items():
            row = all_post_names.index(key_2) + 1
            sheet.write(row, column, value_2)

    # 以传递的name+当前日期作为excel名称保存。
    wbk.save("csdn_spider.xls")
    print("head_names_size:" + str(len(heads_names)) + "-------post_names:" + str(len(all_post_names)))


def main():
    url = CSDN_URL
    url2= "https://bbs.csdn.net/tech_hot_topics?page=2"
    url3= "https://bbs.csdn.net/tech_hot_topics?page=3"
    url4= "https://bbs.csdn.net/tech_hot_topics?page=4"

    html = download_page(url)
    heads_names1, filter_post_names1, head_dic1 = parse_html(html)

    html = download_page(url2)
    heads_names2, filter_post_names2, head_dic2 = parse_html(html)
    html = download_page(url3)
    heads_names3, filter_post_names3, head_dic3 = parse_html(html)
    html = download_page(url4)
    heads_names4, filter_post_names4, head_dic4 = parse_html(html)

    heads_names =[]
    heads_names.extend(heads_names1)
    heads_names.extend(heads_names2)
    heads_names.extend(heads_names3)
    heads_names.extend(heads_names4)

    filter_post_names=[]
    filter_post_names.extend(filter_post_names1)
    filter_post_names.extend(filter_post_names2)
    filter_post_names.extend(filter_post_names3)
    filter_post_names.extend(filter_post_names4)

    all_post_names=[] # 所有顶帖人集合
    all_post_names.extend(set(filter_post_names))

    #写入Excel中
    writeExcel(heads_names,all_post_names,head_dic1,head_dic2,head_dic3,head_dic4)
    # with codecs.open('news','wb',encoding='utf-8') as fp:
    #     while url:
    #         html = download_page(url)
    #         news,url = parse_html(html)
    #         fp.write(u'{news}\n'.format(news='\n'.join(news)))

    # print(data.content)


if __name__ == '__main__':
    main()




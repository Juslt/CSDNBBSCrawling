# coding:utf-8
import requests
import random
import string
from bs4 import BeautifulSoup
import re
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy

url_list = []
fatieren = []
huitieren = []
dict = {}
def get_url():
    url = 'https://bbs.csdn.net/tech_hot_topics'
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    header = {"User-Agent": user_agent}
    wb_data = requests.get(url).content
    soup = BeautifulSoup(wb_data,'html.parser')
    try:
        id_all = soup.find_all('a',target="_blank")
        for id in id_all:
            id1 = id.get("href")
            zz = re.compile(r'\w*39\w*')
            id2 = zz.findall(id1)
            id3 = "".join(id2).strip()
            if id3 !=  '':
                base_url = 'https://bbs.csdn.net/topics/'
                Url =  base_url + id3
                url_list.append(Url)
        return url_list
    except Exception as  e:
        print(e)

def get_data():
    url_list = get_url()
    for url in url_list:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        header = {"User-Agent": user_agent}
        wb_data = requests.get(url).content
        soup = BeautifulSoup(wb_data, 'html.parser')
        send_name = soup.find_all('a',rel="nofollow")
        i = 0
        for k in send_name:
            k1 = k.string
            if k1 != None and k1 != '引用':
               if i == 0:
                   fatieren.append()
               else:
                  huitieren.append()
               i = i + 1
            else:
                pass
    fatieren_set = list(set(fatieren))
    huitieren_set = list(set(huitieren))
    excel = xlwt.Workbook(encoding= 'ascii')
    sheet = excel.add_sheet('bbs')
    for i in range(0,len(fatieren_set)):
        sheet.write(0,i+1,fatieren_set[i])
    for j in range(0,len(huitieren_set)):
        sheet.write(j+1,0,huitieren_set[j])
    excel.save('test.xls')
    return huitieren
def deal_data():
    url_list = get_url()
    for url in url_list:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        header = {"User-Agent": user_agent}
        wb_data = requests.get(url).content
        soup = BeautifulSoup(wb_data, 'html.parser')
        send_name = soup.find_all('a',rel="nofollow")
        i = 0
        list1 = []
        for k in send_name:
            k1 = k.string
            if k1 != None and k1 != '引用':
                if i == 0:
                    dict[k1] = list1
                else:
                    list1.append(k1)
                i = i + 1
            else:
                pass
    print(dict)
if __name__ == '__main__':
    deal_data()

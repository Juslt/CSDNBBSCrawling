import requests
from bs4 import BeautifulSoup

def main():
    # 请求微博数据
    url ="https://weibo.com/bjfbt?is_all=1&stat_date=201806#feedtop"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    headers = {
        'User-Agent': user_agent,
        'Cookie':'SINAGLOBAL=2572789625768.6123.1537948484009; _ga=GA1.2.145867018.1543934483; UM_distinctid=16a10a125ab0-086a126ea834b5-e323069-1fa400-16a10a125ac85b; wb_view_log_6728808634=1920*10801%261536*8641.25; wb_view_log=1920*10801; un=18511037880; wvr=6; UOR=,,www.baidu.com; Ugrow-G0=1ac418838b431e81ff2d99457147068c; ALF=1597325439; SSOLoginState=1565789439; SCF=AjkE-Ox_rdN1Ltu5v1yaSJTjtgLh7grg_svtdlW9E5qRt1i172a94JHmbYrGIr54iCo1a8kXkxVh8ladY7gqozY.; SUB=_2A25wUHyvDeRhGeBJ6VoZ8CbKyDiIHXVTJOlnrDV8PUNbmtAKLVrzkW9NRkbOuW3oqF8YgnlF-dTiuZHAKJiD1TXl; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWGraqBN-9OjTMRICemKgSE5JpX5KzhUgL.FoqNeonRehnce0B2dJLoI7n0xcvj9sLV97tt; SUHB=0jB4ZXl4iBNV0B; YF-V5-G0=d30fd7265234f674761ebc75febc3a9f; _s_tentry=login.sina.com.cn; Apache=5760084432231.271.1565789440873; ULV=1565789440904:45:3:3:5760084432231.271.1565789440873:1565748736935; webim_unReadCount=%7B%22time%22%3A1565789467115%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A31%2C%22msgbox%22%3A0%7D; YF-Page-G0=aac25801fada32565f5c5e59c7bd227b|1565789480|1565789442',
        'Referer':'https://weibo.com/bjfbt?is_all=1&stat_date=201806',
        'Host':'weibo.com'
    }

    wb_data = requests.get(url,headers=headers).content

    print(wb_data)
    # 解析数据
    soup = BeautifulSoup(wb_data, 'html.parser')
    feed_list = soup.find_all('div',attrs={'class':'WB_cardwrap WB_feed_type S_bg2 WB_feed_like '})
    print(len(feed_list))
    for feed_item in feed_list:
        feed_content = feed_item.find('div',attrs={'class':'WB_text W_f14'})
        print(feed_content)

if __name__ == '__main__':
    main()
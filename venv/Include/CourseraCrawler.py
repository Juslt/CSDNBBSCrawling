import requests
from bs4 import BeautifulSoup
import xlwt

# 请求url，获取源码
host_url = "https://www.coursera.org"
# url = "https://www.coursera.org/courses?query=data%20analysis&page=1&configure%5BclickAnalytics%5D=true&indices%5Bprod_all_products_custom_ranking_revenuelast28d%5D%5Bpage%5D=3&indices%5Bprod_all_products_custom_ranking_revenuelast28d%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Bprod_all_products_custom_ranking_revenuelast28d%5D%5Bconfigure%5D%5BhitsPerPage%5D=10"
url = "https://www.coursera.org/courses?query=data%20analysis&indices%5Bprod_all_products_custom_ranking_revenuelast28d%5D%5Bpage%5D=6&indices%5Bprod_all_products_custom_ranking_revenuelast28d%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Bprod_all_products_custom_ranking_revenuelast28d%5D%5Bconfigure%5D%5BhitsPerPage%5D=10&indices%5Bprod_all_products_custom_ranking_revenuelast28d%5D%5BrefinementList%5D%5Bskills%5D%5B0%5D=Data%20Analysis&configure%5BclickAnalytics%5D=true"
class Data:
    def __init__(self,course_name,course_company,time,language,captions):
        self.course_name = course_name
        self.course_company = course_company
        self.time = time
        self.language = language
        self.captions = captions


def parse_detail_html(detail_path):
    content = requests.get(detail_path).content
    soup = BeautifulSoup(content)
    divs = soup.find("div", attrs={"class": "ProductGlance hideOnLarge_1oaat0b p-t-2"})
    time_string=""
    language=""
    captions = ""
    for div in divs:
        svg = div.find("svg",attrs={"class":"SvgIcon_8wfvj4"})
        if(svg!=None):
            title = svg.find("title")
            if (title != None and title.getText()== "Hours to complete"):
                div2 = div.find("div", attrs={"Box_120drhm-o_O-displayflex_poyjc-o_O-columnDirection_ia4371"})
                if (div2 != None):
                    div_captions = div2.find("h4",attrs={"class": "H4_1k76nzj-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 m-b-0"})
                    if (div_captions != None):
                        time = div_captions.find("span")
                        if (time != None):
                            time_string = time.getText()
                            print(time.getText())
            if (title != None and title.getText() == "Available languages"):
                language = div.find("h4").getText()
                div_captions = div.find("div", attrs={"class": "font-sm text-secondary"})
                if (div_captions != None):
                    captions = div_captions.find("span").getText()
                    print(language)
                    print(captions)
                    print("***********************************************************")
    return time_string,language,captions
    # language = soup.find("h4",attrs={"class":"H4_1k76nzj-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 m-b-0","data-reactid":"351"}).getText()
    # language = div.find("h4",attrs={"class":"H4_1k76nzj-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 m-b-0"}).getText()
    # language = soup.find("h4",attrs={"class":"H4_1k76nzj-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 m-b-0"}).getText()
    # captions = soup.find("div",attrs={"class":"font-sm text-secondary"}).find("span").getText()
    # print(language)

def writeExcel(list):
    # 实例化一个Workbook()对象(即excel文件)
    wbk = xlwt.Workbook()
    # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)

    # 绘制
    for i in range(len(list)):
        sheet.write(i,0,list[i].course_name)
        sheet.write(i,1, list[i].course_company)
        sheet.write(i, 2, list[i].time)
        sheet.write(i, 3, list[i].language)
        sheet.write(i, 4, list[i].captions)

    # 以传递的name+当前日期作为excel名称保存。
    wbk.save("coursera_crawler.xls")
    print("complete _ write")

def parse_html(html):
    soup = BeautifulSoup(html)
    li_list = soup.find("ul", attrs={"class": "ais-InfiniteHits-list"})

    list = []
    for course_li in li_list:
        course_name = course_li.find("h2", attrs={"class": "color-primary-text card-title headline-1-text"}).getText()
        course_company = course_li.find("span", attrs={"class": "partner-name"}).getText()
        a = course_li.find("a")
        to_path = a['to']
        print(course_name, "---", course_company, to_path)

        time, language, captions= parse_detail_html(host_url + to_path)
        data = Data(course_name,course_company,time,language,captions)
        list.append(data)
    writeExcel(list)


def del_data():
    heads = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(url)
    parse_html(data.content)


if __name__ == '__main__':
    del_data()




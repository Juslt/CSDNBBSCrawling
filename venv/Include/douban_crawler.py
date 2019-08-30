import requests
from bs4 import BeautifulSoup


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get("https://movie.douban.com/top250", headers=headers).content

    soup = BeautifulSoup(data, 'html.parser')
    # movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})
    # for movie_li in movie_list_soup.find_all('li'):
    #     detail = movie_li.find('div', attrs={'class': 'hd'})
    #     movie_name = detail.find('span', attrs={'class': 'title'}).getText()


    li = soup.find('div',attrs={'class':'paginator'})
    print(li)


if __name__ == '__main__':
    main()

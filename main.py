import requests
import timeit
from selenium import webdriver
from bs4 import BeautifulSoup
from termcolor import colored
import re


# 209.97.161.10:3128 -  Сингапур
proxies = {
    'http': 'http://93.190.137.63:8080',
    'https': 'https://54.39.53.104:3128',
}

headers = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}

url = 'https://zenit25072019.top/line/view/#!/sport5/league3669/'
try:
    #  url = 'https://zenit25072019.top/line/view/#!/sport5/league3669/'
    #  158.174.108.132:8190

    r = requests.get(url, proxies=proxies, timeout=10, headers=headers)
    with open('test1.html', 'wb') as f:
        f.write(r.text.encode('utf-8'))
except requests.exceptions.ConnectionError:
    print("Connection is failed")

url1 ='https://twitter.com/home/'
url = 'https://zenit25072019.top/line/view/#!/sport5/league3669/'
chrome_options = webdriver.ChromeOptions()
proxy = '54.39.53.104:3128'
chrome_options.add_argument('--proxy-server=%s' % proxy)
browser = webdriver.Chrome(executable_path=r"/home/noor/chromedriver", chrome_options=chrome_options)
browser.get(url)
html = browser.page_source
with open('selenium_parsed_home.html', 'w') as f:
    f.write(html)
print("Please wait, I'm processing the web-page...")
soup = BeautifulSoup(html)  # парсим всю страницу
matches_list = soup.find('div', {'class': 'a-s-g-n'})  # находим див, в котором лежит наша таблица матчей
matches = matches_list.find_all('td', {'class': 'g-d-td'})  # берем матч
teams = matches[0].find('a', {'class': 'g-d g-d-s'}).find_all('nobr')

# цикл, который кидает в список все теги tr с class = "4420591"
tr_list = matches_list.find_all('tr', {'class': re.compile(r'^g-tr g-tr-4420\d{3} [oe]$')})
# print(tr_list)
# tr_list - это список всех ячеек таблицы с полной инфой по каждому матчу
for tr in tr_list:
    # print('full tr:{}'.format(tr)), tr - это одна ячейка всей инфы по матчу
    print("Match:")
    pair = tr.find('a', {'class': 'g-d g-d-s'}).find_all('nobr')  # список из команд вместе с тегом, извлекаются с text
    print('\033[1m' + '{} vs {}\033[0m'.format(pair[0].text, pair[1].text))
    raw_coeffs = tr.find_all('a', {'class': 'g-b'})
    # print('raw coeffs - {}'.format(raw_coeffs)) - список _коэфициентов_ и тегов конкретного матча
    home_team_wins = raw_coeffs[0].text
    away_team_team_wins = raw_coeffs[1].text
    if home_team_wins > away_team_team_wins:
        print("First team wins - {}\nSecond team wins - {}".format(colored(home_team_wins, 'green'),
                                                                     colored(away_team_team_wins, 'red')))
    else:
        print("First team wins - {}\nSecond team wins - {}".format(colored(home_team_wins, 'red'),
                                                                   colored(away_team_team_wins, 'green')))
    print('First handicap - {}'.format(raw_coeffs[2].text))
    print('Second handicap - {}'.format(raw_coeffs[3].text))
    print('Total less - {}'.format(raw_coeffs[4].text))
    print('Total more - {}\n'.format(raw_coeffs[5].text))


browser.close()
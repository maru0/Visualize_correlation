from bs4 import BeautifulSoup
import urllib.request
import pdb
import re
import pandas as pd
from time import sleep
import random
import os


class Todoran():
    def __init__(self):
        self.industrial_economy = "https://todo-ran.com/t/gcateg/90001"
        self.culture_live_health = "https://todo-ran.com/t/gcateg/90002"
        self.store_distribution = "https://todo-ran.com/t/gcateg/90003"
        self.entertainment_sports = "https://todo-ran.com/t/gcateg/90004"
        self.country_infra = "https://todo-ran.com/t/gcateg/90005"
        self.society_politics = "https://todo-ran.com/t/gcateg/90006"

    def calcuration(self):
        #self._extract(self.industrial_economy)
        #self._extract(self.culture_live_health)
        self._extract(self.store_distribution)
        self._extract(self.entertainment_sports)
        self._extract(self.country_infra)
        self._extract(self.society_politics)

    def _extract(self,url):
        #instance = urllib.request.urlopen(self.industrial_economy)
        instance = urllib.request.urlopen(url)
        soup = BeautifulSoup(instance,"html.parser")
        categ_tables = soup.find_all('',class_=re.compile("categ_table"))
        main_categorys = soup.find_all('h3',class_="kiji_divtitle")
        categories = []

        # catego_listには農業や水産業などカテゴリごとの内容のリンク先が格納
        for i,catego_list in enumerate(categ_tables):
            title = main_categorys[i].text.strip('□ ')
            catego_list = catego_list.find_all('a')
            sleep(5 + random.randint(0,5))
            target_category = []
            for category in catego_list:
                target_category.append({category.text.strip():category.get("href")})
            self._extract_data(target_category,title)

    def _extract_data(self,targets,cate_dir):
        self._my_makedirs(cate_dir)
        for data_urls in targets:
            for title,url in data_urls.items():
                dfs = pd.read_html(url)
                sleep(5 + random.randint(0,5))
                save_csv = self._search_pd(dfs)
                if save_csv.empty:
                    print(title)
                    print("This is empty")
                else:
                    # 保存
                    try:
                        title = re.sub('（.*）','',title)
                        path = cate_dir + "/" + title.split(' ')[0] + ".csv"
                        save_csv.to_csv(path,encoding="utf-8")
                        #print("ok")
                    except:
                        print(title)
                        print("どうしても無理な箇所")


    def _my_makedirs(self,path):
        if not os.path.isdir(path):
            os.makedirs(path)


    def _search_pd(self,dfs):
        for i in range(len(dfs)):
            try:
                tmp = dfs[i]['偏差値']
                return dfs[i]
            except:
                pass
        return pd.DataFrame()


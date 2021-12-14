from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

r = requests.get("https://yokatlas.yok.gov.tr/lisans-bolum.php?b=10056")
page = "https://yokatlas.yok.gov.tr/"

soup = BeautifulSoup(r.content, "lxml")

links = soup.findAll("h4", {'class': 'panel-title'})

universities = []
arr = []
if os.path.isfile("universities.pkl"):
    df = pd.read_pickle("universities.pkl")
    print("exist")
    print(df)

else:
    for link in links:
        children = link.findChildren("a", recursive=False)
        for child in children:
            main_link = page + child.get('href')
            ch = child.findChildren("div")
            uni_number = child.get('href')[-9:]
            for div in ch:
                arr = [div.text, main_link, uni_number]
                universities.append(arr)

    df = pd.DataFrame(universities)
    df.to_pickle("universities.pkl")

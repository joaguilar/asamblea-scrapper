from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib3
import re
import csv
import crawler
import time

url = "http://www.asamblea.go.cr/Diputados/SitePages/Inicio.aspx"

result = requests.get(url)
# print(result.text)

doc = BeautifulSoup(result.text,"html.parser")
h5s = doc.findAll("h5")
paginasDiputados = []
for oneh5 in h5s:
    print(oneh5)
    print("|"+str(oneh5)+"|")
    name = re.findall('>.*</a>',str(oneh5))[0].replace(">","").replace('</a','')
    url = re.findall('href=".*?"',str(oneh5))[0].replace('href="','').replace('"','')
    print("Diputado: {}, url: {}".format(name,url))
    paginasDiputados.append(
        {
            "diputado": name,
            "url": "http://www.asamblea.go.cr"+url
        }
    )
csv_columns = ['diputado','url']
csv_file = "paginasDiputados.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in paginasDiputados:
            writer.writerow(data)
except IOError:
    print("I/O error")

for data in paginasDiputados:
    crawler.prepareDocsToCrawl(page=data["url"],diputado=data["diputado"])

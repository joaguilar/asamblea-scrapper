import string
from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import urlparse
from pathlib import Path

import re
import csv
from selenium import webdriver
import time


def prepareDocsToCrawl(page:string, diputado:string):
    print('Procesando pagina del diputado:"'+diputado+'" pagina:'+page)
    result = requests.get(page)
    doc = BeautifulSoup(result.text,"html.parser")
    paginaIntervenciones = ""
    for tag in doc.findAll("a"):
        if ('href' in tag.attrs and ("Intervenciones" in tag.attrs['href'])):
            paginaIntervenciones = "http://www.asamblea.go.cr"+tag.attrs['href']
    processPaginaIntervenciones(paginaIntervenciones,diputado,first=True)

def processPaginaIntervenciones(paginaIntervenciones:string, diputado:string, first=False):
    print("Procesando pagina intervenciones: "+paginaIntervenciones)
    result = requests.get(paginaIntervenciones)
    intervenciones = BeautifulSoup(result.text,"html.parser")
    # docs = doc.select
    documentsToDownload=[]
    for theDiv in intervenciones.find_all("div",class_="ms-vb itx"):
        for child in theDiv.findChildren("a"):
            if ('href' in child.attrs and ("docx" in child.attrs['href'])):
                theUrl = 'http://www.asamblea.go.cr'+child.attrs['href']
                print("Document to download: "+ theUrl)
                documentsToDownload.append(
                    {
                        "url":theUrl,
                        "fileName": Path(urlparse(theUrl).path).name
                    }
                )
    # print(intervenciones)
    csv_columns = ['url',"fileName"]
    csv_file = "data/toDownload/"+diputado+".csv"
    try:
        with open(csv_file, 'a+') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            if (first):
                writer.writeheader()
            for data in documentsToDownload:
                writer.writerow(data)
    except IOError:
        print("I/O error")
    #Check for more pages:
    if (first):
        for theA in intervenciones.find_all("a"):
            if('onclick' in theA.attrs and ("javascript:RefreshPageTo" in theA.attrs["onclick"])):
                print(theA.attrs["onclick"])
                theNewUrl = 'http://www.asamblea.go.cr'+str(theA.attrs["onclick"]).replace('javascript:RefreshPageTo(event, "','').replace('");javascript:return false;','')
                print(theNewUrl)
                processPaginaIntervenciones(theNewUrl,diputado)


def main():
    # diputado = "Carlos Ricardo Benavides"
    # prepareDocsToCrawl("http://www.asamblea.go.cr/Diputados/benavides_jimenez/SitePages/Curriculum.aspx",diputado)
    with open("paginasDiputados.csv",'r') as readFile:
        csv_reader = csv.DictReader(readFile)
        for row in csv_reader:
           print(row)
           time.sleep(1)
           prepareDocsToCrawl(page=row["url"],diputado=row["diputado"])
        #    break;


if __name__ == "__main__":
    main()    


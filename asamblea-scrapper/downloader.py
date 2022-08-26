import requests
import re
import csv
import time
import string
from os import listdir, makedirs
from os.path import isfile, join, splitext, isdir

def downloadUrl(destDir:string,destName:string,url:string):
    r = requests.get(url, allow_redirects=True) 
    destPath = destDir+'/'+destName
    with open(destPath,'wb') as theFile:
        theFile.write(r.content)
    

def downloadDocuments(csvDir:string,destDir:string):
    #Get list of csv files to process:
    time.sleep(5)
    csvFiles = [f for f in listdir(csvDir) if isfile(join(csvDir, f))]
    print(csvFiles)
    for csvfile in csvFiles:
        downloadDestination = destDir+'/'+splitext(csvfile)[0]
        if (isdir(downloadDestination)):
            print('Download destination "'+downloadDestination+'" already exists, next!')
        else:
            print('Download destination "'+downloadDestination+'" doesn''t exists, creating it')
            makedirs(downloadDestination)

        print("Download to: "+downloadDestination)
        print("Opening CSV file")
        with open(csvDir+'/'+csvfile,'r') as theDiputadoFile:
            csv_reader = csv.DictReader(theDiputadoFile)
            for rowToDownload in csv_reader:
                downloadTo = downloadDestination+'/'+rowToDownload["fileName"]
                print('Downloading |'+rowToDownload["url"]+'| into |'+downloadTo+'|')
                downloadUrl(
                    destDir=downloadDestination,
                    destName=rowToDownload["fileName"],
                    url=rowToDownload["url"]
                )
                time.sleep(1)




def main():
    downloadDocuments("data/toDownload","data/diputados")
    # downloadUrl(
    #     destDir="data/diputados/Aida María Montiel Héctor",
    #     destName="Montiel Hector, abril 2019.docx",
    #     url="""http://www.asamblea.go.cr/Diputados/montiel_hector/Intervenciones_Plenario/Montiel Hector, abril 2019.docx""")

if __name__ == "__main__":
    main()   
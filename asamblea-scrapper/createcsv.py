import zipfile, re
import os
import sys
import random
import pandas as pd

def progressbar(it, prefix="", size=60, out=sys.stdout): # Python3.6+
    count = len(it)
    def show(j):
        x = int(size*j/count)
        print(f"{prefix}[{u'█'*x}{('.'*(size-x))}] {j}/{count}", end='\r', file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)

def list_all_files(path,pattern):
    all_files = []
    for root, dir_names, file_names in os.walk(path):
        for f in file_names:
            # print("{} {} ".format(pattern,f))
            if(re.match(pattern,f)):
                # print(os.path.join(root, f))
                all_files.append(os.path.join(root, f))
    return all_files

def getOutputFile(file,from_dir,to_dir,from_ext,to_ext):
    newFile = file
    newFile = newFile.replace(from_ext,to_ext)
    newFile = newFile.replace(from_dir,to_dir)
    return newFile

def extractTextOneFile(file,from_dir,to_dir):
    try:
        docx = zipfile.ZipFile(file)
    except:
        return False
    content = docx.read('word/document.xml').decode('utf-8')
    cleaned = re.sub('<(.|\n)*?>','\n',content)
    cleaned = re.sub('\n\n','',cleaned)
    # print(cleaned)
    outputFile = getOutputFile(file,from_dir,to_dir, "docx", "txt")
    os.makedirs(os.path.dirname(outputFile), exist_ok=True)
    # print(outputFile)
    with open(outputFile,'w') as f:
         f.write(cleaned)
    
    return outputFile

def returnTextOneFile(file):
    
    with open(file,'r') as f:
        text =  f.read()
        cleaned = re.sub('HYPERLINK.+\n','\n',text)
        cleaned = re.sub('PAGEREF.+\\\\h','\n',cleaned)
        cleaned = re.sub('TOC.+\\\\h','\n',cleaned)
    
    return cleaned

def extractTextFromDocuments(from_dir):
    files_to_extract = list_all_files(from_dir,".+\.txt")
    files_extracted = []
    for i in progressbar(range(len(files_to_extract)), "Procesando %d archivos" % len(files_to_extract), 80):
        f = returnTextOneFile(files_to_extract[i])
        if (f):
            files_extracted.append(f)
    return files_extracted

def concatenateTextFromFiles(files_extracted,to_file):
    with open(to_file,'w') as f:
        for i in progressbar(
            range(len(files_extracted)), 
            "Procesando %d archivos" % len(files_extracted), 
            80):
            with open(files_extracted[i],'r') as fe:
                lines = fe.readlines()
                for line in lines:
                    if len(line) < 8:
                        lines.remove(line)
                f.writelines(lines)
    return

    


def main():
    files_extracted = extractTextFromDocuments("data/text")
    random.shuffle(files_extracted)
    df = pd.DataFrame(files_extracted, columns = ['text'])
    df.to_csv("diputados.csv")

    # print (files_extracted)
    # concatenateTextFromFiles(files_extracted,"data/text/all_text.txt")


if __name__ == "__main__":
    main()  
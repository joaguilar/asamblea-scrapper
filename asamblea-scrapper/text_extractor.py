import zipfile, re
import os
import sys
import random

dias=[
'Lunes',
'Martes',
'Miércoles',
'Jueves',
'Viernes',
'unes',
'artes',
'iércoles',
'ueves',
'iernes'
]
meses=[
    'Enero',
    'Febrero',
    'Marzo',
    'Abril',
    'Mayo',
    'Junio',
    'Julio',
    'Agosto',
    'Septiembre',
    'Octubre',
    'Noviembre',
    'Diciembre'
]
comisiones=[
    'Control Político'
]
periodos=[
    'Primero',
    'Primera',
    'Segundo',
    'Segunda',
    'Tercero',
    'Tercera',
    'Cuarto',
    'Cuarta',
    'Quinto',
    'Quinta',
    'Sexto',
    'Sexta',
    'Septimo',
    'Septima'
]
sesiones=[
    'extraordinarias',
    'ordinarias',
    'extraordinaria',
    'ordinaria',
    'plenaria'
]

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

def cleanText(content):
    cleaned = re.sub('<(.|\n)*?>','\n',content)
    cleaned = re.sub('\n\n','',cleaned)
    cleaned = re.sub(rf"Acta de la sesión plenaria ({'|'.join(sesiones)}) N\s*?\.\s*?º\s*?[0-9]+",'',cleaned, flags=re.IGNORECASE|re.MULTILINE|re.DOTALL)
    cleaned = re.sub(rf"sesión plenaria ({'|'.join(sesiones)}) N\s*?\.*?\s*?º\s*?[0-9]+",'',cleaned, flags=re.IGNORECASE|re.MULTILINE|re.DOTALL)
    cleaned = re.sub(rf"({'|'.join(periodos)}) período de sesiones extraordinarias",'',cleaned, flags=re.IGNORECASE|re.MULTILINE|re.DOTALL)
    cleaned = re.sub(rf"({'|'.join(periodos)}) legislatura",'',cleaned, flags=re.IGNORECASE|re.MULTILINE|re.DOTALL)
    fechas = rf"({'|'.join(dias)})\s+\d+\s+\w+\s+({'|'.join(meses)})\s+\w+\s+\d+"
    # print (fechas)
    cleaned = re.sub(fechas,'',cleaned, flags=re.IGNORECASE|re.MULTILINE|re.DOTALL)
    cleaned = re.sub("^.*?Contenido\s*?(TOC|No se encontraron entradas de tabla de contenido).+$",'',cleaned, flags=re.IGNORECASE|re.MULTILINE)
    cleaned = re.sub("^\s*\d{1}\s*\n",'',cleaned, flags=re.IGNORECASE|re.MULTILINE)
    cleaned = re.sub("^\s*del\s*\n",'',cleaned, flags=re.IGNORECASE|re.MULTILINE)
    cleaned = re.sub("_Toc\d+.+$",'',cleaned, flags=re.IGNORECASE|re.MULTILINE)
    cleaned = re.sub("^.+PAGEREF.*$",'',cleaned, flags=re.IGNORECASE|re.MULTILINE)
    cleaned = re.sub("^.*?HYPERLINK.*$",'',cleaned, flags=re.IGNORECASE|re.MULTILINE)
    cleaned = re.sub(rf"Diputad(o|a).*?:",'',cleaned, flags=re.IGNORECASE|re.MULTILINE)
    cleaned = re.sub(rf"INTERVENCIÓN POR .*?$",'',cleaned, flags=re.IGNORECASE|re.MULTILINE)
    cleaned = re.sub(rf"^(\s*?{'|'.join(comisiones)})\s*?$",'',cleaned, flags=re.IGNORECASE|re.MULTILINE)
    cleaned = re.sub('HYPERLINK.+\n','\n',cleaned)
    cleaned = re.sub('PAGEREF.+\\\\h','\n',cleaned)
    cleaned = re.sub('TOC.+\\\\h','\n',cleaned)
    return cleaned


def extractTextOneFile(file,from_dir,to_dir):
    try:
        # print("File: "+file)
        docx = zipfile.ZipFile(file)
    except:
        return False
    content = docx.read('word/document.xml').decode('utf-8')
    cleaned = cleanText(content)
    outputFile = getOutputFile(file,from_dir,to_dir, "docx", "txt")
    os.makedirs(os.path.dirname(outputFile), exist_ok=True)
    # print(outputFile)
    with open(outputFile,'w',encoding='utf-8') as f:
        f.write(cleaned)
    
    return outputFile


def extractTextFromDocuments(from_dir,to_dir):
    files_to_extract = list_all_files(from_dir,".+\.docx")
    files_extracted = []
    for i in progressbar(range(len(files_to_extract)), "Procesando %d archivos" % len(files_to_extract), 80):
        f = extractTextOneFile(files_to_extract[i],from_dir,to_dir)
        if (f):
            files_extracted.append(f)

    return files_extracted

def concatenateTextFromFiles(files_extracted,to_file):
    with open(to_file,'w',encoding='utf-8') as f:
        for i in progressbar(
            range(len(files_extracted)), 
            "Procesando %d archivos" % len(files_extracted), 
            80):
            with open(files_extracted[i],'r',encoding='utf-8') as fe:
                lines = fe.readlines()
                for line in lines:
                    if len(line) < 8:
                        lines.remove(line)
                f.writelines(lines)
    return

    


def main():
    files_extracted = extractTextFromDocuments("data/diputados","data/text")
    random.shuffle(files_extracted)

    # print (files_extracted)
    concatenateTextFromFiles(files_extracted,"data/text/all_text.txt")


if __name__ == "__main__":
    main()  
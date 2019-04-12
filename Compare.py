import webbrowser
import pandas as pd
import datetime
import glob

files_dir="./files/"
def getFiles(pattern):
    return glob.glob(pattern)

def getScripts():
    all_scripts = ""
    scripts=getFiles("./js/*.js")
    for sf in scripts:
        f = open(sf,"r")
        all_scripts +=  "\r\n//"+sf+"\r\n" + f.read() 
        f.close()
    return all_scripts



input_files=getFiles(files_dir+"*.csv")

csvCount = len(input_files)
data = []
table = []
rowSayisi = []
csvFile = []
#usecols ile istenen sutunlari okutabiliriz
for i in range(0,csvCount): #csv dosyalarinin pathlerini data listesine yaz
    plsWork = input_files[i]
    data.append(plsWork)

for i in range(0,csvCount): #data pathlerini oku ve table listesine yaz
    plsWork2 = pd.read_csv(data[i])
    table.append(plsWork2)

csv_sutun_isimleri = ["TIME","PQ","CPU","MEMORY"]
for i in range(0,csvCount): #Her table icin sutun ata
    table[i].columns = csv_sutun_isimleri

for i in range(0,csvCount):  #Her table icin farkli bir row sayisi olmali
    plsWork3 = len(table[i])
    rowSayisi.append(plsWork3)

for i in range(0,csvCount): #alter table islemi
    datetimeFormat = "%H:%M:%S"
    maxT = max(table[i]["TIME"])
    minT = min(table[i]["TIME"])
    diff = datetime.datetime.strptime(maxT, datetimeFormat) - datetime.datetime.strptime(minT, datetimeFormat)
    table[i].drop("TIME",axis=1,inplace=False)
    table[i]["TIME"] = diff

    maxPq = max(table[i]["PQ"])
    minPq = min(table[i]["PQ"])
    avgPq = (maxPq-minPq) / rowSayisi[i]

    #pqV = sum(table[i]["PQ"])
    table[i].drop("PQ",axis=1,inplace=False)
    table[i]["PQ"] = avgPq
    cpuV = sum(table[i]["CPU"]) / rowSayisi[i]
    table[i].drop("CPU",axis=1,inplace=False)
    table[i]["CPU"] = cpuV
    memoryV = sum(table[i]["MEMORY"]) / rowSayisi[i]
    table[i].drop("MEMORY",axis=1,inplace=False)
    table[i]["MEMORY"] = memoryV
    plsWork4 = table[i][:1]
    csvFile.append(plsWork4)





jsonResultObject={}; 



for n in range(0,len(csvFile)):
    file_name=input_files[n]
    file_name = file_name.split("/")[-1]

    e = csvFile[n]
    json = {}
    json["time"]=e["TIME"].get(0).total_seconds()
    json["pq"]=e["PQ"].get(0) 
    json["cpu"]=e["CPU"].get(0) 
    json["memory"]=e["MEMORY"].get(0) 
    jsonResultObject[file_name]=json
 


file=open("./template.html","r")
template = file.read()
file.close()


template= template.replace("{{output}}",str(jsonResultObject))
template = template.replace("{{scripts}}",getScripts())
outfile=open("output.html","w")
outfile.write(template)
outfile.close()
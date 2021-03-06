import requests
import pathlib
import os
import pdf2image
import time
from datetime import datetime
from bs4 import BeautifulSoup

status = False

def download_edt(file_name):
    print(file_name.split('/')[0][1], int(file_name.split('/')[1].split('_')[1].split('.')[0].replace('S','')))
    cmd = f"python /home/jeremod/Bureau/Programmation/BotIUT/convertEdtPdf/pdfToPng.py {file_name.split('/')[0][1]} {int(file_name.split('/')[1].split('_')[1].split('.')[0].replace('S',''))}"
    os.system(cmd)


def fetch_edt(status):
    if (status == True):
        return
    status = True
    print(datetime.now().strftime('[%d/%m/%Y %H:%M:%S]'),"================ Recuperation des edts ================")
    html = BeautifulSoup(requests.get(
        "http://edt-iut-info.unilim.fr/edt/").content, features="html.parser")
    listPromo = html.select('td a')
    listPromo.pop(0)
    for link in listPromo:
        html = BeautifulSoup(requests.get(
            "http://edt-iut-info.unilim.fr/edt/"+link.get('href')).content, features="html.parser")
        listEdt = html.select('tr')
        for edt in listEdt[3:-1]:
            data = edt.select('td')
            name = data[1].find('a').get('href')
            date = data[2].text.split(' ')
            date_edt = [int(data) for data in date[0].split("-")]
            heure_edt = [int(data) for data in date[1].split(":")]
            date = datetime(int(date_edt[0]), int(date_edt[1]), int(
                date_edt[2]), heure_edt[0], heure_edt[1])
            try:
                with open('edt/' + name.split('.')[0] + '.json') as f:
                    if(datetime.fromtimestamp(pathlib.Path('edt/' + name.split('.')[0] + '.json').stat().st_ctime) < date):
                        download_edt(link.get('href')+name)
            except IOError:
                download_edt(link.get('href')+name)
    print(datetime.now().strftime('[%d/%m/%Y %H:%M:%S]'),"========================== Fin ==========================")
    status = False

fetch_edt(status)


while True:
    time.sleep(7200)
    fetch_edt(status)
import urllib.request
import datetime
import json
import sys
import os
from time import time
 
def loadJson(Dir):
    """Json 파일에 저장된 데이터 불러오기"""
    with open(Dir, 'r') as file:
        ls = json.load(file)
    return ls

def saveJson(Dir, data):
    """데이터를 Json 파일에 저장하기"""
    with open(Dir, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent="\t")

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

def workingDirectory():
    if getattr(sys, 'frozen', False):
        #test.exe로 실행한 경우,test.exe를 보관한 디렉토리의 full path를 취득
        currDir = os.path.dirname(os.path.abspath(sys.executable))    
    else:
        #python test.py로 실행한 경우,test.py를 보관한 디렉토리의 full path를 취득
        currDir = os.path.dirname(os.path.abspath(__file__))
    return currDir

def filesInFolder(Dir, extention=0):
    if extention:
        return [file.replace(f".{extention}", "") for file in os.listdir(Dir) if file.endswith(f".{extention}")]
    else:
        return [file for file in os.listdir(Dir)]

def download_file(url, filename):
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

def log(text):
    currDir = os.path.dirname(os.path.realpath(__file__))
    with open(f'{currDir}/log.txt', 'a') as file:
        file.write(f"{datetime.datetime.now()} - {text}\n")

def inputType(func):
    return func.__annotations__

def checkTime(func, *params):
    start = time()
    output = func(*params)
    return (time()-start, output)


currDir = os.path.dirname(os.path.realpath(__file__))
from typing import List
from fastapi import FastAPI, Body, UploadFile, Response
from fastapi.responses import FileResponse
import pandas as pd
import csv
import os


app = FastAPI()

@app.post("/case_sensitive")
def dublic(q: list):
    x = 0
    i = 0
    dup = [y for i, y in enumerate(q) if i != q.index(y)]
    for i in range(len(dup)):
        dup[i] = dup[i].lower()
    srt_lst = set()
    index = 0
    x = 0
    for index in range(len(q)):
        if q[index].lower() not in dup:
            srt_lst.add(q[index].lower())
    res = list(srt_lst)
    return res

@app.post("/upload/{file.name}")
def s_files(file_name,response: Response, files: List[UploadFile]):
    uns_files = []
    for file in files:
        if file.filename.partition('.')[-1] not in ["csv", "json"]:
            uns_files.append(file.filename)

    if bool(uns_files):
        response.status_code = 415
        return uns_files



    dat = []
    for file in files:
        dt_r = pd.read_csv(file.file, sep=';') if file.content_type == "text/csv" else pd.read_json(file.file)
        dat.append(dt_r)
        dt_r = pd.concat(dat, dt_r)
    dt_r = pd.concat(dat)
    writer_file(file_name,dt_r)


@app.post("/load/{file_name}")
def new_file(file_name, response: Response):
    if search(file_name):
        return FileResponse(search(file_name))
    else:
        response.status_code = 404
        return file_name + ".cvs"

data_dir = 'data/' if os.environ.get('DATA_DIR') is None else os.environ.get('DATA_DIR')
if not os.path.isdir('data'):
    os.mkdir('data')
def search(file_name):
    if os.path.isfile(data_dir + file_name + '.csv'):
        return data_dir + file_name + '.csv'
    else:
        return False

def writer_file(filename, data):
    path = search(filename)
    if path:
        file_w = pd.read_csv(path, sep=';')
        data = pd.concat([file_w, data])
    else:
        path = data_dir + filename + '.csv'
        f = open(path, 'w+')
        f.close()

        data.to_csv(path, sep=';')
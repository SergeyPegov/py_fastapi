from fastapi import FastAPI

app = FastAPI()


@app.post("/case_sensitive")
async def dublic(q: list):
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
async def 
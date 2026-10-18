from fastapi import FastAPI
from gg import *

app = FastAPI()

@app.post("/kg")
async def create_item(item: str):
    return ramayana(item)

@app.post("/kg_mini")
async def create_item(item: str):
    kanda = item.split(":")[0]
    if kanda == "balakanda":
        return query_engine_balakanda2.query(item).response
    elif kanda == "ayodhyakanda":
        return query_engine_ayodhyakanda2.query(item).response
    elif kanda == "aranyakanda":
        return query_engine_aranyakanda2.query(item).response
    elif kanda == "kishkindhakanda":
        return query_engine_kishkindhakanda2.query(item).response
    elif kanda == "sundarakanda":
        return query_engine_sundarakanda2.query(item).response
    elif kanda == "yuddhakanda":
        return query_engine_yuddhakanda2.query(item).response
    elif kanda == "uttarakanda":
        return query_engine_uttarakanda2.query(item).response
    else:
        return ramayana(item)

# @app.post("/kg2")
# async def create_item(item: str):
#     return query_engine_rag.query(item)

# @app.post("/rag2")
# async def create_item(item: str):
#     return query_engine_rag.query(item)
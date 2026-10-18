from fastapi import FastAPI

app = FastAPI()

with open("cooking/log.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    r = ""
    for line in lines:
        r += line + "\n"

@app.post("/kg")
async def create_item(item: str):
    return r
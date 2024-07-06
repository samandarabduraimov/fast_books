from fastapi import FastAPI



app = FastAPI()


@app.get("/")
async def get_home():
    return {"message": "Hello FastAPI"}

@app.get("/a")
async def get_user():
    return {"message": "Hello Worl   aetrytrtsrytd"}



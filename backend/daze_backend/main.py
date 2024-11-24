from fastapi import FastAPI

app = FastAPI()

# GET route
@app.get("/")
async def base_get_route():
    return {"message": "hello world"}

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Daze Backend"}

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import home, auth

app = FastAPI()
app.include_router(auth.router)
app.include_router(home.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
async def home():
    return {"message": "Silence is Golden!"}

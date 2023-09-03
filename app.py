from typing import Union
from fastapi import FastAPI
import home

api_version = "/api/v1"

app = FastAPI()
app.include_router(home.router, prefix=api_version)


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import config_app
from .routers.apikeys import router as apikeys_router
from .routers.applications import router as applications_router
from .routers.auth import router as auth_router
from .routers.companies import router as companies_router
from .routers.home import router as home_router
from .routers.json import router as json_router

app = FastAPI(title=config_app.APP_NAME, version=config_app.API_VERSION)
app.include_router(apikeys_router)
app.include_router(applications_router)
app.include_router(companies_router)
app.include_router(auth_router)
app.include_router(json_router)
app.include_router(home_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

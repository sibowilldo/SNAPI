from fastapi import APIRouter

router = APIRouter(prefix="", tags=[], responses={404: {"message": "Resource not found!"}})


@router.get("/")
async def home():
    return {"message": "Silence is Golden!"}


@router.get("/changelog")
async def changelog():
    return {"message": "Success", "data": {"v1_0_0": ""}}

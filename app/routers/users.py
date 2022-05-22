from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

fake_users_db = {"0": { "name": "anton", "surname": "ego"}}

@router.get("/")
async def read_items():
    return fake_users_db
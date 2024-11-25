import uvicorn
from fastapi import FastAPI

from app.api.endpoints.currency import currency_router
from app.api.endpoints.users import auth_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(currency_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app")


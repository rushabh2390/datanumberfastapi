from email.header import Header
from telnetlib import STATUS
from typing import Collection
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from schemas import DatesIn, DatesResponse, Months
from functools import lru_cache

from crud import (
    create_dates,
    fetch_all_dates,
    get_popular,
    delete_dates
)
from database import SessionLocal, engine
from typing import Union
import models
import config

models.Base.metadata.create_all(bind=engine)


@lru_cache()
def get_settings():
    return config.Settings()


# App Object
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get("/")
# def read_root():
#     return {"message": "hello world"}


@app.get("/api/dates", response_model=list(), status_code=200)
async def get_dates(db: Session = Depends(get_db)):
    response = await fetch_all_dates(db)
    return response


@app.post("/api/dates", response_model=DatesResponse, status_code=201)
async def post_dates(dates: DatesIn,  db: Session = Depends(get_db)):

    data = await create_dates(db=db, dates_data=dates)
    if data:
        return data
    raise HTTPException(400, "Something went wrong/ Bad Request")


@app.get("/api/popular", response_model=list(), status_code=200)
async def get_popular_months(db: Session = Depends(get_db)):
    response = await get_popular(db)
    return response


@app.delete("/api/dates/{id}", response_model=str, status_code=200)
async def delete_dates_by_id(id: int, db: Session = Depends(get_db),
                             X_API_KEY: Union[str, None] = Header(default=None),
                             settings: config.Settings = Depends(get_settings)):
    if X_API_KEY == settings.secret_api_key:
        response = await delete_dates(db, id)
        if response:
            return "successfully deleted dates!"
        raise HTTPException(404, f"No data Found {id}")
    raise HTTPException(401, f"Unauthorized Access")

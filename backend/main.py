from email.header import Header
from typing import Collection
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, responses, Depends, Header
from fastapi.middleware.cors import CORSMiddleware

from schemas import Dates, DatesIn, DatesResponse
from functools import lru_cache
from models import Dates as ModelDates

import aiohttp
from crud import (
    create_dates,
    fetch_all_dates,
    get_popular,
    delete_dates
)
from database import SessionLocal, engine
from typing import Union
import os
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
# app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get("/")
# def read_root():
#     return {"message": "hello world"}


@app.get("/api/dates")
async def get_dates(db: Session = Depends(get_db)):
    response = fetch_all_dates(db)
    return response


@app.post("/api/dates", response_model=DatesResponse)
async def post_dates(dates: DatesIn,  db: Session = Depends(get_db)):
    async with aiohttp.ClientSession() as session:
        async with session.get("http://numbersapi.com/"+str(dates.month)+"/"+str(dates.day)+"/date") as resp:
            description = await resp.text()
    dates_data = DatesResponse(
        day=dates.day, month=dates.month, fact=description)
    data = create_dates(db=db, dates_data=dates_data)
    if data:
        return dates_data
    raise HTTPException(400, "Something went wrong/ Bad Request")


@app.get("/api/popular")
async def get_popular_months(db: Session = Depends(get_db)):
    response = get_popular(db)
    return response


@app.delete("/api/dates/{id}", response_model=str)
async def delete_dates_by_id(id: int, db: Session = Depends(get_db),
                       X_API_KEY: Union[str, None] = Header(default=None), 
                       settings: config.Settings = Depends(get_settings)):
    if X_API_KEY == settings.secret_api_key:
        response = delete_dates(db, id)
        if response:
            return "successfully deleted dates!"
        raise HTTPException(404, f"There is no dates with this id {id}")
    raise HTTPException(401, f"Unauthorized Access")

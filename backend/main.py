import config
import models
from database import SessionLocal, engine
from crud import (
    create_dates,
    fetch_all_dates,
    get_popular,
    delete_dates
)
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from schemas import DatesIn, DatesResponse
from functools import lru_cache
from typing import Union
import logging
logging.basicConfig(level=logging.DEBUG)

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


@app.get("/api/dates", status_code=200)
async def get_dates(db: Session = Depends(get_db)):
    response = await fetch_all_dates(db)
    if response:
        return response
    raise HTTPException(200, "no data available")


@app.post("/api/dates", response_model=DatesResponse, status_code=201)
async def post_dates(dates: DatesIn,  db: Session = Depends(get_db)):

    data, error = await create_dates(db=db, dates_data=dates)
    if data:
        return data
    if error:
        raise HTTPException(500, "Something went wrong/ Bad Request")
    raise HTTPException(500, "Something went wrong/ Bad Request")


@app.get("/api/popular", status_code=200)
async def get_popular_months(db: Session = Depends(get_db)):
    response = await get_popular(db)
    if response:
        return response
    raise HTTPException(200, "no data available")


@app.delete("/api/dates/{id}", status_code=200)
async def delete_dates_by_id(id: int, db: Session = Depends(get_db),
                             X_API_KEY: Union[str, None] = Header(default=None),
                             settings: config.Settings = Depends(get_settings)):
    if X_API_KEY == settings.secret_api_key:
        response = await delete_dates(db, id)
        if response:
            logging.debug(f'{id} data deleted')
            return "successfully deleted dates!"
        raise HTTPException(404, f"No data Found at {id}")
    logging.debug("unauthorized access occurs")
    raise HTTPException(401, "Unauthorized Access")

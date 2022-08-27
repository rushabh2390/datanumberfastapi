from crud import (
    create_dates,
    fetch_all_dates
)
from typing import Collection
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, responses, Depends
from fastapi.middleware.cors import CORSMiddleware
from schemas import Dates, DatesIn, DatesResponse
from models import Dates as ModelDates
import aiohttp
import os
import crud
import models
import schemas
from database import SessionLocal, engine
from dotenv import load_dotenv

models.Base.metadata.create_all(bind=engine)


load_dotenv('.env')

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
    dates_data = DatesResponse(day=dates.day, month=dates.month, fact= description)
    data = create_dates(db=db, dates_data=dates_data)
    if data:
        return dates_data
    raise HTTPException(400, "Something went wrong/ Bad Request")


# @app.put("/api/dates{title }", response_model=DatesResponse)
# async def put_dates(title: str, desc: str):
    # response = await update_todo(title,desc)
    # if response:
    #     return response
    # raise HTTPException(404, f"There is no TODO item with this title {title}")


# @app.delete("/api/dates/{title}")
# async def delete_dates(title):
    # response = await remove_todo(title)
    # if response:
    #     return "successfully deleted todo Item!"
    # raise HTTPException(404, f"There is no TODO item with this title {title}")

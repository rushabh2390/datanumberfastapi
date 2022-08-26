from crud import (
    create_dates,
    fetch_all_dates
)
from typing import Collection
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, responses, Depends
from fastapi.middleware.cors import CORSMiddleware
from schemas import Dates as SchemaDates
from schemas import DatesIn as SchemaDatesInput
from schemas import DatesResponse as SchemaDatesResponse
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


# @app.get("/")
# def read_root():
#     return {"message": "hello world"}


@app.get("/api/dates")
async def get_dates():
    response = await fetch_all_dates()
    return response


@app.post("/api/dates", response_model=SchemaDatesResponse)
async def post_dates(date: SchemaDatesInput, db: Session):
    async with aiohttp.ClientSession() as session:
        async with session.get("http://numbersapi.com/"+str(date.month)+"/"+str(date.day)+"/date") as resp:
            description = await resp.text()
    dates_data = SchemaDatesResponse(
        day=date.day, month=date.month, fact=description)
    create_dates(db=db, dates_data=dates_data)
    return dates_data
    # response = await create_todo(todo.dict())
    # if response:
    #     return response
    # raise HTTPException(400,"Something went wrong/ Bad Request")


# @app.put("/api/dates{title }", response_model=SchemaDatesResponse)
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

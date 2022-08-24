from typing import Collection
from fastapi import FastAPI, HTTPException, responses
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware, db
from schema import Dates as SchemaDates
from schema import DatesResponse as SchemaDatesResponse
from model import Dates as ModelDates
import aiohttp
import os
from dotenv import load_dotenv


load_dotenv('.env')

# App Object
app = FastAPI()
origins = ["*"]

# from database import(
#     remove_todo,
#     update_todo,
#     create_todo,
#     fetch_all_todos,
#     fetch_on_todo,

# )


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


@app.get("/")
def read_root():
    return {"message": "hello world"}


@app.get("/api/dates")
async def get_dates():
    pass
    # response = await fetch_all_todos()
    # return response


@app.post("/api/dates", response_model=SchemaDatesResponse)
async def post_dates(date: SchemaDates):
    async with aiohttp.ClientSession() as session:
        async with session.get("http://numbersapi.com/"+str(date.month)+"/"+str(date.day)+"/date") as resp:
            description = await resp.text()
    response = SchemaDatesResponse(
        day=date.day, month=date.month, fact=description)
    return response
    # response = await create_todo(todo.dict())
    # if response:
    #     return response
    # raise HTTPException(400,"Something went wrong/ Bad Request")


@app.put("/api/dates{title }", response_model=SchemaDatesResponse)
async def put_dates(title: str, desc: str):
    # response = await update_todo(title,desc)
    # if response:
    #     return response
    raise HTTPException(404, f"There is no TODO item with this title {title}")


@app.delete("/api/dates/{title}")
async def delete_dates(title):
    # response = await remove_todo(title)
    # if response:
    #     return "successfully deleted todo Item!"
    raise HTTPException(404, f"There is no TODO item with this title {title}")

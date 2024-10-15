from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange

import psycopg2
from  psycopg2.extras import RealDictCursor 
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:

    # Connect to an existing database
    try:
        conn =  psycopg2.connect(host = "localhost", database="fastapi", user="postgres", password="11111111", cursor_factory=RealDictCursor)

        # Open a cursor to perform database operations
        cursor= conn.cursor() 
        print("Success")
        break
    except Exception as error:
        print("Connecting to db failed")
        print("Error: ", error)
        time.sleep(3)


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Hello World"}



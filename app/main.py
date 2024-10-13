from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
from passlib.context import CryptContext
import psycopg2
from  psycopg2.extras import RealDictCursor 
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session


pwd_context = CryptContect(schemes=['bcrypt'], deprecated= "auto")
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

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get('/posts', response_model= List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Post).all()
    
    return posts

@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db),):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    
    #  (post.title, post.content, post.published))

    # new_post = cursor.fetchone()
    # conn.commit()
    # print(new_post)
    
    # a simple way of doing this is using the dict unpack method with (**) as below
    # print(post.dict())
    new_post = models.Post(
        # title=post.title, content=post.content, published=post.published,
        **post.dict()
)
  
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model= schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
  
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=  f"post with id : {id} was not found" )
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)
 
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}", response_model= schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")
    
    post_query.update(updated_post.dict(), synchronize_session = False)
    
    db.commit()

 
    return post_query.first()

@app.post('/users', status_code=status.HTTP_201_CREATED, response_model= schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

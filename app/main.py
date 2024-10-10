from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from  psycopg2.extras import RealDictCursor 
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session







# from psycopg.extras import RealDictCursor


models.Base.metadata.create_all(bind=engine)

app = FastAPI()



class Post(BaseModel):
    title: str
    content: str
    published : bool = True
    # rating : Optional[int] = None  

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


my_posts = [
    {"title" : "first title", "content" : "content 1", "id": 1},
    {"title" : "secondtitle", "content" : "content 2", "id": 2},
]



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

@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return {"data" : posts}



@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Post).all()
    
    return {
        "data" : posts
    }

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post : Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    
    #  (post.title, post.content, post.published))

    # new_post = cursor.fetchone()
    # conn.commit()
    # print(new_post)
    
    # a simple way of doing this is using the dict unpack method with (**) as below
    # print(post.dict())
    new_post = models.Post(
        title=post.title, content=post.content, published=post.published,
        # **post.dict()
)
  
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {
        "data" : new_post
    }
    


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
  
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=  f"post with id : {id} was not found" )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"post with id : {id} was not found"}
    return {"post_detail" : post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)
 
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")
    
    post_query.update(updated_post.dict(), synchronize_session = False)
    
    db.commit()

 
    return {"data" : post_query.first()}

    print(post)


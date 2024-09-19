from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from  psycopg2.extras import RealDictCursor 
import time

# from psycopg.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published : bool = True
    rating : Optional[int] = None  

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


@app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {
        "message" : posts
    }

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post : Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000)
    my_posts.append(post_dict)
    return {
        # "message" : "Another one",
        # "new_post" : f" title : {payload['title']}, content : {payload['content']} "
        "data" : post_dict
    }



@app.get("/posts/{id}")
def get_post(id: int, response : Response):
    post = find_post(id)
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=  f"post with id : {id} was not found" )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"post with id : {id} was not found"}
    return {"post_detail" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")
    my_posts.pop(index)
    return Response(status_code = status.HTTP_204_NO_CONTENT)
    # return {"message" : "post deleted successfully"}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data" : post_dict}

    print(post)


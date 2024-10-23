from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from fastapi.responses import JSONResponse

router = APIRouter(

    # prefex = "/users",
    tags = ['Users']

)


@router.post('/users', status_code=status.HTTP_201_CREATED, response_model= schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    
    # hashing password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"User with id : {id} does not exist")

    return user

@router.get('/userss')
def get_users(db: Session = Depends(get_db)):
 
    posts = db.query(models.User).all()
    
    return posts
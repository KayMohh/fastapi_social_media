from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime, timedelta

from .config import settings
from . import schemas, database, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# OAuth2 schema to extract the token from requests
oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

# Configuration Constants
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Function to create an access token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # Add expiration to token payload

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify the token and return token data
def verify_access_token(token: str, credentials_exception: HTTPException):
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credentials_exception  # Raise exception if user_id is missing

        return schemas.TokenData(id=user_id)  # Return token data
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except JWTError:
        raise credentials_exception  # Catch other JWT-related errors

# Function to get the current user from the token
def get_current_user(
    token: str = Depends(oauth2_schema), 
    db: Session = Depends(database.get_db)
):
    # Exception to raise when credentials are invalid
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # Verify the token and get the user ID from it
    token_data = verify_access_token(token, credentials_exception)

    # Query the user from the database
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if user is None:
        raise credentials_exception  # Raise exception if user not found

    return user

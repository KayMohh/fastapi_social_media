from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY

# ALGORITHM


SECRET_KEY = "VERYLONGKEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token, credientials_exception):
    
    try: 
        payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credientials_exception
        
        token_data = schemas.TokenData(id=id)
    except JWTError as e:
        print(e)
        raise credientials_exception
    

        return token_data

def get_current_user(token = Depends(oauth2_schema)):
   
    credientials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"could not validate credential", headers = {"WW-Authenticate" : "Bearer"})

    return verify_access_token(token, credientials_exception)





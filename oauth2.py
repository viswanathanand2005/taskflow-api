from jose import JWTError,jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os

from tables import User
from connection import get_db
from schemas import TokenData

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

key = os.getenv('SECRET_KEY')
algo = os.getenv('ALGORITHM')
time = int(os.getenv('ACCESS_TIME'))

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now() + timedelta(minutes=time)
    to_encode.update({"exp": expire})

    encoded_token = jwt.encode(to_encode,key=key,algorithm=algo)

    return encoded_token

# Cryptographically checking if a token is valid
def verify_access_token(token: str, credentials_exception):

    try:
        # Getting the original data from the encrypted token
        payload = jwt.decode(token=token,key=key,algorithms=[algo])

        # Obtaining the user_id from the data 
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        
        token_data = TokenData(id=id)
    # Raising an exception for any invalid token
    except JWTError:
        raise credentials_exception
    

    return token_data

def get_current_user(token:str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user')

    token_data = verify_access_token(token,credentials_exception)

    user_id = token_data.id
    user = db.query(User).filter(User.id == user_id).first()
    return user


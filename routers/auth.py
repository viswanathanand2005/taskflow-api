from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from connection import get_db
from oauth2 import create_access_token
from tables import User
from schemas import Token
from utils import verify_password

router = APIRouter(tags=["Authentication"])

@router.post('/login',response_model=Token)
def login(credentials: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    email = credentials.username

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid credentials')
    
    if not verify_password(credentials.password,user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid Credentials')
    
    access_token = create_access_token({"user_id": user.id})
    return{
        "accessToken": access_token,
        "token_type": "bearer"
    }




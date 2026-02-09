from fastapi import Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
from typing import List

from connection import get_db
from tables import User
from schemas import UserInput,UserOutput,UserUpdate
from utils import hash_password

router = APIRouter(
    prefix='/users',
    tags=['User']
)

@router.post('/')
def create_user(user: UserInput,db: Session = Depends(get_db)):
    # Hashing the password
    password_hash = hash_password(user.password)
    try:
        new_user = User(
        name = user.name,
        email = user.email,
        password_hash = password_hash
        )
        db.add(new_user)
        db.commit()
        return {"message": "User Created successfully"}
    except:
        db.rollback()
        raise

@router.get('/all',response_model = List[UserOutput])
def display_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get('/{id}',response_model = UserOutput)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    # Raising an exception for invalid user
    if not user:
        raise HTTPException(status_code=404,detail=f'Not Found, user with {id} is not found')
    
    return user
@router.patch('/{id}')
def update_user(id: int, updates: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    # Raising an exception for invalid user
    if not user:
        raise HTTPException(status_code=404, detail=f'No user with the id: {id} exists')

    # Updating the user details
    db.query(User).filter(User.id == id).update(
        updates.dict(exclude_unset=True),
        synchronize_session=False
    )
    db.commit()
    return {"message": "User updated successfully"}

@router.delete('/{id}')
def delete_user(id: int,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id)
    query = user.first()

    # Raising an exception for invalid user
    if not query:
        raise HTTPException(status_code=404, detail= f'No user with the id: {id}')

    # Deleting the user from the db    
    user.delete(synchronize_session=False)
    db.commit()
    return {"message": "User deleted successfully"}

from fastapi import Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
from typing import List

from connection import get_db
from tables import Tag
from schemas import TagCreate,TagUpdate,TagOutput

router = APIRouter(
    prefix='/tags',
    tags=["Tag"]
)

@router.get('/all',response_model=List[TagOutput])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Tag).all()

@router.get('/{id}',response_model=TagOutput)
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Tag).filter(Tag.id == id)

    # Raising an exception for invalid task
    if not task:
        raise HTTPException(status_code=404,detail=f'Tag with the id: {id} does not exist')
    return task.first()

@router.post('/')
def create_task(tag: TagCreate,db: Session = Depends(get_db)):
    try:
        new_tag = Tag(
            name = tag.name
        )
        db.merge(new_tag)
        db.commit()

        return {"message": "Tag was created successfully"}
    except:
        db.rollback()
        raise

@router.patch('/{id}')
def update_tag(id: int,updates: TagUpdate,db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == id)
    query = tag.first()

    #Raising an exception for invalid task
    if not query:
        raise HTTPException(status_code=404,detail=f'Tag with the id: {id} is not present')
    
    # Updating the task details
    tag.update(
        values=updates.dict(exclude_unset=True),
        synchronize_session=True
    )
    db.commit()
    return {"message": "Tag was updated successfully"}

@router.delete('/{id}')
def delete_tag(id: int,db: Session = Depends(get_db)):

    tag = db.query(Tag).filter(Tag.id == id)
    result = tag.first()

    # Raising an exception for invalid user
    if not result:
        raise HTTPException(status_code=404,detail=f'No user with the id: {id}')
    
    #Deleting the tag details
    tag.delete(synchronize_session=False)
    db.commit()

    return {"message": "User has been deleted"}
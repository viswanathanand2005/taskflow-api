from fastapi import Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
from typing import List

from connection import get_db
from tables import Task
from schemas import TaskCreate,TaskUpdate,TaskOutput
from oauth2 import get_current_user

router = APIRouter(
    prefix='/tasks',
    tags=['Task']
)

@router.get('/all',response_model=List[TaskOutput])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@router.get('/{id}',response_model=TaskOutput)
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id)
    if not task:
        raise HTTPException(status_code=404,detail=f'Task with the id: {id} does not exist')
    return task.first()

@router.post('/')
def create_task(task: TaskCreate,db: Session = Depends(get_db),user_id: int = Depends(get_current_user)):
    try:
        new_task = Task(
            user_id = task.user_id,
            title = task.title,
            description = task.description,
            status = task.status,
            priority = task.priority,
            due_date = task.due_date
        )
        db.merge(new_task)
        db.commit()

        return {"message": "Task was created successfully"}
    except:
        db.rollback()
        raise

@router.patch('/{id}')
def update_task(id: int,updates: TaskUpdate,db: Session = Depends(get_db),user_id: int = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == id)
    query = task.first()

    if not query:
        raise HTTPException(status_code=404,detail=f'Task with the id: {id} is not present')
    task.update(
        values=updates.dict(exclude_unset=True),
        synchronize_session=False
    )
    db.commit()
    return {"message": "Task was updated successfully"}

@router.delete('/{id}')
def delete_task(id: int,db: Session = Depends(get_db),user_id: int = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == id)
    if not task.first():
        raise HTTPException(status_code=404,detail=f'Task with id: {id} does not exist')
    
    task.delete(synchronize_session=False)
    db.commit()
    return {"message": "Task deleted successfully"}

from sqlalchemy import Column,BigInteger,ForeignKey,String,VARCHAR,TEXT,Date,Enum
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from connection import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger,primary_key=True,autoincrement=True)
    name = Column(String(50),nullable=False)
    email = Column(String(100),nullable=False,unique=True)
    password_hash = Column(VARCHAR(255),nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP(timezone=True),server_default=text('CURRENT_TIMESTAMP'),onupdate=text('CURRENT_TIMESTAMP'))

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(BigInteger,primary_key=True,autoincrement=True)
    user_id = Column(BigInteger,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    title = Column(VARCHAR(75),nullable=False)
    description = Column(TEXT)
    status = Column(Enum('to_do','in_progress','done'),server_default='to_do')
    priority = Column(Enum('low','medium','high'),server_default='medium')
    due_date = Column(Date)
    deleted_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP(timezone=True),server_default=text('CURRENT_TIMESTAMP'),onupdate=text('CURRENT_TIMESTAMP'))

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(BigInteger,primary_key=True,index=True,autoincrement=True)
    task_id = Column(BigInteger,ForeignKey('tasks.id',ondelete='CASCADE'),nullable=False)
    name = Column(VARCHAR(100),unique=True,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('CURRENT_TIMESTAMP'))


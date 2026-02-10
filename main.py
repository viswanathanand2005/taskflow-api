from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import uvicorn


from routers import user,task,tag,auth
app = FastAPI(title='Creating a CRUD API with authentication')

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_credentials = True
)

@app.get('/api')
def greet():
    return {"message": "Hello World"}

# Routers
app.include_router(user.router)
app.include_router(task.router)
app.include_router(tag.router)
app.include_router(auth.router)

if __name__ == '__main__':
    uvicorn.run("main:app",host=os.getenv('APP_HOST'),port=int(os.getenv('APP_PORT')),reload=True)


from fastapi import FastAPI

import models
from db import engine
from routers import auth, todos, admin, user

app = FastAPI()

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)
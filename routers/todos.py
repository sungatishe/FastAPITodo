from typing import Annotated
from fastapi import Depends, HTTPException, Path, APIRouter, Request, Form
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse

import models
from models import Todos
from db import SessionLocal
from routers.auth import get_current_user

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    tags=["todos"],
    responses={404: {"description": "Not found"}}
)

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session = Depends(get_db)):
    todos = db.query(Todos).filter(Todos.owner_id == 2).all()

    return templates.TemplateResponse("home.html", {"request": request, "todos": todos})


@router.get("/add-todo", name="addtodo", response_class=HTMLResponse)
async def add_new_todo(request: Request):
    return templates.TemplateResponse("add-todo.html", {"request": request})


@router.post("/add-todo", response_class=HTMLResponse)
async def create_todo(request: Request, title: str = Form(...), description: str = Form(...),
                      priority: str = Form(...), db: Session = Depends(get_db)):
    todo_model = Todos()
    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority
    todo_model.complete = False
    todo_model.owner_id = 2

    db.add(todo_model)
    db.commit()

    return RedirectResponse(url='/todos', status_code=status.HTTP_302_FOUND)


@router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()

    return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo})


@router.post("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo_commit(request: Request, todo_id: int, title: str = Form(...), description: str = Form(...),
                           priority: str = Form(...), db: Session = Depends(get_db)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority

    db.add(todo_model)
    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.get("/delete/{todo_id}", name="delete_todo", response_class=HTMLResponse)
async def delete_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == 2).first()

    print(todo_model)

    if todo_model is None:
        print(f"No todo found with id {todo_id} for owner 2")  # Добавьте это для отладки
        return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.get("/complete/{todo_id}", response_class=HTMLResponse)
async def complete_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    todo_model.complete = not todo_model.complete

    db.add(todo_model)
    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

from typing import Union
from fastapi import FastAPI, HTTPException, Request, Depends
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from supabase_client import supabase_client
from authentication import verify_token

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; replace with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods; you can restrict this if needed
    allow_headers=["*"],  # Allows all headers; you can restrict this if needed
)

class Item(BaseModel):
    title: str
    description: str

class UserSignupSchema(BaseModel):
    email: str
    password: str

# signout: supabase.auth.admin.sign_out(jwt)
# token: str = Depends(verify_token)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/sign_up")
def sign_up(user: UserSignupSchema):
    user = supabase_client.auth.sign_up(
        { "email": user.email, "password": user.password }
    )
    return {
        "token": res.get("access_token"),
        "user": user
    }

@app.post("/sign_in")
def sign_in(user: UserSignupSchema):
    try:
        loged_user = supabase_client.auth.sign_in_with_password({ "email": user.email, "password": user.password })
        print("signed user isss", loged_user.user)
        return {
            "user": loged_user.user,
            "access_token": loged_user.session.access_token
        }
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail="Invalid Credentials",
        )

@app.get("/todo")
def get_todos():
    todos = supabase_client.table("todos").select("*").execute()
    return todos.data

@app.post("/todo")
def add_todo(item: Item):
    print("item isss", item)
    new_todo = (
        supabase_client.table("todos")
        .insert({
            "title": item.title,
            "description": item.description
        })
        .execute()
    )
    return new_todo.data

@app.delete("/todo/{todo_id}")
def delete_todo(todo_id: int):
    deleted_todo = supabase_client.table("todos").delete().eq("id", todo_id).execute()
    if not len(deleted_todo.data):
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted_todo.data


# Handler for generic server errors
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )
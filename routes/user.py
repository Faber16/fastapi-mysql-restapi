from fastapi import APIRouter, Response, status
from config.db import con
from models.user import users
from schemas.user import User
from starlette.status import HTTP_204_NO_CONTENT

from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()


@user.get("/users", response_model= list[User], tags= ["Users"])
def get_users():
    return con.execute(users.select()).fetchall()


@user.post("/users", response_model= User, tags= ["Users"])
def create_users(user: User):
    newUser = {"name": user.name, "email": user.email}
    newUser["password"] = f.encrypt(user.password.encode("utf-8"))
    result = con.execute(users.insert().values(newUser))
    return con.execute(users.select().where(users.c.id == result.lastrowid)).first()


@user.get("/users/{id}", response_model= User, tags= ["Users"])
def get_user(id: str):
    return con.execute(users.select().where(users.c.id == id)).first()


@user.delete("/users/{id}", status_code= status.HTTP_204_NO_CONTENT, tags= ["Users"])
def delete_user(id: str):
    result = con.execute(users.delete().where(users.c.id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)


@user.put("/Users/{id}", response_model= User, tags= ["Users"])
def update_user(id: str, user: User):
    con.execute(users.update().values(name=user.name,
                email=user.email, password=f.encrypt(user.password.encode("utf-8"))
    ).where(users.c.id == id))
    return con.execute(users.select().where(users.c.id == id)).first()

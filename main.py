from fastapi import FastAPI
from routes.user import user

app = FastAPI(
    title= "Example API with FastAPI",
    description= "My first api with FastAPI",
    openapi_tags=[{
        "name" : "Users",
        "description" : "Userts routes"
    }]
)

app.include_router(user)

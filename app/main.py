from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote, recipe, ingredient, user_ingredients
from .routers import shopping_list, favorite_recipes
from .config import settings


#models.Base.metadata.create_all(bind=engine) #pt ca avem alembic

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(recipe.router)
app.include_router(ingredient.router)
app.include_router(user_ingredients.router)
app.include_router(shopping_list.router)
app.include_router(favorite_recipes.router)


@app.get("/")
def root():
    return {"message": "Hello World merge merge!"}

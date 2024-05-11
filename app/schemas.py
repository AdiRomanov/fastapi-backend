from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional

from pydantic.types import conint
import ast


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore


class RecipeBase(BaseModel):
    name: str
    cook_time: int
    ingredients: list[str]
    directions: str

    @validator('ingredients', pre=True)
    def ensure_list(cls, v):
        if isinstance(v, str):
            try:
                # Attempt to evaluate the string to a list
                evaluated = ast.literal_eval(v)
                if not isinstance(evaluated, list):
                    raise ValueError("Ingredients must be a list")
                # Further check to ensure all elements are strings
                if not all(isinstance(item, str) for item in evaluated):
                    raise ValueError("All ingredients must be strings")
                return evaluated
            except (SyntaxError, ValueError):
                raise ValueError("Ingredients must be a valid list of strings")
        return v


class Recipe(RecipeBase):
    id: int

    class Config:
        orm_mode = True

class IngredientBase(BaseModel):
    ingredient: str

class Ingredient(IngredientBase):
    id: int

    class Config:
        orm_mode = True

class UserIngredientBase(BaseModel):
    user_id: int
    ingredient_id: int
    


class UserIngredientCreate(UserIngredientBase):
    pass


class UserIngredient(UserIngredientBase):
    class Config:
        orm_mode = True


class UserIngredientUpdate(BaseModel):
    pass    

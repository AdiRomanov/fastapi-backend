from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/recipes",
    tags=['Recipes']
)

@router.get("/", response_model=List[schemas.Recipe])
def get_recipes(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    recipes = db.query(models.Recipe).filter(
        models.Recipe.name.contains(search)).limit(limit).offset(skip).all()
    return recipes


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Recipe)
def create_recipes(recipe: schemas.RecipeBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_recipe = models.Recipe(**recipe.dict())
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    return new_recipe


@router.get("/{id}", response_model=schemas.Recipe)
def get_recipe(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == id).first()
    return recipe


@router.put("/{id}", response_model=schemas.Recipe)
def update_recipe(id: int, recipe: schemas.RecipeBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    db.query(models.Recipe).filter(models.Recipe.id == id).update(recipe.dict())
    db.commit()
    return db.query(models.Recipe).filter(models.Recipe.id == id).first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    db.query(models.Recipe).filter(models.Recipe.id == id).delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)




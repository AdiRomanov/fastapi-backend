from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/ingredients",
    tags=['Ingredients']
)

@router.get("/", response_model=List[schemas.Ingredient])
def get_ingredients(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 1000000, skip: int = 0, search: Optional[str] = ""):
    ingredients = db.query(models.Ingredient).filter(
        models.Ingredient.ingredient.contains(search)).limit(limit).offset(skip).all()
    return ingredients

@router.get("/ingredient-by-name/{name}", response_model=schemas.Ingredient)
def get_ingredient_by_name(name: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    ingredient = db.query(models.Ingredient).filter(models.Ingredient.ingredient == name).first()
    return ingredient

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Ingredient)
def create_ingredient(ingredient: schemas.IngredientBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_ingredient = models.Ingredient(**ingredient.dict())
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)

    return new_ingredient


@router.get("/{id}", response_model=schemas.Ingredient)
def get_ingredient(id: int, db: Session = Depends(get_db)   ):
    ingredient = db.query(models.Ingredient).filter(models.Ingredient.id == id).first()
    return ingredient


@router.put("/{id}", response_model=schemas.Ingredient)
def update_ingredient(id: int, ingredient: schemas.IngredientBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    db.query(models.Ingredient).filter(models.Ingredient.id == id).update(ingredient.dict())
    db.commit()
    return db.query(models.Ingredient).filter(models.Ingredient.id == id).first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    db.query(models.Ingredient).filter(models.Ingredient.id == id).delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


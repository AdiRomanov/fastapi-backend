from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/user-ingredients",
    tags=['User Ingredients']
)

@router.get("/", response_model=List[schemas.UserIngredient])
def get_user_ingredients(db: Session = Depends(get_db), limit: int = 10000, skip: int = 0):
    user_ingredients = db.query(models.UserIngredient).limit(limit).offset(skip).all()
    return user_ingredients


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserIngredient)
def create_user_ingredient(user_ingredient: schemas.UserIngredientCreate, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    
    entity = db.query(models.UserIngredient).filter(
        models.UserIngredient.user_id == current_user.id,
        models.UserIngredient.ingredient_id == user_ingredient.ingredient_id
    ).first()

    if entity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ingredient already exists for this user.")

    new_user_ingredient = models.UserIngredient(**user_ingredient.dict())
    db.add(new_user_ingredient)
    db.commit()
    db.refresh(new_user_ingredient)

    return new_user_ingredient


@router.get('/{id}', response_model=List[schemas.UserIngredient])
def get_user_ingredient(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):

    if id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    user_ingredient = db.query(models.UserIngredient).filter(models.UserIngredient.user_id == id).all()
    if not user_ingredient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"UserIngredient with id: {id} does not exist")

    return user_ingredient




@router.put("/{id}", response_model=schemas.UserIngredient)
def update_user_ingredient(id: int, user_ingredient: schemas.UserIngredientUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    db.query(models.UserIngredient).filter(models.UserIngredient.id == id).update(user_ingredient.dict())
    db.commit()
    return db.query(models.UserIngredient).filter(models.UserIngredient.id == id).first()



@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_ingredient(ingredient_id: int, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    
    user_ingredient = db.query(models.UserIngredient).filter(
        models.UserIngredient.user_id == current_user.id,
        models.UserIngredient.ingredient_id == ingredient_id
    ).first()

    if not user_ingredient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found for this user.")

    db.delete(user_ingredient)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


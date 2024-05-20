from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/favorite-recipes",
    tags=['Favorite Recipes']
)

@router.get("/", response_model=List[schemas.FavoriteRecipe])
def get_favorite_recipes(db: Session = Depends(get_db), limit: int = 10000, skip: int = 0):
    favorite_recipes = db.query(models.FavoriteRecipe).limit(limit).offset(skip).all()
    return favorite_recipes

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.FavoriteRecipe)
def create_favorite_recipe(favorite_recipe: schemas.FavoriteRecipeCreate, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    
    entity = db.query(models.FavoriteRecipe).filter(
        models.FavoriteRecipe.user_id == current_user.id,
        models.FavoriteRecipe.recipe_id == favorite_recipe.recipe_id
    ).first()

    if entity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Recipe already exists in favorites for this user.")

    new_favorite_recipe = models.FavoriteRecipe(**favorite_recipe.dict())
    db.add(new_favorite_recipe)
    db.commit()
    db.refresh(new_favorite_recipe)

    return new_favorite_recipe

@router.get('/{user_id}', response_model=List[schemas.FavoriteRecipe])
def get_favorite_recipe(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):

    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    favorite_recipe = db.query(models.FavoriteRecipe).filter(models.FavoriteRecipe.user_id == user_id).all()
    if not favorite_recipe:
        return []

    return favorite_recipe

@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite_recipe(recipe_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    db.query(models.FavoriteRecipe).filter(models.FavoriteRecipe.recipe_id == recipe_id,
                                           models.FavoriteRecipe.user_id == current_user.id).delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get('/{recipe_id}/{user_id}', status_code=status.HTTP_200_OK)
def check_favorite_recipe(user_id: int, recipe_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):
    favorite_recipe = db.query(models.FavoriteRecipe).filter(models.FavoriteRecipe.user_id == user_id, models.FavoriteRecipe.recipe_id == recipe_id).first()
    if favorite_recipe:
        return True
    return False
import ast
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
def get_recipes(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 1000000, skip: int = 0, search: Optional[str] = ""):
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


@router.get("/recipe-matches/")
def get_recipe_matches(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Fetch the user ingredients from the database
    user_ingredients = db.query(models.UserIngredient).filter(models.UserIngredient.user_id == current_user.id).all()
    user_ingredient_list = []

    if not user_ingredients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No ingredients found for the user")
    
    for user_ingredient in user_ingredients:
        user_ingredient_list.append(db.query(models.Ingredient).filter(models.Ingredient.id == user_ingredient.ingredient_id).first().ingredient)

    # print(user_ingredient_list)

    # Call the matching logic function
    try:
        matched_recipes = match_recipes(user_ingredient_list, db)
        return {"recipes": matched_recipes}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def match_recipes(user_ingredients, db):
    recipes = db.query(models.Recipe).all()  # Fetch all recipes
    recipe_scores = []
    for recipe in recipes:
        
        recipe_ingredients = set(ast.literal_eval(recipe.ingredients)) # convert string to list
        user_ingredients_set = set(user_ingredients)
        common_ingredients = recipe_ingredients.intersection(user_ingredients_set)
        match_percentage = len(common_ingredients) / len(recipe_ingredients) if recipe_ingredients else 0
        match_percentage = round(match_percentage * 100, 2)
        if match_percentage >= 30: # Only consider recipes with at least 30% match
            recipe_scores.append((recipe, match_percentage))
        

    # Sort by match percentage in descending order
    recipe_scores.sort(key=lambda x: x[1], reverse=True)
    return [{"id": recipe.id,"name": recipe.name, "match_percentage": perc} for recipe, perc in recipe_scores]

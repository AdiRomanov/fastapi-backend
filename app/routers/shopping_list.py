from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/shopping-list",
    tags=['Shopping List']
)

@router.get("/", response_model=List[schemas.ShoppingList])
def get_shopping_list(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10000, skip: int = 0):
    shopping_list = db.query(models.ShoppingList).filter(models.ShoppingList.user_id == current_user.id).limit(limit).offset(skip).all()
    return shopping_list


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShoppingList)
def create_shopping_list(shopping_list: schemas.ShoppingListCreate, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    entity = db.query(models.UserIngredient).filter(
        models.ShoppingList.user_id == current_user.id,
        models.ShoppingList.ingredient_id == shopping_list.ingredient_id
    ).first()
    
    if entity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ingredient already exists for this user.")

    new_shopping_list = models.ShoppingList(**shopping_list.dict())
    db.add(new_shopping_list)
    db.commit()
    db.refresh(new_shopping_list)
 
    return new_shopping_list


@router.get('/{id}', response_model=List[schemas.ShoppingList])
def get_shopping_list_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):

    shopping_list = db.query(models.ShoppingList).filter(models.ShoppingList.user_id == current_user.id).all()
    if not shopping_list:
        return []

    return shopping_list


@router.put("/{id}", response_model=schemas.ShoppingList)
def update_shopping_list(id: int, shopping_list: schemas.ShoppingListUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    db.query(models.ShoppingList).filter(models.ShoppingList.id == id).update(shopping_list.dict())
    db.commit()
    return db.query(models.ShoppingList).filter(models.ShoppingList.id == id).first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shopping_list(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    db.query(models.ShoppingList).filter(models.ShoppingList.user_id == current_user.id,
                                         models.ShoppingList.ingredient_id == id).delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
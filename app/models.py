from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="posts")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    posts = relationship("Post", back_populates="owner")
    ingredients = relationship('Ingredient', secondary='user_ingredients', back_populates='users')
    shopping_list = relationship('ShoppingList', back_populates='user')
    favorite_recipes = relationship("FavoriteRecipe", back_populates="user")

class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    ingredient = Column(String, nullable=False)

    users = relationship('User', secondary='user_ingredients', back_populates='ingredients')
    shopping_list_items = relationship('ShoppingList', back_populates='ingredient')

class UserIngredient(Base):
    __tablename__ = 'user_ingredients'
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id', ondelete='CASCADE'), primary_key=True)
    
    # No need to define back_populates here if it's just a simple association table without extra logic
    # Instead, just ensure that the secondary table in User and Ingredient is correctly pointed to this table

class Recipe(Base):
    __tablename__ = 'recipes'
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    cook_time = Column(Integer, nullable=False)
    ingredients = Column(JSONB, nullable=False)
    directions = Column(String, nullable=False)

    favorite_recipes_id = relationship("FavoriteRecipe", back_populates="recipe")


class ShoppingList(Base):
    __tablename__ = 'shopping_lists'
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id', ondelete='CASCADE'), primary_key=True)

    user = relationship('User', back_populates='shopping_list')
    ingredient = relationship('Ingredient', back_populates='shopping_list_items')


class FavoriteRecipe(Base):
    __tablename__ = 'favorite_recipes'
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id', ondelete='CASCADE'), primary_key=True)

    user = relationship("User", back_populates="favorite_recipes")
    recipe = relationship("Recipe", back_populates="favorite_recipes_id")
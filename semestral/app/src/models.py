from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    value = db.Column(db.Float())
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    foods = db.relationship('Food',secondary='food_category',back_populates='categories')

class Food(db.Model):
    __tablename__ = "foods"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True) 
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    categories = db.relationship('Category', secondary = 'food_category',back_populates = 'foods')

class FoodCategory(db.Model):
    __tablename__ = "food_category"
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    foods = db.relationship('Food')
    categories = db.relationship('Category')
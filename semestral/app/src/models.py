from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import datetime


class Category(db.Model):
    """
    Database model for category
    """
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    value = db.Column(db.Float())
    immediateValue = db.Column(db.Float())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    foods = db.relationship(
        'Food', secondary='food_category', back_populates='categories')


class Food(db.Model):
    """
    Database model for food
    """
    __tablename__ = "foods"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    lastServed = db.Column(db.Date, default=datetime.date(2021, 12, 10))
    value = db.Column(db.Float())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    categories = db.relationship(
        'Category', secondary='food_category', back_populates='foods')
    menus = db.relationship('Menu', secondary='food_menu',
                            back_populates='foods', lazy='dynamic')


class FoodCategory(db.Model):
    """
    Database model for m to n relation table between food and category
    """
    __tablename__ = "food_category"
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))


class User(db.Model, UserMixin):
    """
    Database model for user
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    foods = db.relationship('Food')
    categories = db.relationship('Category')
    menus = db.relationship('Menu')


class FoodMenu(db.Model):
    """
    Database model for m to n relation table between food and menu
    """
    __tablename__ = "food_menu"
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'))
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'))


class Menu(db.Model):
    """
    Database model for menu
    """
    __tablename__ = "menus"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.Date)
    foods = db.relationship(
        'Food', secondary='food_menu', back_populates='menus')
    __table_args__ = (db.UniqueConstraint(
        'user_id', 'date', name='_menu_user_date_uc'),)

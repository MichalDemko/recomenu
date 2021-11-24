from os import name
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from flask_sqlalchemy.model import camel_to_snake_case
from .models import Category, Food
from . import db
import json

views = Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        food = request.form.get('food')

        if len(food) < 1:
            flash('Food is short!!',category='error')
        else:
            categoriesId= (int(x.split('_')[-1]) for x in request.form.keys() if x.startswith('category_'))
            categories = [Category.query.get(x) for x in categoriesId]
            if not categories:
                flash('No categories selected',category='error')
                return render_template("home.html", user=current_user)
            new_food = Food(data=food, user_id=current_user.id, categories=categories)
            db.session.add(new_food)
            db.session.commit()
            flash('Food added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-food', methods=['POST'])
def delete_food():
    food = json.loads(request.data)
    foodId = food['foodId']
    food = Food.query.get(foodId)
    if food:
        if food.user_id == current_user.id:
            db.session.delete(food)
            db.session.commit()
    
    return jsonify({})

@views.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'POST':
        category = request.form.get('category')

        if len(category) < 1:
            flash('Category is short!!',category='error')
        else:
            new_category = Category(name=category, value=1. , user_id=current_user.id)
            db.session.add(new_category)
            db.session.commit()
            flash('Food category added!', category='success')

    return render_template("settings.html", user=current_user)



@views.route('/delete-category', methods=['POST'])
def delete_category():
    category = json.loads(request.data)
    categoryId = category['categoryId']
    category = Category.query.get(categoryId)
    if category:
        if category.user_id == current_user.id:
            db.session.delete(category)
            db.session.commit()
    
    return jsonify({})
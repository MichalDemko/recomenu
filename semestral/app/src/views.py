import os
from .config import configuration
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy.sql.elements import and_
from .models import Category, Food, Menu
from . import db
from .recommend import get_food_list, alter_values_add, alter_values_remove, filter_food_list
from .build import build_categories, allowed_file
from .menuview import get_menu
from datetime import date, datetime
from werkzeug.utils import secure_filename
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
            new_food = Food(name=food, user_id=current_user.id, categories=categories)
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

@views.route('/menu',methods=['GET','POST'])
@login_required
def menu():
    foodlist = get_food_list(current_user, date(2021,12,28))
    mydate = request.args.get('date')
    categories_checked = request.args.get('categories')
    if mydate:
        mydate = datetime.strptime(mydate, "%Y-%m-%d").date()
        menu = get_menu(current_user,mydate.isocalendar().year,mydate.isocalendar().week)
    else:
        menu = get_menu(current_user)

    if categories_checked:
        print("CATEGORIES")
        print(categories_checked)
        categories_checked = categories_checked.split(',')
        foodlist = filter_food_list(foodlist, categories_checked)
        categories = build_categories(current_user, categories_checked)
    else:
        categories = build_categories(current_user)

    return render_template("menu.html", user = current_user, foodlist = foodlist, menu = menu, categories = categories)


@views.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'POST':
        if 'categoryform' in request.form:
            category = request.form.get('category')
            value = request.form.get('categoryvalue')

            if len(category) < 1:
                flash('Category is short!!',category='error')
            else:
                print(category,value)
                new_category = Category(name = category, value = value, immediateValue = 10, user_id = current_user.id)
                db.session.add(new_category)
                db.session.commit()
                flash('Food category added!', category='success')
        else:
            print(request.files)
            if 'file' not in request.files :
                flash('No file part', category = 'error')
                return render_template("settings.html", user=current_user)

            file = request.files['file']

            if file.filename == '':
                flash('No selected file',category='error')
                return render_template("settings.html", user=current_user)
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(configuration.UPLOAD_FOLDER, filename))
                flash('File imported!!', category= 'success')

    return render_template("settings.html", user=current_user)


@views.route('/add-to-menu', methods=['POST'])
def add_to_menu():
    data = json.loads(request.data)
    print(data)
    menu = db.session.query(Menu).filter(
        and_(Menu.date == data['date'], Menu.user_id == current_user.id)
    ).first()
    food = Food.query.get(data['foodId'])
    date = datetime.strptime(data['date'], "%Y-%m-%d").date()
    if menu:
        if food in menu.foods:
            flash('Food is in the menu for that day!',category='error')
            return jsonify({})
        alter_values_add(food,date)
        menu.foods.append(food)
        db.session.commit()
    else:
        print("create menu")
        print(datetime.strptime(data['date'], "%Y-%m-%d").date())
        newmenu= Menu(user_id = current_user.id, 
                      date = date)
        alter_values_add(food,date)
        newmenu.foods.append(food)
        db.session.add(newmenu)
        db.session.commit()
    return jsonify({})


@views.route('/delete-from-menu', methods=['POST'])
def delete_from_menu():
    data = json.loads(request.data)
    food = Food.query.get(data['food_id'])
    menu = Menu.query.get(data['menu_id'])
    menu.foods.remove(food)
    db.session.commit()
    alter_values_remove(food)
    return jsonify({})


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


@views.route('/update-category', methods=['POST'])
def update_category():
    updateData = json.loads(request.data)
    categoryId = updateData['categoryId']
    category = Category.query.get(categoryId)
    if category:
        if category.user_id == current_user.id:
            category.value = updateData['value']
            db.session.commit()
    
    return jsonify({})
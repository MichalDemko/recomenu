from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from flask_sqlalchemy.model import camel_to_snake_case
from .models import Food
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
            new_food = Food(data=food, user_id=current_user.id)
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
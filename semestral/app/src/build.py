from os import name
from pandas.core.frame import DataFrame
from sqlalchemy.sql.elements import and_
from .config import configuration
from .models import Category, Food
from . import db
from datetime import datetime
import pandas as pd

def build_categories(user, showCategories: list = None) -> dict:
    categories = { cat.id : {'checked' : 0, 'name': cat.name } for cat in user.categories}
    print(showCategories)
    if showCategories != None:
        for x in showCategories:
            categories[int(x)]['checked'] = 1
    print(categories)
    return categories


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in configuration.ALLOWED_EXTENSIONS


def import_file_to_database(user, path) -> bool:
    print(path)
    file = pd.read_csv(path, sep=';')
    print(file)
    parse_dataframe(user, file)
    return True


def parse_dataframe(user, df : DataFrame) -> bool:
    if not check_dataframe(df):
        return False

    parse_categories(user, df)
    parse_foods(user,df)
    return True


def parse_foods(user, df : DataFrame):
    labels = df.keys()
    for index, row in df.iterrows():
        food = Food(name = row['name'], user_id = user.id, lastServed = datetime.strptime(row['lastserved'], "%Y-%m-%d").date())
        for category in labels:
            if category not in configuration.IMPORT_LABELS_NOT_CATEGORY:
                if row[category] == 1:
                    cat = db.session.query(Category).filter(and_(Category.name == category, Category.user_id == user.id)).first()
                    food.categories.append(cat)
        db.session.add(food)
        db.session.commit()
    return

def parse_categories(user, df : DataFrame):
    control = False
    categories = df.keys()
    for category in categories:
        if category not in configuration.IMPORT_LABELS_NOT_CATEGORY:
            for userCategory in user.categories:
                if category == userCategory.name:
                    control = True

            if not control:
                new_category = Category(name = category, 
                                        value = configuration.CATEGORIES_DEFAULT_IMPORT_VALUE,
                                        immediateValue = configuration.CATEGORIES_DEFAULT_IMPORT_IMMEDIATEVALUE,
                                        user_id = user.id)
                db.session.add(new_category)
                db.session.commit()
    return

def check_dataframe(df : DataFrame) -> bool:
    categories = df.keys()
    if ('name' not in categories) or ('lastserved' not in categories) or ('desc' not in categories) or (categories.size <= 3):
        return False
    return True
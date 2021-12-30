from os import name

from sqlalchemy.sql.expression import asc, desc
from . import db
from .models import Category, Food, Menu
import pandas as pd
import numpy as np
from datetime import date

def get_food_list(user, date) -> dict:
    dataframe = get_correct_dataframe(user, date)
    sortedListofID = dataframe.sort_values('value',axis = 0, ascending = False).index.tolist()
    return build_dict(sortedListofID)


def build_dict(idList: list) -> dict:
    return dict([ make_dict_keyval(k) for k in idList])


def make_dict_keyval(key: int):
    food = Food.query.get(key)
    value = { "name" : food.name,
              "categories" : [(x.id,x.name) for x in food.categories] }
    return (key,value)


def get_correct_dataframe(user, date) -> pd.DataFrame:
    foods = pd.read_sql(f"select * from foods where user_id = {user.id}",db.engine).drop(['date','user_id'],axis='columns')['id']
    categories = pd.read_sql(f"select * from categories where user_id = {user.id}",db.engine)['id']
    foods = pd.DataFrame(foods)
    
    matrix = foods.join(pd.DataFrame(
        [[0. for x in categories.tolist()]],
        index = foods.index,
        columns = categories.tolist()
    ))
    matrix['date_value'] = 0
    computedMatrix = compute_value(create_matrix(user,matrix,date), create_scalar(categories))

    return computedMatrix


def create_matrix(user, emptyDF: pd.DataFrame, date) -> pd.DataFrame:
    builtDF = emptyDF.set_index('id')
    for food in user.foods:
        builtDF.at[food.id, "date_value"] = (date - food.lastServed).days
        for category in food.categories:
            builtDF.at[food.id, category.id ] = 1
    return  builtDF


def create_scalar(categoriesSeries: pd.Series) -> pd.DataFrame:
    myColumns = categoriesSeries.tolist()
    myValues = [Category.query.get(x).value * Category.query.get(x).immediateValue for x in myColumns]
    df = pd.DataFrame([myValues], columns = myColumns)
    df['date_value'] = 0.5
    return df


def compute_value(dataMatrix: pd.DataFrame, kernel: pd.DataFrame) -> pd.DataFrame:

    if dataMatrix.columns.tolist() != kernel.columns.tolist():
        print("CHYBA")
        return pd.DataFrame(columns=['value'])

    index = dataMatrix.index.tolist()
    result = np.sum(dataMatrix.to_numpy() * kernel.to_numpy(),axis=1)

    return pd.DataFrame(result, index = index, columns=['value'])


def alter_values_add(food: Food, date: date):
    for category in food.categories:
        category.immediateValue *= 0.5
        db.session.commit()
    food.lastServed = date
    db.session.commit()
    return

def alter_values_remove(food: Food):
    for category in food.categories:
        category.immediateValue *= 1.2
        db.session.commit()
    entity = food.menus.order_by(desc(Menu.date)).first()
    if entity:
        food.lastServed = entity.date
        db.session.commit()
    else:
        food.lastServed = date(2021,12,10)
        db.session.commit()
    return

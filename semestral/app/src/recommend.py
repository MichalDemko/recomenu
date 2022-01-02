from os import name

from sqlalchemy.sql.expression import asc, desc, select
from sqlalchemy.sql.functions import user
from . import db
from .models import Category, Food, Menu
import pandas as pd
import numpy as np
from datetime import date


def get_food_list(user, date) -> dict:
    """
    Returns sorted dictionary of user's foods
    :param user: current user of the app
    :param date: date to use
    :returns: sorted dictionary of user's foods
    """
    dataframe = get_correct_dataframe(user, date)
    sortedListofID = dataframe.sort_values(
        'value', axis=0, ascending=False).index.tolist()
    return build_dict(sortedListofID)


def build_dict(idList: list) -> dict:
    """
    Creates dictionary of foods from given list
    :param idList: sorted list of ids of foods
    :returns: correct dictionary
    """
    return dict([make_dict_keyval(k) for k in idList])


def make_dict_keyval(key: int):
    """
    Creates json like structure from food in database
    :param key: id of food in database
    :returns: key,value pair 
    """
    food = Food.query.get(key)
    value = {"name": food.name,
             "categories": [(x.id, x.name) for x in food.categories]}
    return (key, value)


def get_correct_dataframe(user, date) -> pd.DataFrame:
    """
    Creates dataframe of foods
    :param user: current user of the app
    :param date: date to use
    :returns: dataframe of user foods with correct recommendation values
    """
    foods = pd.read_sql(f"select * from foods where user_id = {user.id}", db.engine).drop(
        ['date', 'user_id'], axis='columns')['id']
    categories = pd.read_sql(
        f"select * from categories where user_id = {user.id}", db.engine)['id']
    foods = pd.DataFrame(foods)

    matrix = foods.join(pd.DataFrame(
        [[0. for x in categories.tolist()]],
        index=foods.index,
        columns=categories.tolist()
    ))
    matrix['date_value'] = 0
    computedMatrix = compute_value(create_matrix(
        user, matrix, date), create_scalar(categories))

    return computedMatrix


def create_matrix(user, emptyDF: pd.DataFrame, date) -> pd.DataFrame:
    """
    Creates dataframe with row values indicating food containing categories
    :param user: current user of the app
    :param emptyDF: correct dataframe with dummy values 
    :param date: date to use
    :returns: dataframe with correct values
    """
    builtDF = emptyDF.set_index('id')
    for food in user.foods:
        builtDF.at[food.id, "date_value"] = (date - food.lastServed).days
        for category in food.categories:
            builtDF.at[food.id, category.id] = 1
    return builtDF


def create_scalar(categoriesSeries: pd.Series) -> pd.DataFrame:
    """
    Creates dataframe with one row containing category values for recommendation
    :param categoriesSeries: categories
    :returns: correct dataframe
    """
    myColumns = categoriesSeries.tolist()
    myValues = [Category.query.get(
        x).value * Category.query.get(x).immediateValue for x in myColumns]
    df = pd.DataFrame([myValues], columns=myColumns)
    df['date_value'] = 0.5
    return df


def compute_value(dataMatrix: pd.DataFrame, kernel: pd.DataFrame) -> pd.DataFrame:
    """
    Computes dataframe with one column containing recommendation values
    :param dataMatrix: dataframe serving as data for convolution
    :param kernel: dataframe serving as kernel for convolution
    :returns: dataframe witch correct values
    """
    if dataMatrix.columns.tolist() != kernel.columns.tolist():
        print("CHYBA")
        return pd.DataFrame(columns=['value'])

    index = dataMatrix.index.tolist()
    result = np.sum(dataMatrix.to_numpy() * kernel.to_numpy(), axis=1)

    return pd.DataFrame(result, index=index, columns=['value'])


def alter_values_add(food: Food, date: date):
    """
    Recalculates recommendation values for each category
    :param food: food used to calculate
    :param date: date used for food
    """
    localset = set()
    for category in food.categories:
        category.immediateValue *= 0.8
        localset.add(category.id)
        db.session.commit()
    qry = db.session.query(Category).filter(Category.user_id == food.user_id)
    for category in qry:
        if category.id not in localset:
            category.immediateValue *= 1.1
            db.session.commit()
    food.lastServed = date
    db.session.commit()
    return


def alter_values_remove(food: Food):
    """
    Recalculates recommendation values for each category after removing from menu
    :param food: food used to calculate
    """
    localset = set()
    for category in food.categories:
        category.immediateValue *= 1.2
        localset.add(category.id)
        db.session.commit()
    entity = food.menus.order_by(desc(Menu.date)).first()

    qry = db.session.query(Category).filter(Category.user_id == food.user_id)
    for category in qry:
        if category.id not in localset:
            category.immediateValue *= 0.8
            db.session.commit()

    if entity:
        food.lastServed = entity.date
        db.session.commit()
    else:
        food.lastServed = date(2021, 12, 10)
        db.session.commit()
    return


def filter_food_list(foodlist: dict, categories: list) -> dict:
    """
    Filters food list with categories
    :param foodList: original food list
    :param categories: categories we want to be contained in returned foods
    :returns: filtered dict of foods
    """
    newlist = {}
    cattuple = set([int(x) for x in categories])
    for food in foodlist:
        unzip = zip(*foodlist[food]['categories'])
        if (cattuple.issubset(set(list(unzip)[0]))):
            newlist[food] = foodlist[food]
    return newlist

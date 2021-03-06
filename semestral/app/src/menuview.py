from sqlalchemy.sql.elements import and_
from sqlalchemy.sql.expression import desc
from . import db
from .models import Category, Food, Menu
import datetime as dt
import pandas as pd
import calendar


def get_menu(user, year: int = None, weekNumber: int = None) -> dict:
    """
    Returns menu for given year and week
    :param user: user
    :param year: number of year
    :param weekNumber: number of week
    :returns: dictionary representing menu
    """
    if year is None and weekNumber is None:
        return select_week(user, dt.date.today().isocalendar().year, dt.date.today().isocalendar().week)
    return select_week(user, year, weekNumber)


def select_week(user, year: int, weekNumber: int) -> dict:
    """
    Returns menu for given year and week
    :param user: user
    :param year: number of year
    :param weekNumber: number of week
    :returns: dictionary representing menu
    """
    datefrom = dt.datetime.strptime(
        f"{year}-{weekNumber}-1", "%Y-%W-%w").date()
    dateto = dt.datetime.strptime(f"{year}-{weekNumber}-0", "%Y-%W-%w").date()
    qry = db.session.query(Menu).filter(
        and_(Menu.date >= datefrom, Menu.date <=
             dateto, Menu.user_id == user.id)
    ).order_by(
        desc(Menu.date)
    )
    week = {}
    for i in range(7):
        date = (datefrom + dt.timedelta(days=i))
        menu = qry.filter(Menu.date == date).first()
        if menu is None:
            week[calendar.day_name[date.weekday()]] = {'menu_id': None,
                                                       'date': date,
                                                       'nextweek': date + dt.timedelta(days=7),
                                                       'beforeweek': date - dt.timedelta(days=7),
                                                       'foods': []}
        else:
            week[calendar.day_name[date.weekday()]] = {'menu_id': menu.id,
                                                       'date': date,
                                                       'nextweek': date + dt.timedelta(days=7),
                                                       'beforeweek': date - dt.timedelta(days=7),
                                                       'foods': [(x.id, x.name) for x in menu.foods]}
    return week

from sqlalchemy.sql.elements import and_
from sqlalchemy.sql.expression import desc
from . import db
from .models import Category, Food, Menu
import datetime as dt
import pandas as pd
import calendar

def get_menu(user, year: int = None, weekNumber: int = None) -> dict:
    if year == None and weekNumber == None:
        return select_week(user, dt.date.today().isocalendar().year, dt.date.today().isocalendar().week)
    return select_week(user, year, weekNumber)


def select_week(user, year: int, weekNumber: int) -> dict:

    datefrom = dt.datetime.strptime( f"{year}-{weekNumber}-1", "%Y-%W-%w").date()
    dateto = dt.datetime.strptime( f"{year}-{weekNumber}-0", "%Y-%W-%w").date()
    qry = db.session.query(Menu).filter(
        and_(Menu.date >= datefrom, Menu.date <= dateto, Menu.user_id == user.id)
    ).order_by(
        desc(Menu.date)
    )
    week = {}
    print("Query:")
    for i in range(7):
        date = (datefrom + dt.timedelta(days=i))
        menu = qry.filter(Menu.date == date).first()
        if menu is None:
            week[ calendar.day_name[date.weekday() ] ] = {'menu_id': None, 
                                                          'date': date,
                                                          'nextweek': date+dt.timedelta(days=7),
                                                          'beforeweek': date-dt.timedelta(days=7),
                                                          'foods': []}
        else:
            week[ calendar.day_name[date.weekday() ] ] = {'menu_id': menu.id, 
                                                          'date': date,
                                                          'nextweek': date+dt.timedelta(days=7),
                                                          'beforeweek': date-dt.timedelta(days=7),
                                                          'foods': [(x.id,x.name) for x in menu.foods]}
    print(week)
    return week
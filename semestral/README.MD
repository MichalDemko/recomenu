# Continual Menu web app - Semestral work

Project created as a semestral work for BI-PYT course. Specification of project topic in `demkomic.pdf`

## Dependencies

To instal all dependencies used in this project run
```
pip install -r requirements.txt
```

## How to run

When you have downloaded the dependencies, run `main.py` to start the web app

```
semestral> python3 app/main.py 
```

Application should run on 

```
http://localhost:5000
```

### About

This web app has very simple user interface. To use the features you are required to sign up for the page (just localy).

After logging in you can create your own food categories and after that foods with those created categories. `Home` page is reserved for the list of every food. `Menu` page is for creating menus for different days of the weeks and different weeks. `Settings` is used for adding categories and category weight.

For testing purposes you can also use file import on `settings` page with pre-created testfile `app/src/test/tables/testimport.csv` which creates basic lists of categories and foods for you to experiment with.
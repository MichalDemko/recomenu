from .config import configuration


def build_categories(user, showCategories: list = None) -> dict:
    categories = { cat.id : {'checked' : 0, 'name': cat.name } for cat in user.categories}
    print(showCategories)
    if showCategories != None:
        for x in showCategories:
            print(x)
            type(x)
            categories[int(x)]['checked'] = 1
    print(categories)
    return categories


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in configuration.ALLOWED_EXTENSIONS
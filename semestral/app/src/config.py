from os.path import join, dirname, realpath


class configuration():
    """
    Class representing configuration values
    """
    UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'csv'}
    IMPORT_LABELS_NOT_CATEGORY = ('name','desc','lastserved')
    CATEGORIES_DEFAULT_IMPORT_VALUE = 0.5
    CATEGORIES_DEFAULT_IMPORT_IMMEDIATEVALUE = 10
from os.path import join, dirname, realpath


class configuration():
    UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'csv'}
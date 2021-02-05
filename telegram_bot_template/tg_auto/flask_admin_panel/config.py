from ..config import DATABASE, DRIVER, USER, PASSWORD, HOST, DATABASE_NAME, WEBHOOK_HOST, SECRET_KEY_2

RELOAD_REQUEST_PATH = f'{WEBHOOK_HOST}/{SECRET_KEY_2}'

class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #... ://user:password@server/database

    SQLALCHEMY_DATABASE_URI = f'{DATABASE}+{DRIVER}://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}'


    SECRET_KEY = 'something very secret'
    
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'

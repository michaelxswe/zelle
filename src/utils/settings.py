from dotenv import dotenv_values

settings = dotenv_values('.env')

SECRET_KEY = settings['SECRET_KEY']
ALGORITHM = settings['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings['ACCESS_TOKEN_EXPIRE_MINUTES'])
DATABASE_URL = settings['DATABASE_URL']
PASSWORD = settings['PASSWORD']
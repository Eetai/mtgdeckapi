import os

# You need to replace the next values with the appropriate values for your configuration
basedir = os.path.abspath((__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgresql://localhost/mtgapi"

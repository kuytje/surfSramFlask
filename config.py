from os import environ, path, urandom

from flask.cli import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, "config/sramPython.conf"))

class Config(object):
    CLIENT_ID = environ.get('CLIENT_ID') or "APP-B391E9BD-31C5-402A-A774-43F37055B6FB"
    CLIENT_SECRET = environ.get('CLIENT_SECRET') or "***"
    SECRET_KEY = environ.get('SECRET_KEY') or urandom(24)
    DOTWELLKNOWN = environ.get('DOTWELLKNOWN') or "https://proxy.sram.surf.nl/.well-known/openid-configuration"
    REDIRECT_URI = environ.get('REDIRECT_URI') or "http://localhost:8084/authorized/"
    SERVER_NAME = environ.get('SERVER_NAME') or "localhost:8084"

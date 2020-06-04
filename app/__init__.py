from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel
from flask_login import LoginManager
from flask_ldapconn import LDAPConn
from werkzeug import datastructures

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ldap = LDAPConn(app)
babel = Babel(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

@babel.localeselector
def get_locale():
    list_languages = []
    for x in request.accept_languages:
        if 'ca-valencia' in x[0]:
            x = ('ca_ES_valencia',x[1])
        list_languages.append(x)
    new_list_languages = datastructures.LanguageAccept(list_languages)
    request.accept_languages = new_list_languages
    return new_list_languages.best_match(app.config['LANGUAGES'])

from app import routes, models
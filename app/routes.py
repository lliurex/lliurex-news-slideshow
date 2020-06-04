from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, CarruselSettingsForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from flask_babel import lazy_gettext as _l
from json import dump as json_dump, load as json_load
from functools import wraps
import os

def validate_user(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        if current_user.is_authenticated and current_user.username == 'alu01':
            return render_template('access_denied.html')
        return f(*args,**kwargs)
    return wrapper


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',title='Home')


@app.route('/admin/carrusel', methods=['GET', 'POST'])
@validate_user
@login_required
def carrusel():
    form = CarruselSettingsForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            flash(_l('Config saved'))
            if form.background_image.data != None:
                f = form.background_image.data
                f.save(os.path.join(app.instance_path,'rsrc','carrusel_background'))
            with open('/etc/lliurex-news/carrusel.conf','w') as fd:
                config = form.data
                config.pop('background_image')
                config.pop('submit')
                config.pop('csrf_token')
                json_dump(config, fd, indent=4)
    else:
        if os.path.exists('/etc/lliurex-news/carrusel.conf'):
            try:
                with open('/etc/lliurex-news/carrusel.conf','r') as fd:
                    obj = json_load(fd)
                    form = CarruselSettingsForm(**obj)
            except :
                pass
    return render_template('carrusel_admin.html', title='admin carrusel',form=form)

@app.route('/admin/webserver', methods=['GET','POST'])
@login_required
def webserver():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter('username: '+ form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_l('Invalid username or password'))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
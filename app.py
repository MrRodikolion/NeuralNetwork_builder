from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import forms

from data import db_session
from data.users import User

import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/Sing-in', methods=['GET', 'POST'])
def singin():
    if current_user.is_authenticated:
        return redirect('/app')

    form = forms.SinginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if any(field is None for field in form.data.values()):
            return render_template('singin.html', form=form, warn='You must fill all fields')
        if form.password.data != form.conf_password.data:
            return render_template('singin.html', form=form, warn='Password does not match')
        if len(form.password.data) < 8:
            return render_template('singin.html', form=form, warn='Password must contain more than 8 characters')
        if len(db_sess.query(User).filter(User.email == form.mail.data).all()) != 0:
            return render_template('singin.html', form=form, warn='User with this email already exists')

        new_user = User()
        new_user.username = form.username.data
        new_user.email = form.mail.data
        new_user.hashed_password = form.password.data
        db_sess.add(new_user)
        db_sess.commit()

        return redirect('/app')

    return render_template('singin.html', form=form)


@app.route('/Log-in', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/app')

    form = forms.LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        like_user: User = db_sess.query(User).filter(
            User.email == form.mail.data,
        ).first()
        if not like_user:
            return render_template('login.html', form=form, warn='Email is incorrect')
        if not like_user.check_password(form.password.data):
            return render_template('login.html', form=form, warn='Password is incorrect')

        login_user(like_user, remember=True)
        return redirect('/app')
    return render_template('login.html', form=form)


@app.route('/app')
@app.route('/app/projects')
@app.route('/app/projects/nn')
@app.route('/app/projects/db')
def projects():
    if not current_user.is_authenticated:
        return redirect('/Log-in')

    return render_template('main_app.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


def working():
    return 'working'


if __name__ == '__main__':
    db_session.global_init('db/database.sqlite')
    app.run(host='0.0.0.0', port=8080)

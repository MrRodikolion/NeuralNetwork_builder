from flask import Flask, render_template, redirect
import forms

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/Sing-in', methods=['GET', 'POST'])
def singin():
    form = forms.SinginForm()
    if form.validate_on_submit():
        if form.password.data != form.conf_password.data:
            return render_template('singin.html', form=form, warn='Password does not match')
        if len(form.password.data) < 8:
            return render_template('singin.html', form=form, warn='Password must contain more than 8 characters')
        return redirect('/')

    return render_template('singin.html', form=form)


@app.route('/Log-in', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('login.html', form=form)


@app.route('/app/projects')
def projects():
    return render_template('main_app.html')


def working():
    return 'working'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

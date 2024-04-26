from flask import Flask, render_template, redirect, url_for, Blueprint, request, send_file
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import forms
import zipfile
import io
import PIL.Image, PIL.ImageFilter
import numpy as np

from data import db_session
from data.users import User
from data.db_projects import DataBaseProject, Image

from api import blueprint_images

import datetime
import base64

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
def projects():
    if not current_user.is_authenticated:
        return redirect('/Log-in')

    return redirect('/app/projects/nn')


@app.route('/app/projects/nn')
def projects_nn():
    if not current_user.is_authenticated:
        return redirect('/Log-in')

    return render_template('projects_nn.html')


@app.route('/app/projects/db')
def projects_db():
    if not current_user.is_authenticated:
        return redirect('/Log-in')

    db_sess = db_session.create_session()
    _projects = db_sess.query(DataBaseProject).filter(
        DataBaseProject.user_id == current_user.id
    ).all()

    return render_template('projects_db.html', projects=_projects)


@app.route('/app/projects/create/db', methods=['GET', 'POST'])
@login_required
def projects_create_db():
    form = forms.DataBaseProjectCreateForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        same_project = db_sess.query(DataBaseProject).filter(
            DataBaseProject.user_id == current_user.id, DataBaseProject.name == form.project_name.data).first()
        if same_project:
            return redirect(same_project.href)

        new_project = DataBaseProject()
        new_project.name = form.project_name.data
        new_project.href = f'/app/project/db/{current_user.username}/{form.project_name.data}'
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.projects.append(new_project)
        db_sess.add(new_project)
        db_sess.commit()

        return redirect(new_project.href)

    return render_template('projects_create_db.html', form=form)


@app.route('/app/projects/create/nn', methods=['GET', 'POST'])
@login_required
def projects_create_nn():
    form = forms.NeuralNetworkProjectCreateForm()
    if form.validate_on_submit():
        print(form.data)
        return redirect('/')

    return render_template('projects_create_nn.html', form=form)


@app.route('/app/projects/delete/db/<project_name>', methods=['GET', 'POST'])
@login_required
def delete_db_project(project_name):
    form = forms.DeleteProjectForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        to_delete_project = db_sess.query(DataBaseProject).filter(
            DataBaseProject.user_id == current_user.id,
            DataBaseProject.name == project_name
        ).first()
        for image in to_delete_project.images:
            db_sess.delete(image)
        db_sess.delete(to_delete_project)
        db_sess.commit()

        return redirect('/app/projects/db')

    return render_template('delete_project.html', form=form)


@app.route('/app/project/db/<project_username>/<project_name>', methods=['GET', 'POST'])
@app.route('/app/project/db/<project_username>/<project_name>/upload', methods=['GET', 'POST'])
def db_project(project_username, project_name):
    db_sess = db_session.create_session()
    project_user = db_sess.query(User).filter(
        User.username == project_username
    ).first()
    project = db_sess.query(DataBaseProject).filter(
        DataBaseProject.user_id == project_user.id,
        DataBaseProject.name == project_name
    ).first()
    if request.method == 'GET':
        return render_template('db_project_upload.html', project=project)
    elif request.method == 'POST':
        for f in request.files.getlist('file_name'):
            new_img = Image()
            new_img.data = f.read()
            project.images.append(new_img)
        db_sess.commit()
        return redirect(request.url)


@app.route('/app/project/db/<project_username>/<project_name>/dataset')
def db_project_dataset(project_username, project_name):
    db_sess = db_session.create_session()
    project_user = db_sess.query(User).filter(
        User.username == project_username
    ).first()
    project = db_sess.query(DataBaseProject).filter(
        DataBaseProject.user_id == project_user.id,
        DataBaseProject.name == project_name
    ).first()

    image_urls = [(n, f'data:image/png;base64,{base64.b64encode(image.data).decode("utf-8")}') for n, image in
                  enumerate(project.images[:100])]

    return render_template('db_project_view.html', project=project, images=image_urls)


@app.route('/app/project/db/<project_username>/<project_name>/<img_id>')
def db_project_img_view(project_username, project_name, img_id):
    db_sess = db_session.create_session()
    project_user = db_sess.query(User).filter(
        User.username == project_username
    ).first()
    project = db_sess.query(DataBaseProject).filter(
        DataBaseProject.user_id == project_user.id,
        DataBaseProject.name == project_name
    ).first()

    image = f'data:image/png;base64,{base64.b64encode(project.images[int(img_id)].data).decode("utf-8")}'

    return render_template('db_project_img_view.html', project=project, image=image, img_id=img_id)


@app.route('/app/project/db/<project_username>/<project_name>/<img_id>/delete')
def db_project_img_delete(project_username, project_name, img_id):
    db_sess = db_session.create_session()
    project_user = db_sess.query(User).filter(
        User.username == project_username
    ).first()
    project = db_sess.query(DataBaseProject).filter(
        DataBaseProject.user_id == project_user.id,
        DataBaseProject.name == project_name
    ).first()

    db_sess.delete(project.images[int(img_id)])
    db_sess.commit()

    return redirect(f'/app/project/db/{project_username}/{project_name}/dataset')


@app.route('/app/project/db/<project_username>/<project_name>/download', methods=['GET', 'POST'])
def db_project_download(project_username, project_name):
    db_sess = db_session.create_session()
    project_user = db_sess.query(User).filter(
        User.username == project_username
    ).first()
    project = db_sess.query(DataBaseProject).filter(
        DataBaseProject.user_id == project_user.id,
        DataBaseProject.name == project_name
    ).first()

    form = forms.DataBaseProjectGen()
    if form.validate_on_submit():

        memory_file = io.BytesIO()

        with zipfile.ZipFile(memory_file, 'w') as zf:
            for n, image in enumerate(project.images):

                pil_img = PIL.Image.open(io.BytesIO(image.data))
                pil_img = pil_img.resize((form.img_size_x.data, form.img_size_y.data))

                if form.is_add_gray.data:
                    to_save = io.BytesIO()
                    gray_pil_img = pil_img.convert('L')
                    gray_pil_img.save(to_save, format='PNG')
                    zf.writestr(f'{n}_g.jpg', to_save.getvalue())
                if form.is_add_blur.data:
                    to_save = io.BytesIO()
                    blur_pil_img = pil_img.filter(PIL.ImageFilter.GaussianBlur(radius=4))
                    blur_pil_img.save(to_save, format='PNG')
                    zf.writestr(f'{n}_b.jpg', to_save.getvalue())
                if form.is_add_noise.data:
                    to_save = io.BytesIO()

                    np_image = np.array(pil_img)

                    noise = np.random.normal(0, 255, np_image.shape)
                    zero_indx = np.random.choice(np_image.size, size=int(np_image.size - np_image.size * 0.1),
                                                 replace=False)
                    zero_indx = np.unravel_index(zero_indx, np_image.shape)
                    noise[zero_indx] = 0

                    noisy_image = np_image + noise

                    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)

                    noisy_pil_image = PIL.Image.fromarray(noisy_image)
                    noisy_pil_image.save(to_save, format='PNG')
                    zf.writestr(f'{n}_n.jpg', to_save.getvalue())

                to_save = io.BytesIO()
                pil_img.save(to_save, format='PNG')
                zf.writestr(f'{n}.jpg', to_save.getvalue())

        memory_file.seek(0)

        return send_file(memory_file, as_attachment=True, download_name=f'{project_name}.zip')

    return render_template('db_project_download.html', project=project, form=form)


@app.route('/app/project/db/<project_username>/<project_name>/stats')
def db_project_stats(project_username, project_name):
    db_sess = db_session.create_session()
    project_user = db_sess.query(User).filter(
        User.username == project_username
    ).first()
    project = db_sess.query(DataBaseProject).filter(
        DataBaseProject.user_id == project_user.id,
        DataBaseProject.name == project_name
    ).first()

    numper_pictures = len(project.images)

    return render_template('db_project_stats.html', project=project, np=numper_pictures)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    db_session.global_init('db/database.sqlite')
    app.register_blueprint(blueprint_images)
    app.run(host='0.0.0.0', port=8080)

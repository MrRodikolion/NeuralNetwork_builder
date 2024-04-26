import os

from flask import Blueprint, send_file, url_for
from data import db_session
from data.db_projects import Image, DataBaseProject

import io

blueprint_images = Blueprint(
    'images_api',
    __name__,
    template_folder='templates'
)


@blueprint_images.route('/api/images/<project_id>')
def get_main_image(project_id):
    db_sess = db_session.create_session()

    project = db_sess.query(DataBaseProject).filter(DataBaseProject.id == project_id).first()

    if project.images:
        image = project.images[0]
        img_io = io.BytesIO(image.data)

        return send_file(img_io, mimetype='image/jpeg')

    with open('static/images/no_img.jpg', 'rb') as img_file:
        img_bytes = img_file.read()

    img_io = io.BytesIO(img_bytes)

    return send_file(img_io, mimetype='image/jpeg')



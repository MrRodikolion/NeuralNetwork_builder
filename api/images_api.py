from pathlib import Path
from flask_login import current_user, login_required
from PIL import Image as PillowImage

from flask import Blueprint, send_file, url_for, abort
from data import db_session
from data.db_projects import Image, DataBaseProject

import io

blueprint_images = Blueprint(
    'images_api',
    __name__,
    template_folder='templates'
)


@blueprint_images.route('/api/images/<project_id>')
@login_required
def get_main_image(project_id):
    db_sess = db_session.create_session()

    project = db_sess.query(DataBaseProject).filter(DataBaseProject.id == project_id).first()

    if project is None:
        abort(404)
    if project.user_id != current_user.id:
        abort(403)

    if project.images:
        image = project.images[0]
        img_io = io.BytesIO(image.data)

        try:
            with PillowImage.open(io.BytesIO(image.data)) as preview:
                mimetype = preview.get_format_mimetype()
        except OSError:
            abort(404)
        return send_file(img_io, mimetype=mimetype)

    with (Path(__file__).resolve().parents[1] / 'static/images/no_img.jpg').open('rb') as img_file:
        img_bytes = img_file.read()

    img_io = io.BytesIO(img_bytes)

    return send_file(img_io, mimetype='image/jpeg')



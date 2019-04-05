from flask import current_app, flash
import os
from PIL import Image

def portfolio_img_uploader(data, name, folder, testimonial):

    _, f_ext = os.path.splitext(data.filename)

    if f_ext != ".png":
        f_ext = ".png"
    else:
        pass

    picture_fn = name + f_ext

    if testimonial == True:
        folder = os.path.join(current_app.root_path, 'static/img/testimonial', folder)
    elif testimonial == False:
        folder = os.path.join(current_app.root_path, 'static/img/portfolio', folder)

    try:
        os.mkdir(folder)
    except OSError:
        flash('folder with that name already created!')

    picture_path = os.path.join(folder, picture_fn)

    if os.path.isfile(picture_path):
        os.remove(picture_path)

    i = Image.open(data)

    return i.save(picture_path)

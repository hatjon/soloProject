from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.post import Post
import uuid
import os
from contextlib import nullcontext
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

UPLOAD_FOLDER = 'flask_app/static/img/IMAGE_UPLOADS'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/createPost', methods=['POST'])
def createPost():

    if request.files['image'] is None:
        image = ''
        flash('Image is required', 'image')
        return redirect(request.referrer)
    if request.files['image'] is not None:
        image = request.files['image']

    if not Post.validate_post(request.form):
        return redirect(request.referrer)

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        time = datetime.now().strftime("%d%m%Y%S%f")
        time += filename
        filename = time
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    data = {
        'content': request.form['content'],
        'user_id': session['user_id'],
        'image': filename
    }
    Post.create_post(data)
    return redirect('/')

@app.route('/like/<int:id>')
def addLike(id):
    data = {
        'post_id': id,
        'user_id': session['user_id']
    }
    Post.addLike(data)
    return redirect(request.referrer)

@app.route('/unlike/<int:id>')
def removeLike(id):
    data = {
        'post_id': id,
        'user_id': session['user_id']
    }
    Post.removeLike(data)
    return redirect(request.referrer)

@app.route('/delete/<int:id>')
def destroyPost(id):
    data = {
        'post_id': id,
    }
    post = Post.get_post_by_id(data)
    if session['user_id']==post['user_id']:
        Post.deleteAllLikes(data)
        Post.destroyPost(data)
        return redirect(request.referrer)
    return redirect(request.referrer)
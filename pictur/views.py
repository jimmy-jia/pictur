from pictur import app
from flask import Flask, url_for, redirect, request, render_template
import os
from pictur.sql_model import sql_controller

UPLOADS_FOLDER = 'static/resources/postimages'

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and UPLOADS_FOLDER is not '':
        file = request.files['file']
        if file:
            tags = request.form['tags']
            uid = 0 # get a real user later
            description = request.form['description']
            title = request.form['title']
            image_id = sql_controller.insert_post(tags, uid, description, title)[0]
            filename = str(image_id) + '.gif'
            file.save(os.path.join(UPLOADS_FOLDER, filename))
            return redirect(url_for('image', image_id = image_id))
    n_to_display = 9
    posts = sql_controller.select_n_post(n_to_display)
    return render_template('front.html', posts = posts)
	
@app.route('/i<image_id>', methods=['GET', 'POST'])
def image(image_id):
    if request.method == 'POST' and UPLOADS_FOLDER is not '':
        file = request.files['file']
        if file:
            tags = request.form['tags']
            uid = 0 # get a real user later
            description = request.form['description']
            title = request.form['title']
            image_id = sql_controller.insert_post(tags, uid, description, title)[0]
            filename = str(image_id) + '.gif'
            file.save(os.path.join(UPLOADS_FOLDER, filename))
            return redirect(url_for('image', image_id = image_id))
    post = sql_controller.select_post(image_id)
    comments = sql_controller.select_comments_for_post(image_id)
    response = render_template('index.html', post=post, comments=comments, image='{}/{}.gif'.format(UPLOADS_FOLDER, image_id))
    return response

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST' and UPLOADS_FOLDER is not '':
        file = request.files['file']
        if file:
            tags = request.form['tags']
            uid = 0 # get a real user later
            description = request.form['description']
            title = request.form['title']
            image_id = sql_controller.insert_post(tags, uid, description, title)[0]
            filename = str(image_id) + '.gif'
            file.save(os.path.join(UPLOADS_FOLDER, filename))
            return redirect(url_for('image', image_id = image_id))
    return render_template('upload.html')

@app.route('/search', methods=['GET'])
def search_comment():
    tag = request.args.get('tag')
    if tag != None and tag != '':
        posts = sql_controller.tag_search(tag, 9)
        return render_template('front.html', posts=posts)
    return render_template('front.html', posts=[])
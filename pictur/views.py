from pictur import app
from flask import Flask, url_for, redirect, request, render_template
import os
from pictur.sql_model import sql_controller

UPLOADS_FOLDER = '/root/pictur/pictur/static/resources/postimages/'

@app.route('/')
@app.route('/index')
def index():
    '''images = get_recent_images() #images should be a list of image id's '''
    post = {"title":"This fox likes being brushed", "description":"Check this out", "time":"16:15:14 2015-16-32"}
    return render_template('index.html', post=post, image='static/resources/postimages/1.gif')
#, images = images)
	
@app.route('/i=<image_id>')
def image(image_id):
    '''image_data = get_image_metadata(image_id) #image_data should be a dictionary of title, description, etc.'''
    post = sql_controller.select_post(image_id)
    return render_template('index.html', post=post, image='static/resources/postimages/{}.gif'.format(image_id))

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

from pictur import app
from flask import Flask, url_for, redirect, request, render_template
import os

UPLOADS_FOLDER = ''

@app.route('/')
@app.route('/index')
def index():
    '''images = get_recent_images() #images should be a list of image id's '''
    post = {"title":"This fox likes being brushed", "description":"Check this out", "time":"16:15:14 2015-16-32"}
    return render_template('index.html', post=post, image='static/resources/postimages/1.gif')
#, images = images)
	
@app.route('/i=<image_id>')
def profile(image_id):
    '''image_data = get_image_metadata(image_id) #image_data should be a dictionary of title, description, etc.'''
    post = {"title":"This fox likes being brushed", "description":"Check this out", "time":"16:15:14 2015-16-32"}
    return render_template('index.html', post=post, image='static/resources/postimages/{}.gif'.format(image_id))
#, image_id = image_id, image_data = image_data)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    '''if request.method == 'POST' and UPLOADS_FOLDER is not '':
        file = request.files['file']
                image_id = upload_to_database(file) #filename should be an image id
                filename = image_id + '.png'
        file.save(os.path.join(UPLOADS_FOLDER, filename))
        return redirect(url_for('/i/' + image_id))'''
    return render_template('index.html')

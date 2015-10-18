from pictur import app
from flask import Flask, url_for, redirect, request, render_template
import os

UPLOADS_FOLDER = 'static/resources/postimages'

TEMP_COMMENTS = [{'uid':6077,
                  'time':'15:00',
                  'text':'test post 1',
                  'children':[{'uid':190, 'time': '15:00', 'text':'testpost2', 'children':[]},
                              {'uid':3, 'time':'17:00', 'text':'testpost3', 'children':[{'uid':53, 'time':'15:00', 'text':'testpost4', 'children':[]}]}]},
                 {'uid':666, 'time':'2:30', 'text':'testpost master', 'children':[]}]

@app.route('/')
@app.route('/index')
def index():
    '''images = get_recent_images() #images should be a list of image id's '''
    post = {"title":"This fox likes being brushed", "description":"Check this out", "time":"16:15:14 2015-16-32"}
    return render_template('index.html', post=post, image='UPLOADS_FOLDER/{}.gif')
#, images = images)
	
@app.route('/i=<image_id>')
def profile(image_id):
    '''image_data = get_image_metadata(image_id) #image_data should be a dictionary of title, description, etc.'''
    post = {"title":"This fox likes being brushed", "description":"Check this out", "nickname":"ProfSingha", "time":"16:15:14 2015-16-32"}
    testcomment = '''
						<div class="comment child-b">
							<div class="comment-vote">
								<button class="upvote"></button>
								<button class="downvote"></button>
							</div>
    '''
    return render_template('index.html', post=post, image='{}/{}.gif'.format(UPLOADS_FOLDER, image_id), comments=TEMP_COMMENTS)
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

# def commentGenerator(comment):
#       return comment.getChildren() 

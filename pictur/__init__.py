from flask import Flask
from flask.ext.thumbnails import Thumbnail

RELATIVE_FOLDER = 'static/resources/postimages'
UPLOADS_FOLDER = '/root/pictur/pictur/static/resources/postimages'
app = Flask(__name__)
app.host = '0.0.0.0'

app.config['MEDIA_FOLDER'] = UPLOADS_FOLDER
app.config['MEDIA_URL'] = "/" + RELATIVE_FOLDER
thumb = Thumbnail(app)

from pictur import views

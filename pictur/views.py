from pictur import app, RELATIVE_FOLDER
from flask import Flask, url_for, redirect, request, render_template, jsonify
import os
from pictur.sql_model import sql_controller
from flask_oauth2_login import GoogleLogin
import flask.ext.login as flask_login


#https://github.com/maxcountryman/flask-login
#https://github.com/marksteve/flask-oauth2-login/blob/master/flask_oauth2_login/base.py

UPLOADS_FOLDER = '/root/pictur/pictur/static/resources/postimages'

# START GOOGLE OAUTH EXPERIMENTATION

app.config.update(
  SECRET_KEY="secret",
  GOOGLE_LOGIN_REDIRECT_SCHEME="http",
)
'''for config in (
  "GOOGLE_LOGIN_CLIENT_ID",
  "GOOGLE_LOGIN_CLIENT_SECRET",
):

app.config[config] = os.environ[config]'''
app.config['GOOGLE_LOGIN_CLIENT_ID'] = '755630576898-r93qit7p1dn3o4iuglbfqejd92vru1tg.apps.googleusercontent.com'
app.config['GOOGLE_LOGIN_CLIENT_SECRET'] = 'S9e88SekVZO_9a0IVI5fad3y'
google_login = GoogleLogin(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User():
    authenticated = False
    active = False
    anonymous = False
    email = '' # Note: The email should be google's email
    username = 'anonymous' # This is their nickname for the site
    uid = 0
    def is_authenticated(self):
        return self.authenticated
    def is_active(self):
        return self.active
    def is_anonymous(self):
        return self.anonymous
    def get_id(self):
        return self.uid
    def to_string(self):
        return 'User:' + str(self.username) + ' Email:' + str(self.email) + ' UID:' + str(self.uid)

@google_login.login_success
def login_attempt(token, profile): # Google login was successful, so we attempt to log in to pictur now
    google_email = profile['email']
    data = sql_controller.get_user_by_email(google_email)
    if data:
        user = User()
        user.uid = data['uid']
        user.active = True
        success = flask_login.login_user(user)
        #return str(success) + ':' + user.to_string()
        return redirect(url_for('index')) # Login successful redirect to main page
    # Email not registered, ask if they want to register
    uid = sql_controller.insert_user("", google_email)
    user = User()
    user.uid = uid
    user.active = True
    flask_login.login_user(user)
    return redirect(url_for('signup')) 
#    return jsonify(token=token, profile=profile)
    
# jsonify(token=token, profile=profile)

@google_login.login_failure
def login_failure(e):
    return jsonify(error=str(e))
  
  
@app.route('/testauth')
def testauth():
    return """
<html>
<a href="{}">Login with Google</a>
""".format(google_login.authorization_url())

'''<a href='/'>Logout</a>'''

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('index'))
    

@login_manager.user_loader # Shouldn't be called?
def user_loader(uid):
    data = sql_controller.get_user_by_uid(uid)
    if data:
        user = User()
        user.email = data['email']
        user.username = data['nickname']
        user.uid = data['uid']
        return user
    return None

@login_manager.request_loader
def request_loader(request):
    return None

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'
    
@app.route('/protected')
def protected():
    user = flask_login.current_user
    if user.is_anonymous():
        return 'not logged in'
    return 'Logged in as: ' + user.to_string()
 
# END GOOGLE OAUTH EXPERIMENTATION 
    
# START ACTUAL WEBSITE

def process_upload(request):
    file = request.files['file']
    if file:
        tags = request.form['tags']
        description = request.form['description']
        title = request.form['title']
        image_id = sql_controller.insert_post(tags, user.uid, description, title)[0]
        filename = str(image_id) + '.gif'
        file.save(os.path.join(UPLOADS_FOLDER, filename))
        return image_id
    return 0
    
def process_comment(request, pid):
    user = flask_login.current_user
    if user.is_anonymous():
        user = User()
    pcid = request.form['parentcid']
    content = request.form['content']
    sql_controller.insert_comment(pid, user.uid, content, pcid)
    
def edit_comment(request):
    cid = request.form['cid']
    content = request.form['content']
    sql_controller.update_comment(cid, content)

def id_to_path(pid):
    return str(pid) + '.gif'
    
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    page_context = {}
    user = flask_login.current_user
    if user.is_anonymous():
        user = User()
    else:
        if len(user.username.strip()) == 0:
            return redirect(url_for('signup'))
    if request.method == 'POST' and UPLOADS_FOLDER is not '':
        image_id = process_upload(request) # get a real user later
        return redirect(url_for('image', image_id = image_id))
    n_to_display = 25
    page = int(request.args.get('page', default = '1'))-1
    posts = sql_controller.select_n_post_offset(n_to_display, n_to_display*page)
    page_context['google_url'] = google_login.authorization_url()
    user = flask_login.current_user
    if not user.is_anonymous():
        page_context['username'] = user.username
    page_context['id_to_path'] = id_to_path
    return render_template('front.html', posts = posts, page_context = page_context).format(google_login.authorization_url())
	
@app.route('/i<image_id>', methods=['GET', 'POST'])
def image(image_id):
    page_context = {}
    user = flask_login.current_user
    if user.is_anonymous():
        user = User()
    else:
        if len(user.username.strip()) == 0: 
            return redirect(url_for('signup'))
    if request.method == 'POST' and UPLOADS_FOLDER is not '':
        source = request.form['source']
        if source == 'post':
            image_id = process_upload(request) # get a real user later
            return redirect(url_for('image', image_id = image_id))
        elif source == 'comment':
            process_comment(request, image_id)
            return redirect(url_for('image', image_id = image_id))
        elif source == 'commentedit':
            edit_comment(request)
            return redirect(url_for('image', image_id = image_id))
        elif source == 'deletepost':
            sql_controller.delete_post(image_id)
            return redirect(url_for('index'))
    post = sql_controller.select_post(image_id)
    comments = sql_controller.select_comments_for_post(image_id)
    tags = post['tags'].split(",")
    page_context['nickname'] = sql_controller.get_user_by_uid(post['uid'])['nickname']
    page_context['google_url'] = google_login.authorization_url()
    response = render_template('index.html', post=post, tags=tags, comments=comments, image='{}/{}.gif'.format(RELATIVE_FOLDER, image_id), page_context = page_context)
    return response

@app.route('/search', methods=['GET', 'POST'])
def search_comment():
    user = flask_login.current_user
    if user.is_anonymous():
        user = User()
    else:
        if len(user.username.strip()) == 0: return redirect(url_for('signup'))
    if request.method == 'POST' and UPLOADS_FOLDER is not '':
        image_id = process_upload(request) # get a real user later
        return redirect(url_for('image', image_id = image_id))
    tag = request.args.get('tag')
    if tag != None and tag != '':
        posts = sql_controller.tag_search(tag, 9)
        return render_template('front.html', posts=posts)
    return render_template('front.html', posts=[])
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    page_context = {}
    page_context['from_google'] = 0
    if request.method == 'POST':
        name = request.form['signup-name']
        if len(name.strip()) == 0:
            return redirect(url_for('signup'))
        sql_controller.update_user(flask_login.current_user.uid, name)
        return redirect(url_for('index'))
    user = flask_login.current_user
    if user.is_anonymous():
        page_context['google_url'] = google_login.authorization_url()
        return render_template('signup.html', page_context = page_context)
    if len(user.username.strip()) == 0:
        page_context['from_google'] = 1
        return render_template('signup.html', page_context = page_context)
        

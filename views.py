from pictur import pictur

@pictur.route('/')
@pictur.route('/index')
def index():
    return render_template('index.html')

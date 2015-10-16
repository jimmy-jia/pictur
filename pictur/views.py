from pictur import app
from flask import Flask, url_for, redirect, request, render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
	
@app.route('/p/<subpic>/i/<image_id>')
def profile(subpic, image_id):
    return render_template('index.html')

@app.route('/p/<subpic>/upload', methods=['GET', 'POST'])
def upload_file(subpic):
    '''if request.method == 'POST':
        file = request.files['file']
        file.save('C:\\Users\\Charles\\Documents\\411Project\\upload\\test.png')
        return redirect(url_for('index'))'''
    return render_template('index.html')

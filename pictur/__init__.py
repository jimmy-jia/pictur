from flask import Flask
app = Flask(__name__)
app.host = '0.0.0.0'
from pictur import views

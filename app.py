from dotenv import load_dotenv
from api import api_blueprint
from flask import Flask
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

CORS(app, resources={r"/api/*": {"origins": "*"}})
load_dotenv(dotenv_path='.env')

app.register_blueprint(api_blueprint, url_prefix='/api')


@app.route('/')
def homepage():
    the_time = datetime.now()
    print(the_time)

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>

    <img src="http://loremflickr.com/600/400" />
    """.format(time=the_time)

from flask import Flask, flash, redirect, request
from datetime import datetime
from regex import P
from sklearn import cluster
from werkzeug.utils import secure_filename

from pandas import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.cluster import KMeans

app = Flask(__name__)

# SETTING FOLDER
UPLOAD_FOLDER = './static/uploads/'
app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def homepage():
    the_time = datetime.now()
    print(the_time)

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>

    <img src="http://loremflickr.com/600/400" />
    """.format(time=the_time)


@app.route("/test")
def test():
    data = pd.read_csv('./static/uploads/matrix.csv')
    cluster = KMeans(n_clusters=4)
    data["cluster"] = cluster.fit_predict(data[data.columns[2:]])
    data = data.to_dict(orient='records')

    return {"data": data}, 200

from flask import Flask, flash, redirect, request
from datetime import datetime
from sklearn import cluster
from werkzeug.utils import secure_filename

import numpy as np
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import date, timedelta, datetime
from numpy import arange
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from pandas import merge
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
app = Flask(__name__)
CORS(app, supports_credentials=True)
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


@app.route("/review")
def review():
    data = devideGroup()
    return {"data": data}, 200


def devideGroup():
    df_feature = pd.read_csv('./static/uploads/feature.csv')
    df_feature.head()
    df_review = pd.read_csv('./static/uploads/review_feature.csv')
    df_review.head()
    df = merge(df_feature, df_review, on="FeatureID")
    df.head()
    # tạo table đếm mỗi Feature theo review
    table = df.pivot_table(index=["ReviewID"], columns=[
                           "FeatureID"], values="n")
    table.head()
    table = table.fillna(0).reset_index()
    table.head()
    # trích xuất các feature
    cols = table.columns[1:]
    # clustering of reviews
    # tao thuat toan cluster kmean với số cụm =4
    cluster = KMeans(n_clusters=4)
    # dự đoán nhóm cụm cho mỗi dòng đánh giá
    table["cluster"] = cluster.fit_predict(table[table.columns[2:]])
    table.to_csv('./static/uploads/cluster_matrix.csv')
    g1 = table[table["cluster"] == 0]
    g2 = table[table["cluster"] == 1]
    g3 = table[table["cluster"] == 2]
    g4 = table[table["cluster"] == 3]
    eachgroup_feature = pd.DataFrame()
    eachgroup_feature['g1'] = g1[cols].sum()
    eachgroup_feature['g2'] = g2[cols].sum()
    eachgroup_feature['g3'] = g3[cols].sum()
    eachgroup_feature['g4'] = g4[cols].sum()
    eachgroup_feature.to_csv('./static/uploads/eachgroup_feature.csv')
    wg_eachgroup_feature = pd.DataFrame()
    wg_eachgroup_feature['g1'] = eachgroup_feature['g1'].div(
        g1["ReviewID"].count())
    wg_eachgroup_feature['g2'] = eachgroup_feature['g2'].div(
        g2["ReviewID"].count())
    wg_eachgroup_feature['g3'] = eachgroup_feature['g3'].div(
        g3["ReviewID"].count())
    wg_eachgroup_feature['g4'] = eachgroup_feature['g4'].div(
        g4["ReviewID"].count())
    wg_eachgroup_feature.loc['wg', :] = wg_eachgroup_feature.sum(axis=0)
    wg_eachgroup_feature.iloc[-1]
    max = wg_eachgroup_feature.max(axis=1).iloc[-1]
    second = wg_eachgroup_feature.apply(
        lambda row: row.nlargest(2).values[-1], axis=1).iloc[-1]
    third = wg_eachgroup_feature.apply(
        lambda row: row.nlargest(3).values[-1], axis=1).iloc[-1]
    fourth = wg_eachgroup_feature.apply(
        lambda row: row.nlargest(4).values[-1], axis=1).iloc[-1]
    conditions = [(wg_eachgroup_feature.iloc[-1] == max), (wg_eachgroup_feature.iloc[-1] == second),
                  (wg_eachgroup_feature.iloc[-1] == third), (wg_eachgroup_feature.iloc[-1] == fourth)]
    values = ['G1', 'G2', 'G3', 'G4']
    wg_eachgroup_feature.loc['group', :] = np.select(conditions, values)
    result = pd.DataFrame(table[["ReviewID", "cluster"]])
    condition2 = [(table["cluster"] == 0), (table["cluster"] == 1),
                  (table["cluster"] == 2), (table["cluster"] == 3)]
    group = ['g1', 'g2', 'g3', 'g4']
    result['group'] = np.select(condition2, group)
    wg_eachgroup_feature.to_csv("./static/uploads/wg_eachgroup_feature.csv")
    value2 = wg_eachgroup_feature.iloc[-1].to_list()
    result['groupQuality'] = np.select(condition2, value2)
    result.drop("cluster", axis=1, inplace=True)
    result.drop("group", axis=1, inplace=True)
    result.to_csv('./static/uploads/result.csv')
    data = result.to_dict(orient='records')
    return data


@app.route("/apireview")
def review():
    data = predictReview()
    return {"data": data}, 200


def predictReview():
    data = pd.read_csv('./static/uploads/matrix.csv')
    cluster = KMeans(n_clusters=4)
    data["cluster"] = cluster.fit_predict(data[data.columns[2:]])
    condition2 = [(data["cluster"] == 0), (data["cluster"] == 1),
                  (data["cluster"] == 2), (data["cluster"] == 3)]
    wg_eachgroup_feature = pd.read_csv(
        "./static/uploads/wg_eachgroup_feature.csv")
    wg_eachgroup_feature.drop('FeatureID', axis=1, inplace=True)
    value2 = wg_eachgroup_feature.iloc[-1].to_list()
    data['groupQuality'] = np.select(condition2, value2)
    data = data.to_dict(orient='records')
    return data

from flask import Blueprint, request, redirect

from api.data.MatrixDB import MatrixDB
import pandas as pd

matrixDB = MatrixDB()

data_blueprint = Blueprint('data_blueprint', __name__)


# @ data_blueprint.route('/test-mgdb', methods=['GET'])
# def test_mgdb():
#     matrixDB.create_sample_data()
#     return "OK"


@ data_blueprint.route('/test-tts', methods=['GET'])
def test_tts():
    df_review = pd.read_csv('./static/uploads/matrix.csv')
    # remove all data in collection
    matrixDB.remove_all_data()
    matrixDB.df_to_mongo(df_review)
    return "OK"


@ data_blueprint.route('/test-getdata', methods=['GET'])
def test_getdata():

    data_df = matrixDB.mongo_to_df()
    data_df = data_df.drop(columns=['_id'])
    return data_df.to_json()

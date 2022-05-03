from flask import request
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from pandas import merge
from api.data.MatrixDB import MatrixDB
from api.data.WgFeatureDB import WgFeatureDB
matrixDB = MatrixDB()
wgFeatureDB = WgFeatureDB()


def DBdevideGroup():
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
    # remove all data and add matrix in collection MatrixDB
    matrixDB.remove_all_data()
    matrixDB.df_to_mongo(table)
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
    # remove all data and add wgFeature in collection WgFeatureDB
    wgFeatureDB.remove_all_data()
    wgFeatureDB.df_to_mongo(wg_eachgroup_feature)
    value2 = wg_eachgroup_feature.iloc[-1].to_list()
    result['groupQuality'] = np.select(condition2, value2)
    result.drop("cluster", axis=1, inplace=True)
    result.drop("group", axis=1, inplace=True)
    result.to_csv('./static/uploads/result.csv')
    data = result.to_dict(orient='records')
    return data


def add2DataFrame():
    df_feature = pd.read_csv('./static/uploads/feature.csv')
    df_review = pd.read_csv('./static/uploads/review_feature.csv')
    df = pd.merge(df_feature, df_review, on="FeatureID")
    df_matrix = pd.read_csv('./static/uploads/matrix.csv')
    df_no = df.pivot_table(index=["ReviewID"], columns=[
                           "FeatureID"], values="n")
    df_no = df_no.fillna(0).reset_index()
    cols = list(df_no.columns)
    df_matrix.drop("Unnamed: 0", axis=1, inplace=True)
    cols_matrix = list(df_matrix.columns)
    # change type column df_matrix matching column table
    for i in range(len(cols_matrix)):
        for j in range(len(cols)):
            if cols_matrix[i] == cols[j]:
                df_matrix[cols_matrix[i]
                          ] = df_matrix[cols_matrix[i]].astype(float)
                break
    # remove first column of 2 data frames
    df_matrix.drop(df_matrix.columns[0], axis=1, inplace=True)
    df_no.drop(df_no.columns[0], axis=1, inplace=True)

    # add row 1 -> len of df_no to df_matrix
    len_no = len(df_no)
    len_matrix = len(df_matrix)
    for i in range(len_no):
        row = df_no.iloc[i]
        df_matrix.loc[len_matrix + i] = row.values

    print(df_matrix)

    return df_matrix.to_json(orient='records')


def createlabel():
    json = request.get_json()
    # convert json to dataframe
    data = pd.DataFrame(json)
    # add to matrixDB collection
    matrixDB.df_to_mongo(data)
    # data = pd.read_json(json, orient='index')
    cluster = KMeans(n_clusters=4)
    data["cluster"] = cluster.fit_predict(data[data.columns[2:]])
    condition2 = [(data["cluster"] == 0), (data["cluster"] == 1),
                  (data["cluster"] == 2), (data["cluster"] == 3)]
    wg_eachgroup_feature = pd.read_csv(
        "./static/uploads/wg_eachgroup_feature.csv")
    value2 = wg_eachgroup_feature.iloc[-1].to_list()
    value2.remove('group')
    data['groupQuality'] = np.select(condition2, value2)
    data = data[['ReviewID', 'groupQuality']]
    data = data.to_dict(orient='records')

    return {"data": data}, 200


def devideGroup():
    # tạo table đếm mỗi Feature theo review
    table = matrixDB.mongo_to_df()
    table = table.drop(columns=['_id'])
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
    # remove all data and add wgFeature in collection WgFeatureDB
    wgFeatureDB.remove_all_data()
    wgFeatureDB.df_to_mongo(wg_eachgroup_feature)
    value2 = wg_eachgroup_feature.iloc[-1].to_list()
    result['groupQuality'] = np.select(condition2, value2)
    result.drop("cluster", axis=1, inplace=True)
    result.drop("group", axis=1, inplace=True)
    result.to_csv('./static/uploads/result.csv')
    print(result)
    return result.to_dict(orient='records')


def DBcreatelabel():
    json = request.get_json()
    # convert json to dataframe
    data = pd.DataFrame(json)
    # add to matrixDB collection
    matrixDB.df_to_mongo(data)
    # data = pd.read_json(json, orient='index')
    cluster = KMeans(n_clusters=4)
    data["cluster"] = cluster.fit_predict(data[data.columns[2:]])
    condition2 = [(data["cluster"] == 0), (data["cluster"] == 1),
                  (data["cluster"] == 2), (data["cluster"] == 3)]
    wg_eachgroup_feature = wgFeatureDB.mongo_to_df()
    wg_eachgroup_feature = wg_eachgroup_feature.drop(columns=['_id'])
    value2 = wg_eachgroup_feature.iloc[-1].to_list()
    data['groupQuality'] = np.select(condition2, value2)
    data = data[['ReviewID', 'groupQuality']]
    data = data.to_dict(orient='records')

    return {"data": data}, 200

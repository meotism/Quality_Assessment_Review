import pandas as pd
from config.db import MongoDB

collection_name = 'WgLabel'

mongoDB = MongoDB()


class WgFeatureDB:
    def __init__(self):
        self.collection = mongoDB.get_db().get_collection(collection_name)

    # # dataframe to mongodb
    def df_to_mongo(self, df):
        a = 1
        for index, row in df.iterrows():
            # drop review id
            data = row.to_dict()
            result = {}
            # convert all key to string
            for key in data:
                result[str(key)] = data[key]
            # Set self collection object id = a+1
            result['_id'] = a
            a += 1
            # how to add result to mongodb and _id is number
            self.collection.insert_one(result)

    #  # mongodb to dataframe

    def mongo_to_df(self):
        df = pd.DataFrame(list(self.collection.find()))
        return df

    #  # remove all data in collection
    def remove_all_data(self):
        self.collection.delete_many({})

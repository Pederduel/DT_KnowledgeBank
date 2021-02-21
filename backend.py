import pymongo
from pymongo import MongoClient
import os # for using os commands
import settings # importing settings.py allows us to use the os.getenv command for calling the .env file

# imports for machine learning
import pandas as pd
import numpy as np
from sklearn import datasets, svm
import pickle
import time
#import xgboost
#from xgboost import XGBClassifier

# importing database url from .env file
mongoUrl = os.getenv("MONGO_URL")

# setting the cluster variable
cluster = MongoClient(mongoUrl)

# setting the database variable
db = cluster["KnowledgeBank"]

# setting collection variables
modelsCollection = db["models"]

iris = datasets.load_iris(return_X_y=True)
X = iris[0] # data
y = iris[1] # target

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)

# XGBoost training
#xgb = XGBClassifier()
#xgb.fit(X_train, y_train)

# Classification
clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
score = clf.score(X_test, y_test)

def save_model_to_db(model, client, database, dbconnection, model_name):
    pickled_model = pickle.dumps(model)
    myClient = pymongo.MongoClient(client)
    mydb = myClient[db]
    mycon = mydb[dbconnection]
    info = mycon.insert_one({model_name: pickled_model, 'name': model_name, 'created_time': time.time()})
    details = {
        'inserted_id':info.inserted_id,
        'model_name':model_name,
        'created_time':time.time()
    }
    return details

def fetch_model_from_db(model_name, client, database, dbconnection):
    json_data = {}
    myClient = pymongo.MongoClient(client)
    mydb = myClient[db]
    mycon = mydb[dbconnection]
    data = mycon.find({'name':model_name})

    for i in data:
        json_data = i
    pickled_model = json_data[model_name]

    return pickle.loads(pickled_model)

test = save_model_to_db(model = clf, client = mongoUrl, database = db, dbconnection = modelsCollection, model_name='Test')
print(test)

#def main():
#    testSave = save_model_to_db(clf, mongoUrl, db, modelsCollection,'Test')

#if __name__ == "__main__":
#    main()

# first connection test
'''test1 = {"_id": 0, "name": "Hypertension", "Description": "Predicts risk of developing hypertension", 
"beta_0": -15.139611, "beta_1": 0.048337, "beta_2": 0.055844, "beta_3": 0.060932, 
"Age": 25, "Systolic": 120, "Diastolic": 75}

modelsCollection.insert_one(test1)'''
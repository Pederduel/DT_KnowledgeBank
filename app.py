import pymongo
from pymongo import MongoClient
import os # for using os commands
import setup # importing setup.py allows us to use the os.getenv command for calling the .env file

from flask import Flask, request, json, Response, jsonify, make_response, send_file
from flask_restful import Api, Resource
from flask_restx import Api, Resource, fields
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import requests
from gridfs import GridFS
import urllib

# imports for machine learning
#import pandas as pd
#import numpy as np
#from sklearn import datasets, svm, linear_model
#import pickle
#from pickle import load
#import json
import onnx
from onnx import load_model
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import StringTensorType, FloatTensorType
import onnxruntime as rt

import onnxmltools
import onnxmltools.convert.common.data_types


# -------- SETUP -------- #

mongoUrl = os.getenv("MONGO_URL")                      # URL for the MongoDB Atlas cluster
KGEUrl = "https://kge-dtapp.herokuapp.com/model-onnx"  # URL for the KGE heroku endpoints

client = MongoClient(mongoUrl)                    # The cluster itself as the client

knowledgeGenerator = client["KnowledgeGenerator"] # KGE database
KGE_Models = knowledgeGenerator["fs.files"]       # The collection within the database storing the trained models

knowledgeBank = client["KnowledgeBank"]           # KB database
KB_Models = knowledgeBank["fs.files"]               # The collection storing the models in the KB
fs = GridFS(knowledgeBank)                        # Using GridFS to store large files in MongoDB

app = Flask(__name__)
app.config["MONGO_URI"] = mongoUrl
api = Api(app=app,
            version=0.01,
            title="Knowledge Bank",
            description="Backend for storing machine learning models in the Digital Twins project")

# -------- END SETUP -------- #


# -------- METHODS AND ENDPOINTS -------- #

@api.route("/models/<model_name>/")
@api.doc(params={'name': 'Model name'})
class GetModel(Resource):
    def get(self, model_name):
        try:
            model = KB_Models.find_one({"name" : model_name})
        except:
            e = pymongo.errors.InvalidName(error_labels=404 ,message="The model could not be found...")
            return e
        return model

@api.route("/models/delete/<model_name>/")
@api.doc(params={'name': 'Model name'})
class DeleteModel(Resource):
    def delete(self, model_name):
        try:
            KB_Models.delete_one({'name': model_name})
        except:
            e = pymongo.errors.InvalidName(error_labels=404 ,message="The model '{model_name}' could not be found...")
            return e

@api.route("/kge-models", methods=["GET"])
class KGEModel(Resource):
    def get(self):  
        onnx_filename = "model-onnx.onnx" # filename for the onnx model
        urllib.request.urlretrieve(KGEUrl, onnx_filename) # request file from url
        model = onnx.load(onnx_filename) # load onnx file
        onnx.save(model, onnx_filename) # save as onnx file to make sure its saved correctly (redundant)
        #sess = rt.InferenceSession(filename)
        #input_name = sess.get_inputs()[0].name
        #label_name = sess.get_outputs()[0].name
        #test_x = np.array([[24, 130, 83, 1]])
        #prediction = sess.run(None, {input_name: test_x.astype(np.float32)})[0]
        model_name = "test_onnx_model"
        #store_model(onnx_filename, model_name, 1, "Onnx file used for testing") # store onnx model in KB
        return send_file(onnx_filename, attachment_filename="ONNX Model. v0.1") # send model when url is requested

def store_model(file, filename, version, desc):
    with open(file, 'rb') as f:
        fs.put(f, filename=filename, version=version, description=desc)

def save_as_onnx(model_to_save, filename):
    initial_type = [('float_input', FloatTensorType([1, 4]))]
    onx = convert_sklearn(model_to_save, initial_types=initial_type)
    with open(filename, "wb") as f:
        f.write(onx.SerializeToString())

'''
@api.route("/models/")
class GetAllModels(Resource):
    def get_all_models(self):
        models = list(KGE_Models.find())
        return models

class PostModel(Resource):
    print("PostModel called")
    def post(self, serialized_model):
        print("In post method")
        try:
            print("In try")
            print(serialized_model)
            KB_Models.insert_one(serialized_model)
            print(serialized_model)
        except:
            e = pymongo.errors.InvalidOperation()
            return e
'''
# -------- END METHODS AND ENDPOINTS -------- #

# -------- RUN APP -------- #

if __name__ == "__main__":
    app.run(debug=True)


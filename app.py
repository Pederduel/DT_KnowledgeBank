import pymongo
from pymongo import MongoClient
import os # for using os commands
import env # importing env.py allows us to use the os.getenv command for calling the .env file

from flask import Flask, request, Response, send_file 
from flask_restx import Api, Resource, fields
#from flask_pymongo import PyMongo
from gridfs import GridFS
import urllib

# -- Imports for machine learning -- #
import onnx
import onnxruntime as rt
import onnxmltools

# -------- SETUP -------- #

mongoUrl = os.getenv("MONGO_URL")                      # URL for the MongoDB Atlas cluster
KGEUrl = "https://kge-dtapp.herokuapp.com/model-onnx"  # URL for the KGE Heroku endpoint

client = MongoClient(mongoUrl)                    # The cluster itself as the client

knowledgeGenerator = client["KnowledgeGenerator"] # KGE database
KGE_Models = knowledgeGenerator["fs.files"]       # The collection storing the trained models in the KGE

knowledgeBank = client["KnowledgeBank"]           # KB database
KB_Models = knowledgeBank["fs.files"]             # The collection storing the models in the KB
fs = GridFS(knowledgeBank)                        # Using GridFS (as 'fs') to store large files in MongoDB

app = Flask(__name__)
app.config["MONGO_URI"] = mongoUrl
#mongo = PyMongo(app)
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
            model = KB_Models.find_one({"filename" : model_name})
        except:
            e = pymongo.errors.InvalidName(error_labels=404 ,message="The model could not be found...")
            return e
        return model

@api.route("/models/delete/<model_name>/")
@api.doc(params={'name': 'Model name'})
class DeleteModel(Resource):
    def delete(self, model_name):
        try:
            KB_Models.delete_one({'filename': model_name})
        except:
            e = pymongo.errors.InvalidName(error_labels=404 ,message="The model '{model_name}' could not be found...")
            return e

@api.route("/kge-models", methods=["GET"])
class KGEModel(Resource):
    def get(self):  
        onnx_file = "model-onnx.onnx" # filename for the onnx model
        urllib.request.urlretrieve(KGEUrl, onnx_file) # request ONNX file from URL using urllib for easier file management
        model = onnx.load(onnx_file) # load onnx file
        onnx.save(model, onnx_file) # overwright as ONNX file to make sure its saved correctly (redundant?)
        
        onnx_modelName = "test_onnx_model_v2"
        #store_model(onnx_file, onnx_modelName, 1, "Onnx file used for testing") # store ONNX model in KB as GridFS
        modelfromKB = KB_Models.find_one({"filename": onnx_modelName})
        print("---- vv Model from KB vv ----")
        print(modelfromKB)
        return send_file(onnx_file, attachment_filename="ONNX Model. v0.1") # send model when URL is requested

def store_model(onnx_file, modelName, version, desc):
    with open(onnx_file, 'rb') as f:
        fs.put(f, filename=modelName, version=version, description=desc)

#sess = rt.InferenceSession(filename)
#input_name = sess.get_inputs()[0].name
#label_name = sess.get_outputs()[0].name
#test_x = np.array([[24, 130, 83, 1]])
#prediction = sess.run(None, {input_name: test_x.astype(np.float32)})[0]

#requests
#pandas
#sklearn
#Flask-PyMongo

# -------- END METHODS AND ENDPOINTS -------- #

# -------- RUN APP -------- #

if __name__ == "__main__":
    app.run(debug=True)


# DT_KnowledgeBank
Used for storing and distributing machine learning models to the Digital Twins mobile application.


## Needed packages are:

### pymongo: 
```bash
pip install pymongo
```

 - To get the dnspython module: 
 ```bash
 pip install pymongo[srv]
 ``` 
 (Needed to connect to the MongoDB Atlas cluster)

### Environment: 
```bash
pip install -U python-dotenv
```
### Server (Flask)
```bash
pip install flask
pip install flask-restx
```
### ONNX:
```bash
pip install onnx onnxmltools onnxruntime
```
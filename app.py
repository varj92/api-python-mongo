from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['MONGO_URI']='mongodb+srv://api:api@cluster0.fm27z.mongodb.net/prospectos?retryWrites=true&w=majority'
mongo = PyMongo(app)

#CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def home():
    return('Hola Mundo')

@app.route('/captura', methods=['POST'])
def captura():
    nombre =request.json['nombre']
    appaterno = request.json['appaterno']
    apmaterno = request.json['apmaterno']
    calle = request.json['calle']
    numero = request.json['numero']
    colonia = request.json['colonia']
    codpos = request.json['codpos']
    telefono = request.json['telefono']
    rfc = request.json['rfc']

    if nombre and appaterno and calle and numero and colonia and codpos and telefono and rfc:
        id = mongo.db.prospectos.insert(
        {
            'nombre' : nombre,
            'appaterno' : appaterno,
            'apmaterno' : apmaterno,
            'calle' : calle,
            'numero' : numero,
            'colonia' : colonia,
            'codpos' : codpos,
            'telefono' : telefono,
            'rfc' : rfc,
            'estatus' : 'Enviado'
        })
        response = {
            '_id': str(id),
            'nombre' : nombre,
            'appaterno' : appaterno,
            'apmaterno' : apmaterno,
            'calle' : calle,
            'numero' : numero,
            'colonia' : colonia,
            'codpos' : codpos,
            'telefono' : telefono,
            'rfc' : rfc
        }
        return response

    else:
        return not_found()

    return {'message': 'Recibido'}

@app.route('/listado', methods = ['GET'])
def listado():
    prospectos = mongo.db.prospectos.find()
    response = json_util.dumps(prospectos)
    return Response(response, mimetype='application/json')

@app.route('/listado/<id>', methods = ['GET'])
def detalle(id):
    prospecto = mongo.db.prospectos.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(prospecto)
    return Response(response, mimetype='application/json')

@app.route('/evaluacion/<id>', methods = ['PUT'])
def evaluacion(id):
    nombre =request.json['nombre']
    appaterno = request.json['appaterno']
    apmaterno = request.json['apmaterno']
    calle = request.json['calle']
    numero = request.json['numero']
    colonia = request.json['colonia']
    codpos = request.json['codpos']
    telefono = request.json['telefono']
    rfc = request.json['rfc']
    estatus = request.json['estatus']
    rechazo = request.json['rechazo']

    if estatus:
        mongo.db.prospectos.update_one({'_id': ObjectId(id)}, {'$set': 
        {
            'nombre' : nombre,
            'appaterno' : appaterno,
            'apmaterno' : apmaterno,
            'calle' : calle,
            'numero' : numero,
            'colonia' : colonia,
            'codpos' : codpos,
            'telefono' : telefono,
            'rfc' : rfc,
            'estatus' : estatus,
            'rechazo' : rechazo
        }})
        response = jsonify({'message': 'Prospecto Autorizado - id: ' + id})
        return response
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run()
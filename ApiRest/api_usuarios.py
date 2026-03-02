from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

usuarios = [
    {"id": 101, "nombre": "Alicia", "rol": "Admin"},
    {"id": 102, "nombre": "Roberto", "rol": "Cliente"},
]

class UsuarioLista(Resource):
    def get(self):
        return jsonify(usuarios)

api.add_resource(UsuarioLista, "/usuarios")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5081, debug=True)
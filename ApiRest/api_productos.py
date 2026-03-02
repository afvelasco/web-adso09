from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

# Simulación base de datos
productos = [
    {"id": 1, "nombre": "Teclado Gamer", "precio": 185000},
    {"id": 2, "nombre": "Mouse Gamer", "precio": 148000},
    {"id": 3, "nombre": "Auriculares Gamer", "precio": 242000}
]

class ProductoLista(Resource):
    def get(self):
        # Devuelve directamente el array
        return jsonify(productos)

    def post(self):
        nuevo_producto = request.json
        nuevo_producto["id"] = len(productos) + 1
        productos.append(nuevo_producto)
        return jsonify(nuevo_producto)

class Producto(Resource):
    def get(self, id):
        producto = next((p for p in productos if p["id"] == id), None)
        if producto:
            return jsonify(producto)
        return jsonify({"mensaje": "Producto no encontrado"}), 404

api.add_resource(ProductoLista, "/productos")
api.add_resource(Producto, "/productos/<int:id>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5080, debug=True)
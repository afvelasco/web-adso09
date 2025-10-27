from flask import Flask, render_template, request
import mysql.connector
import hashlib

programa = Flask(__name__)
mi_db = mysql.connector.connect(host="localhost",
                                port="3306",
                                user="root",
                                password="",
                                database="db-adso09")
mi_cursor = mi_db.cursor()

@programa.route("/")
def index():
    return render_template("index.html")

@programa.route("/login", methods=['POST'])
def login():
    usua = request.form["usua"]
    contra = request.form["contra"]
    sql = f"SELECT * FROM usuarios WHERE usuario='{usua}'"
    mi_cursor.execute(sql)
    resultado = mi_cursor.fetchall()
    cifrada = hashlib.sha512(contra.encode("utf-8")).hexdigest()
    if len(resultado)>0 and cifrada==resultado[0][3]:
        sql = "SELECT * FROM productos"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return render_template("productos.html", productos = resultado)
    else:
        return render_template("index.html",msg = "Credenciales incorrectas")
    
if __name__=="__main__":
    programa.run(host="0.0.0.0",port="5000",debug=True)
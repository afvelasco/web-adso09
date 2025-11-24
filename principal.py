import os
from flask import Flask, redirect, render_template, request, send_from_directory
import mysql.connector
import hashlib

programa = Flask(__name__)
mi_db = mysql.connector.connect(host="localhost",
                                port="3306",
                                user="root",
                                password="",
                                database="db-adso09")
mi_cursor = mi_db.cursor()
programa.config['CARPETA_UP'] = os.path.join('uploads')

@programa.route("/uploads/<nombre>")
def uploads(nombre):
    return send_from_directory(programa.config['CARPETA_UP'],nombre)

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
        return redirect("/productos")
    else:
        return render_template("index.html",msg = "Credenciales incorrectas")

@programa.route("/productos")
def productos():
    sql = "SELECT * FROM productos WHERE inactivo=0"
    mi_cursor.execute(sql)
    resultado = mi_cursor.fetchall()
    return render_template("productos.html", productos = resultado)

@programa.route("/agregaproducto")
def agregaproducto():
    return render_template("agregaproducto.html")

@programa.route("/guardaproducto", methods=['POST'])
def guardaproducto():
    id = request.form['id']
    nom = request.form['nom']
    pre = request.form['pre']
    sal = request.form['sal']
    foto = request.files['foto']
    nom,ext =os.path.splitext(foto.filename)
    foto_nueva = 'P'+id+ext
    foto.save("uploads/"+foto_nueva)
    sql = f"INSERT INTO productos (idproducto,nombre,precio,saldo,foto) VALUES ('{id}','{nom}',{pre},{sal},'{foto_nueva}')"
    mi_cursor.execute(sql)
    mi_db.commit()
    return redirect('/productos')

@programa.route("/modificaproducto/<id>")
def modificaproducto(id):
    sql = f"SELECT * FROM productos WHERE idproducto='{id}'"
    mi_cursor.execute(sql)
    resultado = mi_cursor.fetchall()[0]
    return render_template("/modificaproducto.html", pro=resultado)

@programa.route("/actualizaproducto", methods=['POST'])
def actualizaproducto():
    id = request.form['id']
    nom = request.form['nom']
    pre = request.form['pre']
    sal = request.form['sal']
    foto = request.files['foto']
    sql = f"UPDATE productos SET nombre='{nom}', precio={pre}, saldo={sal} WHERE idproducto='{id}'"
    mi_cursor.execute(sql)
    mi_db.commit()
    n,ext =os.path.splitext(foto.filename)
    if n!="":
        sql = f"SELECT * FROM productos WHERE idproducto='{id}'"
        mi_cursor.execute(sql)
        foto_vieja = mi_cursor.fetchall()[0][4]
        if foto_vieja != "":
            os.remove(os.path.join(programa.config['CARPETA_UP'],foto_vieja))
        foto_nueva = 'P'+id+ext
        foto.save("uploads/"+foto_nueva)
        sql = f"UPDATE productos SET foto='{foto_nueva}' WHERE idproducto='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()
    return redirect("/productos")            

@programa.route("/borraproducto/<id>")
def borraproducto(id):
    sql = f"UPDATE productos SET inactivo=1 WHERE idproducto='{id}'"
    print(id)
    mi_cursor.execute(sql)
    mi_db.commit()
    return redirect("/productos")

if __name__=="__main__":
    programa.run(host="0.0.0.0",port="5000",debug=True)
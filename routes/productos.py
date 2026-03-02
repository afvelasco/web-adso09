from conexion import *
from models.productos import mis_productos

@programa.route("/productos")
def productos():
    if session.get('login') == True:
        resultado = mis_productos.consulta()
        return render_template("productos.html", productos = resultado)
    else:
        return redirect("/")

@programa.route("/agregaproducto")
def agregaproducto():
    if session.get('login') == True:
        return render_template("agregaproducto.html",msg="")
    else:
        return redirect("/")

@programa.route("/guardaproducto", methods=['POST'])
def guardaproducto():
    if session.get('login') == True:
        id = request.form['id']
        nom = request.form['nom']
        pre = request.form['pre']
        sal = request.form['sal']
        foto = request.files['foto']
        resultado = mis_productos.consulta_id(id)
        if len(resultado)==0:
            mis_productos.agrega(id,nom,pre,sal,foto)
            return redirect('/productos')
        else:
            return render_template("agregaproducto.html", msg = "Este Id de producto ya está en uso")
    else:
        return redirect("/")

@programa.route("/modificaproducto/<id>")
def modificaproducto(id):
    if session.get('login') == True:
        resultado = mis_productos.consulta_id(id)[0]
        return render_template("/modificaproducto.html", pro=resultado)
    else:
        return redirect("/")

@programa.route("/actualizaproducto", methods=['POST'])
def actualizaproducto():
    if session.get('login') == True:
        id = request.form['id']
        nom = request.form['nom']
        pre = request.form['pre']
        sal = request.form['sal']
        foto = request.files['foto']
        mis_productos.modifica(id,nom,pre,sal,foto)
        return redirect("/productos")            
    else:
        return redirect("/")

@programa.route("/borraproducto/<id>")
def borraproducto(id):
    if session.get('login') == True:
        mis_productos.borra(id)
        return redirect("/productos")
    else:
        return redirect("/")

@programa.route("/consultaproducto", methods=['POST'])
def consultaproducto():
    datos=request.json
    id = datos['id']
    resultado = mis_productos.consulta_id(id)
    if len(resultado)>0:
        salida = {"valor":1, "msg":"El id ya existe"}
    else:
        salida = {"valor":0, "msg":"El id no existe"}
    return salida
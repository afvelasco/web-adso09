from conexion import *
import routes.productos

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
        session['login'] = True
        session['id'] = usua
        session['nombre'] = resultado[0][1]
        return redirect("/bienvenida")
    else:
        return render_template("index.html",msg = "Credenciales incorrectas")

@programa.route("/bienvenida")
def bienvenida():
    if session.get('login') == True:
        nom = session.get("nombre")
        return render_template("bienvenida.html", nom = nom)
    else:
        return redirect("/")


if __name__=="__main__":
    programa.run(host="0.0.0.0",port="5000",debug=True)
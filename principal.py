from flask import Flask, render_template, request

programa = Flask(__name__)

@programa.route("/")
def index():
    return render_template("index.html")

@programa.route("/login", methods=['POST'])
def login():
    usua = request.form["usua"]
    contra = request.form["contra"]
    if usua=="afvelasco" and contra=="1234":
        return render_template("bienvenido.html")
    else:
        return render_template("index.html",msg = "Credenciales incorrectas")
    

if __name__=="__main__":
    programa.run(host="0.0.0.0",port="5000",debug=True)
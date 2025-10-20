from flask import Flask

programa = Flask(__name__)

@programa.route("/")
def index():
    return "Esta es mi primer web-sita"

if __name__=="__main__":
    programa.run(host="0.0.0.0",port="5000",debug=True)
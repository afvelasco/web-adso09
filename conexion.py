from datetime import timedelta
import os
from random import randint
from flask import Flask, redirect, render_template, request, send_from_directory, session
import mysql.connector
import hashlib

programa = Flask(__name__)
programa.secret_key = str(randint(10000,99999))
programa.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
mi_db = mysql.connector.connect(host="localhost",
                                port="3306",
                                user="root",
                                password="",
                                database="db-adso09")
mi_cursor = mi_db.cursor()
programa.config['CARPETA_UP'] = os.path.join('uploads')

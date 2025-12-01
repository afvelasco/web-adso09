from conexion import *

class Productos:
    def consulta(self):
        sql = "SELECT * FROM productos WHERE inactivo=0"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado
    
    def consulta_id(self, id):
        sql = f"SELECT * FROM productos WHERE idproducto='{id}'"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado
    
    def agrega(self,id,nom,pre,sal,foto):
        nom,ext =os.path.splitext(foto.filename)
        foto_nueva = 'P'+id+ext
        foto.save("uploads/"+foto_nueva)
        sql = f"INSERT INTO productos (idproducto,nombre,precio,saldo,foto) VALUES ('{id}','{nom}',{pre},{sal},'{foto_nueva}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def modifica(self,id,nom,pre,sal,foto):
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
        
    def borra(self,id):
        sql = f"UPDATE productos SET inactivo=1 WHERE idproducto='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()

mis_productos = Productos()


import sqlite3

def cargar_campo(nombre, puntaje):
    
    with sqlite3.connect('parcial_juego/base_datos/data_base.db') as conexion:
        try:
            sentencia = '''
                        insert into Score (nombre, puntaje) values (?,?)
                        '''
            conexion.execute(sentencia, (nombre, puntaje))
            print('cargado correctamente')
            return True 
        except Exception as e:
            print('Error al cargar el campo en la base de datos:', e)
            return False

def saber_top10():
    
    with sqlite3.connect('parcial_juego/base_datos/data_base.db') as conexion:
        try:
            cursor = conexion.cursor()
            sentencia = 'SELECT nombre, puntaje FROM Score ORDER BY puntaje DESC LIMIT 10'
            cursor.execute(sentencia)
            resultados = cursor.fetchall()
            return resultados
        except Exception as e:
                print('Error al buscar el top 10 en la base de datos:', e)
                return False
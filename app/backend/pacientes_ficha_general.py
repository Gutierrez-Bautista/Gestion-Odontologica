import sqlite3

DB_NAME = 'app/clinica.db'

def alta_ficha_general(nombre_apellido,datos_ficha_general):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM FichaGeneral where nombre_apellido = ?"
        cursor.execute(query, (nombre_apellido,))
        valid = cursor.fetchall()
        if not valid:
            cursor.execute('insert into FichaGeneral (nombre_apellido,obra_social,nro_afiliado,hta,diabetes,alergia,probl_renales,probl_cardiacos,plan_tratamiento,observaciones) values(?,?,?,?,?,?,?,?,?,?)',(nombre_apellido,datos_ficha_general))
            valid = cursor.fetchall()
            return ['paciente cargado con ficha general','dataUpload',200]
        else: 
            return 'paciente ya cargado'
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)

def consulta_ficha_general(nombre_apellido):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM FichaGeneral where nombre_apellido = ?"
        cursor.execute(query, (nombre_apellido,))
        valid = cursor.fetchall()
        if not valid:
            return ['ficha general del paciente encontrada', valid, 200]
        else: 
            return ('paciente no existe','pacienteNotExists',200)
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)

def actualizar_ficha_genral(datos_ficha_general,nombre_apellido):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM FichaPAMI where nombre_apellido = ?"
        cursor.execute(query, (nombre_apellido,))
        valid = cursor.fetchall()
        if not valid:
            cursor.execute('update table FichaGeneral set nombre_apellido = ? ,obra_social = ? ,nro_afiliado = ? ,hta = ? ,diabetes = ? ,alergia,probl_renales = ? ,probl_cardiacos = ? ,plan_tratamiento = ? ,observaciones = ?  where nombre_apellido = ?' , (datos_ficha_general, nombre_apellido))
            valid = cursor.fetchall()
            return ['paciente actualizado con ficha general','dataUpload',200]
        else: 
            return ('paciente no existe','pacienteNotExists',200)
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)
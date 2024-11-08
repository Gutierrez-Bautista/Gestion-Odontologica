import sqlite3


DB_NAME = 'app/clinica.db'

"""   datos historia clinica odontologica:
      # motivo-consulta (texto) --> por que asistio a consulta
      # consulta-otro-prof (0 o 1) --> si ha consultado a otro porfesional
      # dif-masticar (0 o 1) --> si tiene dificultad para masticar o no
      # dif-hablar (0 o 1) --> si tiene dificultad para hablar o no
      # mov-dental (0 o 1) --> si tiene movilidad dental o no
      # sang-encias (0 o 1) --> si le sangran la encias o no
      # cant-sepillados (o o mayor) --> cantidad de sepillados diarios
      # azucar (texto) --> momentos de azucar
    
    datos odontograma:
      # estado-odontograma (texto)
      # tratamiento-odontograma (texto) --> puede estar vacio  
"""

def agregar_historia_clinica_odon(historia_clinica, id_paciente):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM HistoriaClinicaOdontologica where paciente_id = ?"
        cursor.execute(query, (id_paciente,))
        valid = cursor.fetchall()
        if not valid:
            cursor.execute('insert into HistoriaClinicaOdontologica (paciente_id,motivo_consulta,consulta_reciente,dificultad_masticar,dificultad_hablar,movilidad_dentaria,sangrado_encias,cantidad_cepillados_diarios,momentos_azucar, descripcion) values(?,?,?,?,?,?,?,?,?,?)',(id_paciente,*historia_clinica))
            connection.commit()
            valid = cursor.fetchall()
            return ['paciente cargado con historial clinico','dataUpload',200]
        else: 
            return 'paciente ya cargado'
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)

def actualizar_historia_clinica_odon(historia_clinica,id_paciente):
    print(historia_clinica, '\n', id_paciente)
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM HistoriaClinicaOdontologica where paciente_id = ?"
        cursor.execute(query, (id_paciente,))
        valid = cursor.fetchall()
        if valid:
            cursor.execute('update HistoriaClinicaOdontologica set motivo_consulta = ?, consulta_reciente = ?,dificultad_masticar = ?, dificultad_hablar = ?, movilidad_dentaria = ?,sangrado_encias = ?,cantidad_cepillados_diarios = ?,momentos_azucar = ?, descripcion = ? where paciente_id = ?' , (*historia_clinica, id_paciente))
            connection.commit()
            valid = cursor.fetchall()
            return ['paciente actualizado con historia clinica','dataUpload',200]
        else: 
            return ('paciente no existe','pacienteNotExists',200)
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)

def consultar_historia_clinica_odon(id_paciente):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM HistoriaClinicaOdontologica where paciente_id = ?"
        cursor.execute(query, (id_paciente,))
        valid = cursor.fetchall()
        if valid:
            return ['historial clinico del paciente encontrada', valid[0], 200]
        else: 
            return ('paciente no existe','pacienteNotExists',200)
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)
    
def alta_odontograma(odontograma, id_paciente):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM odontograma where paciente_id = ?"
        cursor.execute(query, (id_paciente,))
        valid = cursor.fetchall()
        if not valid:
            cursor.execute('insert into odontograma (paciente_id ,estado,tratamiento) values(?,?,?)',(id_paciente,*odontograma))
            connection.commit()
            valid = cursor.fetchall()
            return ['paciente cargado con odontograma','dataUpload',200]
        else: 
            return 'paciente ya cargado'
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)

def consulta_odontograma(id_paciente):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM odontograma where paciente_id = ?"
        cursor.execute(query, (id_paciente,))
        valid = cursor.fetchall()
        if valid:
            return ['odontograma del paciente encontrada', valid[0], 200]
        else: 
            return ('paciente no existe','pacienteNotExists',200)
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)

def actualizar_odontograma(id_paciente,odontograma):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM odontograma where paciente_id = ?"
        cursor.execute(query, (id_paciente,))
        valid = cursor.fetchall()
        if valid:
            cursor.execute('update odontograma set estado = ?, tratamiento = ? where paciente_id = ?' , (*odontograma, id_paciente))
            connection.commit()
            return ['paciente actualizado con odontograma','dataUpload',200]
        else:
            return ('paciente no existe','pacienteNotExists',200)
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)
""" 
id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            fecha DATE NOT NULL,
            descripcion TEXT NOT NULL,
"""
def alta_historia_clinica(historia_clinica,paciente_id):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM HistoriaClinica where paciente_id = ?"
        cursor.execute(query, (paciente_id,))

        cursor.execute('insert into HistoriaClinica (paciente_id , fecha, descripcion) values(?,?,?)',(paciente_id,*historia_clinica))
        connection.commit()

        return ['paciente cargado con Histora Clinica','dataUpload',200]
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)

def actualizar_historia_clinica(historia_clinica, id_historia_clinica):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM HistoriaClinica where id = ?"
        cursor.execute(query, (id_historia_clinica,))
        valid = cursor.fetchall()
        if valid:
            cursor.execute('update HistoriaClinica set fecha = ?, descripcion = ? where id = ?' , (*historia_clinica,id_historia_clinica))
            connection.commit()
            valid = cursor.fetchall()
            return ['Histora Clinica actualizada','dataUpload',200]
        else: 
            return ('paciente no existe','pacienteNotExists',200)
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)

def consulta_historia_clinica(paciente_id):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM HistoriaClinica where paciente_id = ?"
        cursor.execute(query, (paciente_id,))
        valid = cursor.fetchall()
        if valid:
            return ['Historia clinica del paciente encontrada', valid, 200]
        else: 
            return ('paciente no existe','pacienteNotExists',200)
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)

def eliminar_historia_clinica(id_historia_clinica):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "DELETE FROM HistoriaClinica where id = ?"
        cursor.execute(query, (id_historia_clinica,))
        connection.commit()

        return ('paciente eliminado', 'dataDelete', 200)
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)
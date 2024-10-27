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
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM HistoriaClinicaOdontologica where paciente_id = ?"
        cursor.execute(query, (id_paciente,))
        valid = cursor.fetchall()
        if not valid:
            cursor.execute('update table HistoriaClinicaOdontologica set motivo_consulta = ?,consulta_reciente = ?,dificultad_masticar = ?,dificultad_hablar = ?,movilidad_dentaria = ?,sangrado_encias = ?,cantidad_cepillados_diarios = ?,momentos_azucar = ?, descripcion = ? where paciente_id = ?' , (*historia_clinica, id_paciente))
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
        if not valid:
            cursor.execute('update table odontograma set  where paciente_id = ?' , (*odontograma, id_paciente))
            connection.commit()
            valid = cursor.fetchall()
            return ['paciente actualizado con odontograma','dataUpload',200]
        else: 
            return ('paciente no existe','pacienteNotExists',200)
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)
    


def alta_historia_clinica(datos_historia_clinica):
    pass

def actualizar_historia_clinica(datos_historia_clinica, id_historia_clinica):
    pass

def consulta_historia_clinica(id_paciente):
    pass

def eliminar_historia_clinica(id_historia_clinica):
    pass

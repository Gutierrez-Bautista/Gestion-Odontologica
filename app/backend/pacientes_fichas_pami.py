import sqlite3

DB_NAME = 'app/clinica.db'

def ficha_pami(datos_ficha_pami, anamnesis, id_paciente):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM FichaPAMI where id = ?"
        cursor.execute(query, (id_paciente,))
        valid = cursor.fetchall()
        if not valid:
            cursor.execute('insert into FichaPAMI (id_paciente,lugar,fecha,nro_beneficio,titular,parentesco,localidad_paciente,codigo_postal_paciente,profesional,domicilio_prestador, localidad_prestador,codigo_prestador,medico_cabecera,tel_fijo_prestador) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (id_paciente, *datos_ficha_pami))
            connection.commit()
            ficha_pami_id = cursor.lastrowid
            cursor.execute('insert into Anamnesis (ficha_pami_id,enfermedad,tratamiento_medico,medicacion,alergia_droga,diabetes,cantidad_fuma,probl_cardiacos,hipertension,toma_aspirina_anticoagulantes,fue_operado) values(?,?,?,?,?,?,?,?,?,?,?)', (ficha_pami_id, *anamnesis))
            connection.commit()
            valid = cursor.fetchall()
            return ['paciente cargado con ficha pami','dataUpload',200]
        else: 
            return ['paciente ya cargado', 'dataAlreadyUpload', 200]
    except sqlite3.Error as e:
        return (f"Error al solicitar la información hila: {e}", "dataBaseError", 500)

def actualizar_ficha_pami (datos_ficha_pami, id, anamnesis):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM FichaPAMI where id = ?"
        cursor.execute(query, (id,))
        valid = cursor.fetchall()
        if not valid:
            cursor.execute('update table FichaPAMI set lugar = ?, fecha = ?, nro_beneficio = ?, titular = ?, parentesco = ?, localidad_paciente = ?, codigo_postal_paciente = ?, profesional = ?, domicilio_prestador = ?,  localidad_prestador = ?, medico_cabecera = ? where id = ?' , (*datos_ficha_pami, id))
            cursor.execute('update table Anamnesis set enfermedad = ?, tratamiento_medico = ?, medicacion = ?, alergia_droga = ?, diabetes = ?, cantidad_fuma =? ,probl_cardiacos = ?, hipertension = ?, toma_aspirina_anticoagulantes = ?, fue_operado = ? where id = ?',(*anamnesis, id))
            connection.commit()
            valid = cursor.fetchall()
            return ['paciente actualizado con ficha pami y anamnesis','dataUpload',200]
        else: 
            return ('paciente no existe','pacienteNotExists',200)
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)

def consulta_ficha_pami(id_paciente):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM FichaPAMI where id_paciente = ?"
        cursor.execute(query, (id_paciente,))
        valid = cursor.fetchall()
        if valid:
            return ['paciente encontrado', valid[0], 200]
        else: 
            return ('paciente no existe','pacienteNotExists',200)
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)

def consulta_anamnesis (id_ficha):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM Anamnesis where ficha_pami_id = ?"
        print(id_ficha)
        cursor.execute(query, (id_ficha,))
        valid = cursor.fetchall()
        if valid:
            return ['paciente encontrado', valid[0], 200]
        else: 
            return ('paciente no existe','pacienteNotExists',200)
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)
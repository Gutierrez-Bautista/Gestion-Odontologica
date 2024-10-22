import sqlite3

DB_NAME = 'app/clinica.db'

def ficha_pami(datos_ficha_pami, anamnesis, id_paciente):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM FichaPAMI where id = ?" # Esta consulta esta mal
        cursor.execute(query, (id_paciente,))
        valid = cursor.fetchall()
        ficha_pami_id = id_paciente # Esta logica es erronea
        if not valid:
            cursor.execute('insert into FichaPAMI (lugar,fecha,nro_beneficio,titular,parentesco,localidad_paciente,codigo_postal_paciente,profesional,domicilio_prestador, localidad_prestador,medico_cabecera) values(?,?,?,?,?,?,?,?,?,?,?)',(datos_ficha_pami))
            cursor.execute('insert into Anamnesis (ficha_pami_id,enfermedad,tratamiento_medico,medicacion,alergia_droga,diabetes,cantidad_fuma,probl_cardiacos,hipertension,toma_aspirina_anticoagulantes,fue_operado) values(?,?,?,?,?,?,?,?,?,?,?)',(ficha_pami_id,anamnesis)) # creeria que esto no funciona
            valid = cursor.fetchall()
            return ['paciente cargado con ficha pami','dataUpload',200]
        else: 
            return ['paciente ya cargado', 'dataAlreadyUpload', 200]
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)

def actualizar_ficha_pami (datos_ficha_pami, id, anamnesis):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM FichaPAMI where id = ?"
        cursor.execute(query, (id,))
        valid = cursor.fetchall()
        if not valid:
            cursor.execute('update table FichaPAMI set lugar = ?, fecha = ?, nro_beneficio = ?, titular = ?, parentesco = ?, localidad_paciente = ?, codigo_postal_paciente = ?, profesional = ?, domicilio_prestador = ?,  localidad_prestador = ?, medico_cabecera = ? where id = ?' , (datos_ficha_pami, id))
            cursor.execute('update table Anamnesis set enfermedad = ?, tratamiento_medico = ?, medicacion = ?, alergia_droga = ?, diabetes = ?, cantidad_fuma =? ,probl_cardiacos = ?, hipertension = ?, toma_aspirina_anticoagulantes = ?, fue_operado = ? where id = ?',(anamnesis, id))
            valid = cursor.fetchall()
            return ['paciente actualizado con ficha pami y anamnesis','dataUpload',200]
        else: 
            return ('paciente no existe','pacienteNotExists',200)
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)
    

def consulta_ficha_pami(id):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM FichaPAMI where id = ?"
        cursor.execute(query, (id,))
        valid = cursor.fetchall()
        if not valid:
            return ['paciente encontrado', valid, 200]
        else: 
            return ('paciente no existe','pacienteNotExists',200)
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)
import sqlite3

DB_NAME = 'app/clinica.db'

def ficha_pami(datos_ficha_pami, anamnesis, id_paciente):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM FichaPAMI where id = ?"
        cursor.execute(query, (id_paciente,))
        valid = cursor.fetchall()
        print('pacientes_ficha_pami linea 12. datos_ficha_pami =', datos_ficha_pami)
        print('pacientes_ficha_pami linea 13. anamnesis =', anamnesis)
        print('pacientes_ficha_pami linea 14. id_paciente =', id_paciente)
        print('pacientes_ficha_pami linea 15. valid =', valid)
        if not valid:
            print('pacientes_ficha_pami linea 17')
            cursor.execute('insert into FichaPAMI (id_paciente,lugar,fecha,nro_beneficio,titular,parentesco,localidad_paciente,codigo_postal_paciente,profesional,domicilio_prestador, localidad_prestador,codigo_prestador,medico_cabecera,tel_fijo_prestador) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (id_paciente, *datos_ficha_pami))
            print('pacientes_ficha_pami linea 19')
            connection.commit()
            print('pacientes_ficha_pami linea 21')

            ficha_pami_id = cursor.lastrowid
            print('pacientes_ficha_pami linea 24')
            cursor.execute('insert into Anamnesis (ficha_pami_id,enfermedad,tratamiento_medico,medicacion,alergia_droga,diabetes,cantidad_fuma,probl_cardiacos,hipertension,toma_aspirina_anticoagulantes,fue_operado) values(?,?,?,?,?,?,?,?,?,?,?)', (ficha_pami_id, *anamnesis))
            print('pacientes_ficha_pami linea 26')
            connection.commit()
            print('pacientes_ficha_pami linea 28')
            valid = cursor.fetchall()
            print('pacientes_ficha_pami linea 30')
            return ['paciente cargado con ficha pami','dataUpload',200]
        else: 
            return ['paciente ya cargado', 'dataAlreadyUpload', 200]
    except sqlite3.Error as e:
        return (f"Error al solicitar la información hila: {e}", "dataBaseError", 500)

def actualizar_ficha_pami (datos_ficha_pami, id_paciente, anamnesis):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM FichaPAMI where id_paciente = ?"
        cursor.execute(query, (id_paciente,))
        valid = cursor.fetchall()
        print('actualizar_ficha_pami linea 45. id_paciente =', id_paciente)
        print('actualizar_ficha_pami linea 46. valid =', valid)
        print('actualizar_ficha_pami linea 46. datos_ficha_pami =', datos_ficha_pami)
        if valid:
            cursor.execute('update FichaPAMI set lugar = ?, fecha = ?, nro_beneficio = ?, titular = ?, parentesco = ?, localidad_paciente = ?, codigo_postal_paciente = ?, profesional = ?, domicilio_prestador = ?,  localidad_prestador = ?, codigo_prestador = ?, medico_cabecera = ?, tel_fijo_prestador = ? where id_paciente = ?' , (*datos_ficha_pami, id_paciente))
            connection.commit()
            cursor.execute('update Anamnesis set enfermedad = ?, tratamiento_medico = ?, medicacion = ?, alergia_droga = ?, diabetes = ?, cantidad_fuma =? ,probl_cardiacos = ?, hipertension = ?, toma_aspirina_anticoagulantes = ?, fue_operado = ? where id = ?',(*anamnesis, valid[0][0]))
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

        cursor.execute(query, (id_ficha,))
        valid = cursor.fetchall()
        if valid:
            return ['paciente encontrado', valid[0], 200]
        else: 
            return ('paciente no existe','pacienteNotExists',200)
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)
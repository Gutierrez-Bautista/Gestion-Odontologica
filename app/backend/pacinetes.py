import sqlite3
import tablas
import pacientes_fichas_pami
import pacientes_ficha_general
import fichas_compartidas


DB_NAME = 'app/clinica.db'


#alta
def alta_paciente(nombre_apellido,telefono,email,edad,dni,domicilio,fecha_nacimiento,posee_pami, datos_ficha_pami,anamnesis, datos_ficha_general,odontograma,historia_clinica_odontologica):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM Pacientes where nombre_apellido = ?"
        cursor.execute(query, (nombre_apellido,))
        valid = cursor.fetchall()
        if not valid:
            cursor.execute('insert into Pacientes (nombre_apellido,telefono,email,edad,dni,domicilio,fecha_nacimiento,posee_pami) values(?,?,?,?,?,?,?,?)',(nombre_apellido,telefono,email,edad,dni,domicilio,fecha_nacimiento,posee_pami))
            connection.commit()
            valid = cursor.fetchall()
        else: 
            return ('paciente ya cargado','dataAlreadyUpload',200)
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)
    finally:
        cursor.execute('select max(id) from Pacientes')
        id_paciente = cursor.fetchall()[0][0]
        if posee_pami == '1':
            res = pacientes_fichas_pami.ficha_pami(datos_ficha_pami, anamnesis, id_paciente)
        else:
            res = pacientes_ficha_general.alta_ficha_general(datos_ficha_general, id_paciente)
        res1 = fichas_compartidas.alta_odontograma(odontograma, id_paciente)
        res2 = fichas_compartidas.agregar_historia_clinica_odon(historia_clinica_odontologica,id_paciente)
        return [res, res1, res2]

def actualizar_paciente (id,nombre_apellido,telefono,email,edad,dni,domicilio,fecha_nacimiento,posee_pami, datos_ficha_pami, anamnesis,datos_ficha_general, odontograma):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM Pacientes where id = ?"
        cursor.execute(query, (id,))
        valid = cursor.fetchall()
        if valid:
            cursor.execute('update Pacientes set nombre_apellido = ? ,telefono = ? ,email = ? ,edad = ? ,dni = ? ,domicilio = ? ,fecha_nacimiento = ? ,posee_pami = ? where id = ?', (nombre_apellido,telefono,email,edad,dni,domicilio,fecha_nacimiento,posee_pami,id))
            valid = cursor.fetchall()
            connection.commit()

            print('posee_pami =', posee_pami, '\ntype(posee_pami) = ', type(posee_pami))
            if posee_pami == '1':
                print('if posee_pami == "1" = True')
                cursor.execute('select * from FichaPAMI where id_paciente = ?', id)
                valid = cursor.fetchall()
                cursor.execute('select * from FichaGeneral where id_paciente = ?', id)
                valid1 = cursor.fetchall()
                print('pacientes linea 57. "valid"', valid)
                print('pacientes linea 58. "if valid"', True if valid else False)
                print('pacientes linea 59. "valid1"', valid1)
                print('pacientes linea 60. "if valid1"', True if valid1 else False)

                if valid1:
                    cursor.execute('delete from FichaGeneral where id_paciente = ?',id)

                if valid:
                    res = pacientes_fichas_pami.actualizar_ficha_pami (datos_ficha_pami, id ,anamnesis)
                
                else:   
                    res = pacientes_fichas_pami.ficha_pami (datos_ficha_pami , anamnesis, id)
            else:
                print('if posee_pami == "1" = False')
                cursor.execute('select * from FichaPAMI where id_paciente = ?', id)
                valid = cursor.fetchall()
                cursor.execute('select * from FichaGeneral where id_paciente = ?', id)
                valid1 = cursor.fetchall()
                print('pacientes linea 77. "valid"', valid)
                print('pacientes linea 78. "if valid"', True if valid else False)
                print('pacientes linea 79. "valid1"', valid1)
                print('pacientes linea 80. "if valid1"', True if valid1 else False)

                if valid:
                    cursor.execute('delete from FichaPAMI where id_paciente = ?',id)
                    cursor.execute('delete from Anamnesis where ficha_pami_id = ?',id)

                if valid1:
                    res = pacientes_ficha_general.actualizar_ficha_genral (datos_ficha_general, id)
                
                else:
                    res = pacientes_ficha_general.alta_ficha_general (datos_ficha_general, id)
            connection.commit()
            print('res =', res)

            fichas_compartidas.actualizar_odontograma(id, odontograma)


            return ['paciente actualizado','dataUpdated',200]
        else:
            return ('paciente no existe','pacienteNotExists',200)
    except sqlite3.Error as e:
        print('e.args = ', e.args)
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)

# consulta por nombre ==> listo
# consulta por id ==> listo
# consulta por pami ==> listo

def consul_pacente (id_paciente, nom_paciente, pami_paciente):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM Pacientes "
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)
    finally:
        try:
            if id_paciente is not None:
                cursor.execute(query + 'where id =?',(id_paciente,))
                valid = cursor.fetchall()
                if not valid:
                    return ['Cliente no encontrado', 'noDataFound', 403]
                else:
                    basic = valid[0]
                    if basic[8] == 0:
                        ficha = pacientes_ficha_general.consulta_ficha_general(id_paciente)
                        
                    else:
                        ficha = pacientes_fichas_pami.consulta_ficha_pami(id_paciente)
                        

                    historial_odontologico = fichas_compartidas.consultar_historia_clinica_odon(id_paciente)
                    odontograma = fichas_compartidas.consulta_odontograma(id_paciente)

                    if ficha[1] == 'pacienteNotExists':
                        return ['error garrafal en ficha, debe rehacerse la BBDD', 'criticalError', 500]
                    if historial_odontologico[1] == 'pacienteNotExists':
                        return ['error garrafal en historial odontologico, debe rehacerse la BBDD', 'criticalError', 500]
                    if odontograma[1] == 'pacienteNotExists':
                        return ['error garrafal en odontograma, debe rehacerse la BBDD', 'criticalError', 500]
                    
                    ficha = ficha[1]

                    historial_odontologico = historial_odontologico[1]
                    odontograma = odontograma[1]

                    if basic[8] == 0: anamnesis = "noAplica"
                    else: anamnesis = pacientes_fichas_pami.consulta_anamnesis(ficha[0])[1]


                    return ['cliente encontrado',
                            {"basic": basic,
                            "ficha": ficha,
                            "anamnesis": anamnesis,
                            "historial_odontologico": historial_odontologico,
                            "odontograma": odontograma,
                            "historia_clinica": "notDeveloped"}, 200]
            elif nom_paciente is not None:
                cursor.execute(query + "where nombre_apellido like ? ||'%' or nombre_apellido like '%;' || ? || '%'",(nom_paciente, nom_paciente))

                valid = cursor.fetchall()
                if not valid:
                    return ['Cliente no encontrado', 'noDataFound', 403]
                else:
                    return ['cliente encontrado', valid, 200]
            elif pami_paciente is not None:
                cursor.execute(query + 'where posee_pami =?',(pami_paciente,))
                valid = cursor.fetchall()
                if not valid:
                    return ['Cliente no encontrado', 'noDataFound', 403]
                else:
                    return ['cliente encontrado', valid, 200]
            else:
                return ['argumento no pasado', 'argNotPassed', 412]
        except sqlite3.Error as e:
                return (f"Error al solicitar la información: {e}", "dataBaseError", 500)

def eliminar(id_paciente):
    pass

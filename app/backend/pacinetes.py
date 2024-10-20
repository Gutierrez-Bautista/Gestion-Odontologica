import sqlite3
import tablas


DB_NAME = 'app/clinica.db'


#alta
def alta_paciente(nombre_apellido,telefono,email,edad,dni,domicilio,fecha_nacimiento,posee_pami):
    print(nombre_apellido,telefono,email,edad,dni,domicilio,fecha_nacimiento,posee_pami)
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM Pacientes where nombre_apellido = ?"
        cursor.execute(query, (nombre_apellido,))
        valid = cursor.fetchall()
        if not valid:
            cursor.execute('insert into Pacientes (nombre_apellido,telefono,email,edad,dni,domicilio,fecha_nacimiento,posee_pami) values(?,?,?,?,?,?,?,?)',(nombre_apellido,telefono,email,edad,dni,domicilio,fecha_nacimiento,posee_pami))
            valid = cursor.fetchall()
            return ['paciente cargado','dataUpload',200]
        else: 
            cursor.execute('update table Pacientes set nombre_apellido = ? ,telefono = ? ,email = ? ,edad = ? ,dni = ? ,domicilio = ? ,fecha_nacimiento = ? ,posee_pami = ? where nombre_apellido = ?', (nombre_apellido,telefono,email,edad,dni,domicilio,fecha_nacimiento,posee_pami,nombre_apellido))
            valid = cursor.fetchall()
            return ['paciente actualizado','dataUpload',200]
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)

#consulta por nombre ==> listo
#consulta por id ==> listo
#consulta por pami ==> listo


def consul_pacente (id_paciente, nom_paciente, pami_paciente):
    # print(id_paciente, nom_paciente, pami_paciente)
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
                    return ['cliente encontrado', valid[0], 200]
            elif nom_paciente is not None:
                cursor.execute(query + 'where nombre_apellido =?',(nom_paciente,))
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

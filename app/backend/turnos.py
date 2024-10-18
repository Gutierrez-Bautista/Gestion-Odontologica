import sqlite3
import tablas

DB_NAME = 'app/clinica.db'

def solicitar_info(fecha_turno1, fecha_turno2):
    """
    Solicita información de un turno específico según la fecha proporcionada.
    """
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "SELECT * FROM turnos WHERE fecha between ? and ? order by horario, fecha"
        cursor.execute(query, (fecha_turno1, fecha_turno2))
        resultados = cursor.fetchall()

        if resultados:
            res = []
            for r in resultados:
                cursor.execute('select nombre_apellido from Pacientes where id = ?', (r[1],))
                paciente = cursor.fetchall()
                a = list(r)
                a.append(paciente[0][0])
                res.append(a)
            cursor.close()
            connection.close()
            return (res, 'dataFound', 200)
        else:
            cursor.close()
            connection.close()
            return ("N/A", "noDataFound", 403)
            #return f"No se encontraron turnos para la fecha {fecha_turno}."
            pass
    except sqlite3.Error as e:
        return (f"Error al solicitar la información: {e}", "dataBaseError", 500)

def solicitar_info_turno_id (turno_id):
    return (f'Aun no se ha creado la funcionalidad', 'inDevelopment', 404)

def agregar_info(nombre, fecha, hora, motivo):
    """
    Agrega un nuevo turno a la base de datos.
    """
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("select * from turnos where fecha = ? and horario = ?", (fecha, hora))
        valid = cursor.fetchall()
        if len(valid) == 0:
            q = "select * from Pacientes where nombre_apellido = ?"
            cursor.execute(q, (nombre,))
            res = cursor.fetchall()
            if len(res) == 0:
                cursor.execute("insert into Pacientes (nombre_apellido) values (?)", (nombre,))
                connection.commit()
                cursor.execute("select max(id) from Pacientes")
                paciente_id = cursor.fetchall()[0][0]
            else:
                paciente_id = res[0][0]
            query = "INSERT INTO turnos (paciente_id, fecha, horario, motivo) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (paciente_id, fecha, hora, motivo))
            connection.commit()
            cursor.close()
            connection.close()
            return ["Turno agregado exitosamente.", "dataUploaded", 200]
        else:
            return ["El horario de ese turno ya esta ocupado", "dataNoUpload", 200]
        
    except sqlite3.Error as e:
        return (f"Error al agregar el turno: {e}", f"dataBaseError", 500)


def eliminar_turno_por_fecha(fecha_turno, t_horario):
    """
    Elimina un turno según la fecha proporcionada.
    """
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        query = "DELETE FROM turnos WHERE fecha = ? and horario = ?"
        cursor.execute(query, (fecha_turno,t_horario))
        connection.commit()

        if cursor.rowcount > 0:
            resultado = [f"Turnos eliminados para la fecha {fecha_turno} {t_horario}.", "dataDeleted", 200]
        else:
            resultado = [f"No se encontraron turnos para la fecha {fecha_turno} {t_horario}.", "noDataFound", 403]

        cursor.close()
        connection.close()

        return resultado

    except sqlite3.Error as e:
        return (f"Error al eliminar los turnos: {e}", "dataBaseError", 500)

def actualizar_turno_por_fecha (datos_actuales, nuevos_datos):
    # [fecha_actual, horario_actual, motivo_actual]
    # [nueva_fecha, nuevo_horario, nuevo_motivo]
    for i in range(len(datos_actuales)):
        if nuevos_datos[i] == '': nuevos_datos[i] = datos_actuales[i]
    print(datos_actuales)
    print(nuevos_datos)
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        query = "update turnos set fecha=?, horario=?, motivo=? WHERE fecha = ? and horario = ?"
        cursor.execute(query, (nuevos_datos[0], nuevos_datos[1], nuevos_datos[2], datos_actuales[0], datos_actuales[1]))
        connection.commit()

        if cursor.rowcount > 0:
            resultado = [f"Turno de la fecha {datos_actuales[0]} {datos_actuales[1]} modificado.", "dataUpdated", 200]
        else:
            resultado = [f"No se encontro turno para la fecha {datos_actuales[0]} {datos_actuales[1]}.", "noDataFound", 403]
        
        cursor.close()
        connection.close()

        return resultado
    except sqlite3.Error as e:
        return (f"Error al modificar el turno: {e}", "dataBaseError", 500)
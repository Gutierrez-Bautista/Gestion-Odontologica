import sqlite3
import tablas

DB_NAME = 'clinica.db'

def solicitar_info(fecha_turno1, fecha_turno2):
    """
    Solicita información de un turno específico según la fecha proporcionada.
    """
    try:

        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        query = "SELECT * FROM turnos WHERE fecha between fecha_turno1 and fecha_turno2"
        cursor.execute(query, (fecha_turno1,fecha_turno2))
        resultados = cursor.fetchall()
        cursor.close()
        connection.close()
        if resultados:
            return resultados
        else:
            #return f"No se encontraron turnos para la fecha {fecha_turno}."
            pass
    except sqlite3.Error as e:
        return f"Error al solicitar la información: {e}"


def agregar_info(nombre, fecha, hora, motivo):
    """
    Agrega un nuevo turno a la base de datos.
    """
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("select * from turnos where fecha = ? and hora = ?", (fecha, hora))
        valid = cursor.fetchall()
        if len(valid) != 0:
            query = "INSERT INTO turnos (nombre, fecha, hora, motivo) VALUES (?, ?, ?,?)"
            cursor.execute(query, (nombre, fecha, hora))
            connection.commit()
            cursor.close()
            connection.close()
            return "Turno agregado exitosamente."
        else:
            return "El horario de ese turno ya esta ocupado"
        
    except sqlite3.Error as e:
        return f"Error al agregar el turno: {e}"


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
            resultado = f"Turnos eliminados para la fecha {fecha_turno}."
        else:
            resultado = f"No se encontraron turnos para la fecha {fecha_turno}."

        cursor.close()
        connection.close()

        return resultado

    except sqlite3.Error as e:
        return f"Error al eliminar los turnos: {e}"

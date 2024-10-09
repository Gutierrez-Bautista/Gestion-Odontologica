import sqlite3
import tablas

DB_NAME = 'clinica.db'

def solicitar_info(fecha_turno):
    """
    Solicita información de un turno específico según la fecha proporcionada.
    """
    try:

        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        query = "SELECT * FROM turnos WHERE fecha = ?"
        cursor.execute(query, (fecha_turno,))
        resultados = cursor.fetchall()
        cursor.close()
        connection.close()
        if resultados:
            return resultados
        else:
            return f"No se encontraron turnos para la fecha {fecha_turno}."

    except sqlite3.Error as e:
        return f"Error al solicitar la información: {e}"


def agregar_info(nombre, fecha, hora):
    """
    Agrega un nuevo turno a la base de datos.
    """
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = "INSERT INTO turnos (nombre, fecha, hora) VALUES (?, ?, ?)"
        cursor.execute(query, (nombre, fecha, hora))
        connection.commit()
        cursor.close()
        connection.close()

        return "Turno agregado exitosamente."
    
    except sqlite3.Error as e:
        return f"Error al agregar el turno: {e}"


def eliminar_turno_por_fecha(fecha_turno):
    """
    Elimina un turno según la fecha proporcionada.
    """
    try:

        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        query = "DELETE FROM turnos WHERE fecha = ?"
        cursor.execute(query, (fecha_turno,))
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

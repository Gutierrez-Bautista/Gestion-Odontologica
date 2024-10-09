import sqlite3


def agregar_paciente(name, password):
    with open("a.txt", mode="a") as archivo:
        archivo.write(f'{name};{password}\n')




# el frontend manda una fecha y el backend tiene que devolver los datos 

# id, fecha, hora, nombre, apellido

# tabla (BBDD) turnos: id, hora, fecha, id_paciente(nomb, ape)

# 1turno = btn => nombre y apellido
# id_turno, nombre, apellido



# manejar todo con diccionarios
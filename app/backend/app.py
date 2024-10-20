from flask import Flask, jsonify, request
from flask_cors import CORS
from webbrowser import open
import turnos
import pacinetes

app = Flask(__name__)
CORS(app)

@app.get('/api/data')
def data_get():
    return jsonify({
        'key': 'value'
        })

@app.post('/api/turnos/get')
def get_turnos ():
    fecha_turno1 = request.form['fecha_turno1']
    fecha_turno2 = request.form['fecha_turno2']

    soli = turnos.solicitar_info(fecha_turno1, fecha_turno2)

    return jsonify({
        "status": soli[2],
        "name": soli[1],
        "message": soli[0] #esto devuelve los resultados de la busqueda por fecha
    })

@app.post('/api/turnos/upload')
def upload_turno ():
    name = request.form.get("fullname")
    date = request.form.get("date")
    hour = request.form.get("hour")
    minute = request.form.get('minute')
    motivo = request.form.get('motivo')

    res = turnos.agregar_info(name, date, hour + ':' + minute, motivo.lower())

    return jsonify({
        "status": res[2],
        "name": res[1],
        "message": res[0]
    })

@app.delete('/api/turnos/delete')
def delete_turno ():
    hora = request.form.get('hour')
    dia = request.form.get('day')

    res = turnos.eliminar_turno_por_fecha(dia, hora)

    return jsonify({
        "status": res[2],
        "name": res[1],
        "message": res[0]
    })

@app.put('/api/turnos/update')
def update_turno():
    fecha_actual = request.form.get('fecha-actual')
    hora_actual = request.form.get('hora-actual')
    motivo_actual = request.form.get('motivo-actual')
    nueva_fecha = request.form.get('nueva-fecha')
    nueva_hora = request.form.get('nueva-hora')
    nuevo_motivo = request.form.get('nuevo-motivo')

    print(fecha_actual, hora_actual, nueva_fecha, nueva_hora, nuevo_motivo)

    res = turnos.actualizar_turno_por_fecha([fecha_actual, hora_actual, motivo_actual], [nueva_fecha, nueva_hora, nuevo_motivo])

    return jsonify({
        "status": res[2],
        "name": res[1],
        "message": res[0]
    })

@app.get('/api/pacientes/get')
def get_pacientes ():
    paciente_id = request.args.get('id_paciente')
    paciente_nom = request.args.get('nom_paciente')
    paciente_pami = request.args.get('pami')

    res = pacinetes.consul_pacente(paciente_id, paciente_nom, paciente_pami)

    return jsonify({
        "status": res[2],
        "name": res[1],
        "message": res[0]
    })

@app.post('/api/pacientes/alta')
def post_pacientes():
    nombre_apellido = request.form.get('nombre_apellido')
    telefono = request.form.get('telefono')
    email = request.form.get('email')
    edad = request.form.get('edad')
    dni = request.form.get('dni')
    domicilio = request.form.get('domicilio')
    fecha_nacimiento = request.form.get('fecha_nacimiento')
    posee_pami = request.form.get('posee_pami')

    print(request.form.to_dict())

    """
    Necesito que al alta se agreguen los datos de la ficha general, la ficha de PAMI, la anamnesis, el historial odontologico y el odontograma.
    Tanto los pacientes normales como aquellos con PAMI tienen un historial odontologico y un odontograma, no obstante, cada uno de ellos tiene su ficha correspondiente, los pacientes que poseen PAMI tienen una ficha de PAMI mientras que el resto tiene una ficha general.
    A continuacion se especifica el nombre con el que se pasan los datos desde el frontend junto con una descripcion de que se esta pasando y que tipo de datos son (todos son strings, cuando se dice que algo es un numero hace referencia a que el texto contiene solo numeros):

    datos ficha general:
      # obra-social (texto) --> puede estar vacio
      # n-afiliado (0 o mayor) --> numero de afiliado (puede estar vacio)
      # hta (0 o 1) --> si tiene hipertension arterial o no
      # diabetes (0 o 1) --> si tiene diabetes o no
      # alergias (texto) --> alergias del paciente (puede estar vacio)
      # prob-renales (0 o 1) --> si tiene problemas renales o no
      # prob-cardiacos (0 o 1) --> si tiene problemas cardiacos o no
      # plan-tratamiento (texto) --> puede estar vacio
      # observaciones (texto) --> puede estar vacio

    datos de ficha pami:
      # lugar (texto) --> no se de que
      # fecha (dd/mm/aaaa) --> no se de que
      # n-beneficio --> numero de beneficio
      # titular (0 o 1) --> si es titular o no
      # parentesco (texto) --> (supongo que es entre el paciente y el titular de la obra social) (puede estar vacio)
      # loc-paciente (texto) --> localidad del paciente
      # cod-post-paciente (texto) --> codigo postal del paciente
      # profesional --> profesional
      # domicilio-prestador (texto)
      # loc-prestador --> localidad del prestador
    
    datos anamnesis:
      # sufre-enfermedad (0 o 1) --> si sufre alguna enfermedad o no
      # trat-med (texto) --> tratamiento medico (puede estar vacio)
      # medicacion (texto) --> medicacion que toma (puede estar vacio)
      # alergias-drogas (texto) --> medicaciones a las que es alergico (puede estar vacio)
      # cant-fuma (0 o mayor) --> cantidad que fuma
      # diabetes (0 o 1) --> si tiene diabetes o no
      # hta (0 o 1) --> si tiene hipertension arterial o no
      # aspi-antcuag (0 o 1) --> si toma aspirinas.anticuagulantes o no
      # operado (0 o 1) --> si ha sido operado
    
    datos historia clinica odontologica:
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
    
    Estos son solo los datos puntuales de las tablas especificadas anteriormente, no obstante en algunas de ellas tambien deben cargarse datos que estan el la tabla de pacientes.

    Cuando el paciente que se esta cargando es de PAMI no se pasan los datos de la ficha general mientras que si el paciente no posee PAMI no se pasan datos de la ficha PAMI ni de la anamnesis
    """

    res = pacinetes.alta_paciente(nombre_apellido,telefono,email,edad,dni,domicilio,fecha_nacimiento,posee_pami)

    return jsonify({
        "status": res[2],
        "name": res[1],
        "message": res[0]
    })

if __name__ == '__main__':
    # open('app/frontend/index.html', 2)
    app.run(debug = True, port = 8000, use_reloader = False)

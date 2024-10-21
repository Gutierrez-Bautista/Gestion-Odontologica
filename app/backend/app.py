from flask import Flask, jsonify, request
from flask_cors import CORS
from webbrowser import open
import turnos
import pacinetes
import sqlite3

app = Flask(__name__)
CORS(app)
DB_NAME = 'app/clinica.db'
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

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('select id from pacientes where nombre_apellido = ?',(nombre_apellido))
    id_paciente = cursor.fetchall()[0][0]  #obtengo el id del paciente en cuestion


    telefono = request.form.get('telefono')
    email = request.form.get('email')
    edad = request.form.get('edad')
    dni = request.form.get('dni')
    domicilio = request.form.get('domicilio')
    fecha_nacimiento = request.form.get('fecha_nacimiento')
    posee_pami = request.form.get('posee_pami')

    print(request.form.to_dict())

    #----datos de la ficha de pami----#

    lugar = request.form.get('lugar')
    fecha = request.form.get('fecha')
    nro_beneficio = request.form.get('n-beneficio')
    titular,parentesco = request.form.get('titular')
    localidad_paciente = request.form.get('parentesco')
    codigo_postal_paciente = request.form.get('loc-paciente')
    profesional = request.form.get('cod-post-paciente')
    domicilio_prestador = request.form.get('profesional')
    localidad_prestador = request.form.get('domicilio-prestador')
    medico_cabecera = request.form.get('loc-prestador')

    datos_ficha_pami = (lugar,fecha,nro_beneficio,titular,parentesco,localidad_paciente,codigo_postal_paciente,profesional,domicilio_prestador, localidad_prestador,medico_cabecera)

    #----datos de la anamnesis----#   

    enfermedad = request.form.get ('sufre-enfermedad')
    tratamiento_medico = request.form.get ('trat-med')
    medicacion = request.form.get ('medicacion')
    alergia_droga = request.form.get ('alergias-drogas')
    diabetes1 = request.form.get ('diabetes')
    cantidad_fuma = request.form.get ('cant-fuma')
    probl_cardiacos1 = request.form.get ('probl-cardiacos')
    hipertension = request.form.get ('hta')
    toma_aspirina_anticoagulantes = request.form.get ('aspi-antcuag')
    fue_operado = request.form.get ('operado')

    anamnesis = (enfermedad,tratamiento_medico,medicacion,alergia_droga,diabetes1,cantidad_fuma,probl_cardiacos1,hipertension,toma_aspirina_anticoagulantes,fue_operado)

    #----datos de la ficha general----#
    obra_social = request.form.get ('obra-social')
    nro_afiliado = request.form.get ('n-afiliado')
    hta = request.form.get ('hta')
    diabetes = request.form.get ('diabetes')
    alergia = request.form.get ('alergias')
    probl_renales = request.form.get ('prob-renales')
    probl_cardiacos = request.form.get ('prob-cardiacos')
    plan_tratamiento = request.form.get ('plan-tratamiento')
    observaciones = request.form.get ('observaciones')

    datos_ficha_general=(obra_social,nro_afiliado,hta,diabetes,alergia,probl_renales,probl_cardiacos,plan_tratamiento,observaciones)

    #----historial clinico odontologico 

    motivo_consulta = request.form.get ('motivo-consulta')
    consulta_reciente = request.form.get ('consulta-otro-prof')
    dificultad_masticar = request.form.get ('dif-masticar')
    dificultad_hablar = request.form.get ('dif-hablar')
    movilidad_dentaria = request.form.get ('mov-dental')
    sangrado_encias = request.form.get ('sang-encias')
    cantidad_cepillados_diarios = request.form.get ('cant-sepillados')
    momentos_azucar = request.form.get ('azucar')

    historia_clinica = (motivo_consulta,consulta_reciente,dificultad_masticar,dificultad_hablar,movilidad_dentaria,sangrado_encias,cantidad_cepillados_diarios,momentos_azucar)

    #----datos del odontograma----#

    estado = request.form.get ('estado-odontograma')
    tratamiento = request.form.get ('tratamiento-odontograma')

    odontograma = (estado,tratamiento)

    res = pacinetes.alta_paciente(nombre_apellido,telefono,email,edad,dni,domicilio,fecha_nacimiento,posee_pami, datos_ficha_pami,anamnesis)

    return jsonify({
        "status": res[2],
        "name": res[1],
        "message": res[0]
    })

if __name__ == '__main__':
    # open('app/frontend/index.html', 2)
    app.run(debug = True, port = 8000, use_reloader = False)

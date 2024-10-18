from flask import Flask, jsonify, request
from flask_cors import CORS
from webbrowser import open
import turnos

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

if __name__ == '__main__':
    # open('app/frontend/index.html', 2)
    app.run(debug = True, port = 8000, use_reloader = False)

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

    res = turnos.agregar_info(name, date, hour + ':' + minute, motivo)

    return jsonify({
        "status": res[2],
        "name": res[1],
        "message": res[0]
    })

if __name__ == '__main__':
    # open('app/frontend/index.html', 2)
    app.run(debug = True, port = 8000, use_reloader = False)

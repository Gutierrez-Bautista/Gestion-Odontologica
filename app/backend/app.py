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

@app.post('/api/enviar')
def env():
    fecha_turno = request.form['fecha_turno']
    #password = request.form['password']

    soli = turnos.solicitar_info(fecha_turno)


    return jsonify({
        "status": 200,
        "name": soli[1],
        "message": soli[0] #esto devuelve los resultados de la busqueda por fecha
    })

if __name__ == '__main__':
    open('app/frontend/index.html', 2)
    app.run(debug = True, port = 8000, use_reloader = False)

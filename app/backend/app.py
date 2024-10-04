from flask import Flask, jsonify, request
from flask_cors import CORS
from webbrowser import open
import database_manager

app = Flask(__name__)
CORS(app)

@app.get('/api/data')
def data_get():
    return jsonify({
        'key': 'value'
        })

@app.post('/api/enviar')
def env():
    name = request.form['user']
    password = request.form['password']

    database_manager.agregar_paciente(name, password)

    return jsonify({
        "status": 200,
        "message": f"user {name} register with password {password}"
    })

if __name__ == '__main__':
    open('frontend\index.html', 2)
    app.run(debug = True, port = 8000, use_reloader = False)

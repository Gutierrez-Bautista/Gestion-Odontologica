import sqlite3
import asyncio

# Conexión a la base de datos (se crea si no existe)
def conectar_bd():
    conn = sqlite3.connect('clinica.db')  # Nombre de la base de datos
    return conn

# Función para crear las tablas

conn = conectar_bd()
cursor = conn.cursor()

# Crear tabla Pacientes
async def pacientes ():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_apellido TEXT NOT NULL,
            telefono TEXT,
            email TEXT,
            edad INTEGER,
            dni TEXT NOT NULL UNIQUE,
            domicilio TEXT,
            fecha_nacimiento DATE,
            posee_pami BOOLEAN
        )
        ''')

# Crear tabla Turnos
async def turnos():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Turnos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        fecha DATE NOT NULL,
        horario TEXT NOT NULL,
        motivo TEXT,
        FOREIGN KEY (paciente_id) REFERENCES Pacientes(id)
    )
    ''')

# Crear tabla HistoriaClinica (para tratamientos hechos al paciente)
async def HistoriaClinica ():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS HistoriaClinica (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        fecha DATE NOT NULL,
        descripcion TEXT NOT NULL,
        FOREIGN KEY (paciente_id) REFERENCES Pacientes(id)
    )
    ''')

# Crear tabla FichaGeneral
async def FichaGeneral ():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS FichaGeneral (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_apellido TEXT NOT NULL,
        dni TEXT NOT NULL UNIQUE,
        obra_social TEXT,
        nro_afiliado TEXT,
        fecha_nacimiento DATE,
        edad INTEGER,
        domicilio TEXT,
        telefono TEXT,
        planilla_cara_dientes TEXT,
        hta BOOLEAN,
        diabetes BOOLEAN,
        alergia BOOLEAN,
        detalles_alergia TEXT,
        probl_reales BOOLEAN,
        probl_cardiacos BOOLEAN,
        plan_tratamiento TEXT,
        observaciones TEXT,
        firma_paciente BOOLEAN,
        firma_profesional BOOLEAN
    )
    ''')

# Crear tabla FichaPAMI
async def FichaPAMI ():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS FichaPAMI (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lugar TEXT,
        fecha DATE,
        nro_beneficio TEXT,
        nro_documento TEXT NOT NULL UNIQUE,
        fecha_nacimiento DATE,
        apellido_nombre TEXT,
        titular BOOLEAN,
        parentesco TEXT,
        localidad_paciente TEXT,
        codigo_postal_paciente TEXT,
        telefono_paciente TEXT,
        profesional TEXT,
        domicilio_prestador TEXT,
        localidad_prestador TEXT,
        telefono_fijo_prestador TEXT,
        codigo_prestador TEXT,
        medico_cabecera TEXT
    )
    ''')

# Crear tabla Anamnesis
async def Anamnesis ():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Anamnesis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ficha_pami_id INTEGER,
        enfermedad BOOLEAN,
        tratamiento_medico BOOLEAN,
        detalles_tratamiento TEXT,
        medicacion BOOLEAN,
        detalles_medicacion TEXT,
        alergia_droga BOOLEAN,
        detalles_alergia_droga TEXT,
        diabetes BOOLEAN,
        fuma BOOLEAN,
        cantidad_fuma INTEGER,
        probl_cardiacos BOOLEAN,
        hipertension BOOLEAN,
        toma_aspirina_anticoagulantes BOOLEAN,
        fue_operado BOOLEAN,
        FOREIGN KEY (ficha_pami_id) REFERENCES FichaPAMI(id)
    )
    ''')

# Crear tabla HistoriaClinicaPAMI
async def HistoriaClinicaPAMI ():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS HistoriaClinicaPAMI (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ficha_pami_id INTEGER,
        motivo_consulta TEXT,
        consulta_reciente BOOLEAN,
        dificultad_masticar BOOLEAN,
        dificultad_hablar BOOLEAN,
        movilidad_dentaria BOOLEAN,
        sangrado_encias BOOLEAN,
        cantidad_cepillados_diarios INTEGER,
        momentos_azucar TEXT,
        FOREIGN KEY (ficha_pami_id) REFERENCES FichaPAMI(id)
    )
    ''')

# Crear tabla Odontograma
async def odontograma ():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Odontograma (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        diente TEXT NOT NULL,
        estado TEXT NOT NULL,
        tratamiento TEXT,
        FOREIGN KEY (paciente_id) REFERENCES Pacientes(id)
    )
    ''')

# Crear tabla Estadisticas
async def estadisticas():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Estadisticas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        fecha DATE NOT NULL,
        descripcion TEXT NOT NULL,
        valor INTEGER,
        FOREIGN KEY (paciente_id) REFERENCES Pacientes(id)
    )
    ''')

# Crear tabla Servicios
async def servicios ():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Servicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_servicio TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        costo REAL
    )
    ''')

def fin ():
    conn.commit()
    print("Tablas creadas con éxito.")

    conn.close()

async def main():
    # Ejecutar varias tareas en paralelo y esperar a que todas terminen
    asyncio.gather(
        pacientes (),
        turnos (),
        HistoriaClinica (),
        FichaGeneral (),
        FichaPAMI (),
        Anamnesis (),
        HistoriaClinicaPAMI (),
        odontograma (),
        estadisticas (),
        servicios (),
    )
    fin()

asyncio.run(main())
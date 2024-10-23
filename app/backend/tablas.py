import aiosqlite
import asyncio
import time

# Crear tabla Pacientes
async def pacientes(conn):
    async with conn.cursor() as cursor:
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS Pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_apellido TEXT NOT NULL,
                telefono TEXT,
                email TEXT,
                edad INTEGER,
                dni TEXT UNIQUE,
                domicilio TEXT,
                fecha_nacimiento DATE,
                posee_pami BOOLEAN
            )''')

# Crear tabla Turnos
async def turnos(conn):
    async with conn.cursor() as cursor:
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS Turnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            fecha DATE NOT NULL,
            horario TEXT NOT NULL,
            motivo TEXT,
            FOREIGN KEY (paciente_id) REFERENCES Pacientes(id)
        )''')

# Crear tabla HistoriaClinica
async def HistoriaClinica(conn):
    async with conn.cursor() as cursor:
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS HistoriaClinica (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            fecha DATE NOT NULL,
            descripcion TEXT NOT NULL,
            FOREIGN KEY (paciente_id) REFERENCES Pacientes(id)
        )''')

# Crear tabla FichaGeneral
async def FichaGeneral(conn):
    async with conn.cursor() as cursor:
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS FichaGeneral (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER NOT NULL,
            obra_social TEXT,
            nro_afiliado TEXT,
            hta BOOLEAN,
            diabetes BOOLEAN,
            alergia TEXT,
            probl_renales BOOLEAN,
            probl_cardiacos BOOLEAN,
            plan_tratamiento TEXT,
            observaciones TEXT
        )''')

# Crear tabla FichaPAMI
async def FichaPAMI(conn):
    async with conn.cursor() as cursor:
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS FichaPAMI (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER NOT NULL,
            lugar TEXT,
            fecha DATE,
            nro_beneficio TEXT,
            titular BOOLEAN,
            parentesco TEXT,
            localidad_paciente TEXT,
            codigo_postal_paciente TEXT,
            profesional TEXT,
            domicilio_prestador TEXT,
            localidad_prestador TEXT,
            codigo_prestador TEXT,
            medico_cabecera TEXT,
            tel_fijo_prestador text
        )''')

# Crear tabla Anamnesis
async def Anamnesis(conn):
    async with conn.cursor() as cursor:
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS Anamnesis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ficha_pami_id INTEGER,
            enfermedad BOOLEAN,
            tratamiento_medico TEXT,
            medicacion TEXT,
            alergia_droga text,
            diabetes BOOLEAN,
            cantidad_fuma INTEGER,
            probl_cardiacos BOOLEAN,
            hipertension BOOLEAN,
            toma_aspirina_anticoagulantes BOOLEAN,
            fue_operado BOOLEAN,
            FOREIGN KEY (ficha_pami_id) REFERENCES FichaPAMI(id)
        )''')

# Crear tabla HistoriaClinica
async def HistoriaClinicaOdontologica(conn):
    async with conn.cursor() as cursor:
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS HistoriaClinicaOdontologica (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            motivo_consulta TEXT,
            consulta_reciente BOOLEAN,
            dificultad_masticar BOOLEAN,
            dificultad_hablar BOOLEAN,
            movilidad_dentaria BOOLEAN,
            sangrado_encias BOOLEAN,
            cantidad_cepillados_diarios INTEGER,
            momentos_azucar TEXT,
            descripcion TEXT,
            FOREIGN KEY (paciente_id) REFERENCES Pacientes(id)
        )''')

# Crear tabla Odontograma
async def odontograma(conn):
    async with conn.cursor() as cursor:
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS Odontograma (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            estado TEXT,
            tratamiento TEXT,
            FOREIGN KEY (paciente_id) REFERENCES Pacientes(id)
        )''')

# Crear tabla Estadisticas
async def estadisticas(conn):
    async with conn.cursor() as cursor:
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS Estadisticas (
            fecha DATE NOT NULL,
            descripcion TEXT NOT NULL,
            valor INTEGER
        )''')

# Crear tabla Servicios
async def servicios(conn):
    async with conn.cursor() as cursor:
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS Servicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_servicio TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            costo float
        )''')

# Función para confirmar los cambios y cerrar la conexión
async def fin(conn):
    await conn.commit()
    await conn.close()
    print("Tablas creadas con éxito.")

# Función principal asincrónica
async def main():
    async with aiosqlite.connect('app/clinica.db') as conn:
        # Ejecutar todas las tareas asincrónicamente
        await asyncio.gather(
            pacientes(conn),
            turnos(conn),
            HistoriaClinica(conn),
            HistoriaClinicaOdontologica(conn),
            FichaGeneral(conn),
            FichaPAMI(conn),
            Anamnesis(conn),
            odontograma(conn),
            estadisticas(conn),
            servicios(conn)
        )
        await fin(conn)

# Ejecutar el código asincrónicamente
asyncio.run(main())
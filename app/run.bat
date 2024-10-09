@echo off
:: Nombre del entorno virtual
set VENV_NAME=venv

:: Crear el entorno virtual
python -m venv %VENV_NAME%

:: Activar el entorno virtual
call %VENV_NAME%\Scripts\activate

:: Confirmación de activación
echo Entorno virtual %VENV_NAME% creado y activado.
C:\Users\User\Documents\6C\programacion\gestion-odontologica\app

:: Instalar dependencias si existe el archivo requirements.txt
if exist requirements.txt (
    echo Instalando dependencias desde requirements.txt...
    pip install -r requirements.txt
) else (
    echo No se encontro el archivo requirements.txt, instalando paquetes predeterminados...
    pip install flask flask-cors aiosqlite
    pip freeze > requirements.txt
)

:: Confirmación de instalación
echo Dependencias instaladas correctamente.

:: Pausa para mantener la ventana abierta
pause

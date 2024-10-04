@echo off

:: Activar el entorno virtual
call venv\Scripts\activate

:: Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt

:: Iniciar la aplicación Flask
echo Iniciando la aplicación Flask...
python app.py

:: Mantener la ventana abierta
pause

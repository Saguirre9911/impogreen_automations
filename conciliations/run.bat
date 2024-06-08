@echo off
REM Activar el entorno virtual de Python
call myenv\Scripts\activate

REM Instalar dependencias
pip install -r requirements.txt

REM Ejecutar el script de Python
python transform_csv_consi.py

REM Pausar para ver los logs
echo.
echo El script ha terminado de ejecutarse. Presiona cualquier tecla para cerrar esta ventana.
pause >nul

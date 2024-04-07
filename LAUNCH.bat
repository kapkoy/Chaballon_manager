@echo off
start http://127.0.0.1:8000/
call _files\venv\Scripts\activate.bat

cd _files
echo Tu peux me fermer ;)
pythonw app.pyw
exit
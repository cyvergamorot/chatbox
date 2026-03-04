@echo off
cd /d c:\Users\Eli\chatbot\backend
"C:\Users\Eli\AppData\Local\Python\bin\python.exe" -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
pause

@echo off
call venv\Scripts\activate
python -m uvicorn src.api.main:app --reload
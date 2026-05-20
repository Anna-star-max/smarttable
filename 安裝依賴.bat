@echo off
title SmartTable - 安裝依賴
color 0A

echo ========================================
echo   SmartTable 依賴套件安裝程式
echo ========================================
echo.

cd /d "%~dp0"

REM 檢查 pip
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] pip 未安裝，請先安裝 Python 3.9+
    echo 官網下載：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [安裝中] FastAPI 與相關套件...
pip install fastapi uvicorn python-dotenv httpx

echo [安裝中] AI API 與資料處理...
pip install minimax openai pandas openpyxl python-docx pdfplumber

echo [安裝中] 檔案處理與 OCR...
pip install python-multipart rapidocr-onnxruntime Pillow

echo.
echo ========================================
echo   依賴安裝完成！
echo ========================================
echo.
echo 請確認已將 .env.example 複製為 .env 並填入 API Key
echo.
echo 按任意鍵繼續...
pause >nul
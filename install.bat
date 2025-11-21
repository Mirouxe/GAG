@echo off
REM Script d'installation automatique pour Windows
REM Usage: Double-cliquez sur install.bat

echo ================================================================
echo   Installation de ICG - Generateur de Graphiques
echo ================================================================
echo.

REM Verifier que Python est installe
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe !
    echo Telechargez Python sur : https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python trouve
echo.

REM Creer l'environnement virtuel
echo Creation de l'environnement virtuel...
python -m venv venv

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer les dependances
echo Installation des bibliotheques (peut prendre 2-5 minutes)...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ================================================================
echo   Installation terminee avec succes !
echo ================================================================
echo.
echo [IMPORTANT] Configuration requise
echo.
echo 1. Creez le fichier .streamlit\secrets.toml avec :
echo    OPENAI_API_KEY = "votre-cle-api"
echo    LLM_MODEL = "gpt-4o-mini"
echo.
echo 2. Pour lancer l'application :
echo    venv\Scripts\activate
echo    streamlit run app.py
echo.
echo Consultez GUIDE_TRANSFERT.md pour plus d'informations
echo ================================================================
pause


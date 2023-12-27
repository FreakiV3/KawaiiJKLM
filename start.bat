@echo off

REM Vérifier si le fichier dependencies.json existe
if not exist dependencies.json (
    echo { "dependencies_installed": false } > dependencies.json
)

REM Lecture du fichier JSON
for /f "tokens=2 delims=:}" %%a in ('type dependencies.json') do set "dep_status=%%a"

REM Vérification si les dépendances sont installées
if /i "%dep_status%"=="false" (
    echo Vérification des dépendances...
    echo Veuillez patienter...

    REM Installation des dépendances
    pip install pynput pyautogui pyperclip colorama python-osc

    REM Mise à jour du statut dans le fichier JSON
    echo { "dependencies_installed": true } > dependencies.json

    echo Dépendances installées avec succès!
)

REM Annimation du titre
title Kawaii KRNL / FreakiV3

REM Lancement du script principal
python main.py

pause

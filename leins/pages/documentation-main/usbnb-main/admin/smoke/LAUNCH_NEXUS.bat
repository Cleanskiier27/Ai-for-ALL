@echo off
title NETWORKBUSTER M2M NEXUS - FULL STACK LAUNCHER
color 0b

echo.
echo  ███╗   ██╗███████╗████████╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗
echo  ████╗  ██║██╔════╝╚══██╔══╝██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝
echo  ██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║██║   ██║██████╔╝█████╔╝
echo  ██║╚██╗██║██╔══╝     ██║   ██║███╗██║██║   ██║██╔══██╗██╔═██╗
echo  ██║ ╚████║███████╗   ██║   ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗
echo  ╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
echo.
echo  MOON 2 MARS DEEP SPACE AI NETWORK - CISLUNAR NEXUS
echo  ====================================================
echo.

set MIDDLEWARE=c:\leins\pages\documentation-main\usbnb-main\admin\smoke\server.py
set VITE_DIR=C:\Users\User\.gemini\antigravity\scratch\networkbuster-os-ui
set IP=192.168.1.14

echo [1/3] Starting Flask M2M Middleware on port 8080...
start "NB-M2M-Middleware" cmd /k "python %MIDDLEWARE%"
timeout /t 2 /nobreak > nul

echo [2/3] Starting Vite React Frontend on port 5173...
start "NB-M2M-Vite" cmd /k "cd /d %VITE_DIR% && npm run dev"
timeout /t 3 /nobreak > nul

echo [3/3] NETWORK ACCESS UPLINKS ESTABLISHED
echo.
echo  === ACCESS TERMINALS ===
echo.
echo  Vite UI (Local) :  http://localhost:5173
echo  Vite UI (Network): http://%IP%:5173
echo  Flask API       :  http://%IP%:8080/api/system-state
echo.
echo  Network devices can access the Nexus at: http://%IP%:5173
echo.
echo  Press any key to open the Nexus in your browser...
pause > nul

start http://localhost:5173

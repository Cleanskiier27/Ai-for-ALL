@echo off
title NetworkBuster OS Server Gateway
color 0b

echo ===================================================
echo     INITIALIZING NETWORKBUSTER OS PROTOCOLS...
echo ===================================================
echo.
echo Starting the Redundant Python Gateway Server...
echo The OS will be accessible on your local network at:
echo http://192.168.1.14:8080/
echo.
echo Press Ctrl+C to terminate the uplink.
echo.

python server.py

pause

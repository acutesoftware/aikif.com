@echo off
echo Starting web server for AIKIF

start python.exe aikif_web.py
echo Server started..
timeout 4
start  http://127.0.0.1:5000


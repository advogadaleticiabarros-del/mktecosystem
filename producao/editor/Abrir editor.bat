@echo off
title Editor de artes (deixe esta janela aberta)
cd /d "%~dp0"
python servidor.py
if errorlevel 1 pause

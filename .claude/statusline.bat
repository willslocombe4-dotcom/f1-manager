@echo off
setlocal enabledelayedexpansion

REM Get git branch if available
for /f "tokens=*" %%a in ('git rev-parse --abbrev-ref HEAD 2^>nul') do set BRANCH=%%a
if not defined BRANCH set BRANCH=no-git

REM Count Python files
set /a COUNT=0
for /r %%f in (*.py) do set /a COUNT+=1

echo F1 Manager ^| Branch: %BRANCH% ^| %COUNT% .py files

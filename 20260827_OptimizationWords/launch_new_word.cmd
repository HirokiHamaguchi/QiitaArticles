@echo off
REM Show only the CLI output, not each command being executed.

REM Use UTF-8 for the Japanese text printed by the Python CLI.
chcp 65001 >nul

REM Move to the repository so relative paths work when launched from Desktop.
REM /d also allows changing the current drive.
cd /d "C:\Users\hirok\Documents\QiitaArticles"

REM Run the CLI, rebuild the combined README, and then open Explorer.
".venv\Scripts\python.exe" "20260827_OptimizationWords\new_word.py" --open-explorer

REM Save Python's exit code before another command can overwrite it.
set "optimization_words_exit_code=%errorlevel%"

REM Zero means success. Keep the window open after an error or cancellation.
if not "%optimization_words_exit_code%"=="0" (
    echo.
    echo The operation did not complete. Check the message above.
    pause
)

REM Return Python's exit code to the caller and finish this batch file.
exit /b %optimization_words_exit_code%

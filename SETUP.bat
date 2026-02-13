@echo off
echo ============================================================
echo  First-Time Setup
echo ============================================================
echo.
echo Installing required Python package...
pip install markdown
echo.
echo Creating folder structure...
if not exist "content" mkdir content
if not exist "content\example" mkdir content\example
if not exist "docs" mkdir docs
if not exist "memory" mkdir memory
echo.
echo Done! Your folder structure is ready.
echo.
echo Next steps:
echo  1. Add your Markdown (.md) files to the CONTENT folder
echo  2. Double-click RUN.bat whenever you want to convert and publish
echo.
pause

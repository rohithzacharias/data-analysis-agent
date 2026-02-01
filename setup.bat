@echo off
REM Setup script for Data Analysis Agent (Windows)

echo 🧠 Data Analysis Agent - Setup Script
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    exit /b 1
)

echo ✓ Python found
for /f "tokens=*" %%i in ('python --version') do echo   %%i
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    exit /b 1
)
echo ✓ Virtual environment created
echo.

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo 📚 Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ Failed to install dependencies
    exit /b 1
)
echo.
echo ✓ Dependencies installed successfully

REM Run tests
echo.
echo 🧪 Running module tests...
python test_modules.py

if errorlevel 1 (
    echo.
    echo ⚠️  Setup completed but some tests failed.
    echo You may still be able to use the system.
) else (
    echo.
    echo ======================================
    echo 🎉 Setup completed successfully!
    echo ======================================
    echo.
    echo To get started:
    echo   1. Activate the virtual environment:
    echo      venv\Scripts\activate
    echo.
    echo   2. Run the demo notebook:
    echo      jupyter notebook examples\demo_analysis.ipynb
    echo.
    echo   3. Or use the CLI:
    echo      python cli.py sample titanic
    echo.
    echo   4. See QUICKSTART.md for more examples
    echo.
)

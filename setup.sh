#!/bin/bash

# Setup script for Data Analysis Agent
# This script sets up the virtual environment and installs dependencies

echo "🧠 Data Analysis Agent - Setup Script"
echo "======================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

if [ $? -eq 0 ]; then
    echo "✓ Virtual environment created"
else
    echo "❌ Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "📚 Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Dependencies installed successfully"
else
    echo ""
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Run tests
echo ""
echo "🧪 Running module tests..."
python test_modules.py

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "🎉 Setup completed successfully!"
    echo "======================================"
    echo ""
    echo "To get started:"
    echo "  1. Activate the virtual environment:"
    echo "     source venv/bin/activate"
    echo ""
    echo "  2. Run the demo notebook:"
    echo "     jupyter notebook examples/demo_analysis.ipynb"
    echo ""
    echo "  3. Or use the CLI:"
    echo "     python cli.py sample titanic"
    echo ""
    echo "  4. See QUICKSTART.md for more examples"
    echo ""
else
    echo ""
    echo "⚠️  Setup completed but some tests failed."
    echo "You may still be able to use the system."
fi

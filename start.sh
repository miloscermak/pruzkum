#!/bin/bash

echo "==================================="
echo "OSINT Deep Research Application"
echo "==================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  UPOZORNĚNÍ: Soubor .env neexistuje!"
    echo "📝 Vytvářím .env z .env.example..."
    cp .env.example .env
    echo "✅ Soubor .env vytvořen. Prosím, vyplňte svůj OpenAI API klíč!"
    echo ""
    read -p "Stiskněte Enter pro pokračování nebo Ctrl+C pro ukončení..."
fi

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Vytvářím virtuální prostředí..."
    python3 -m venv venv
    echo "✅ Virtuální prostředí vytvořeno"
fi

# Activate venv
echo "🔧 Aktivuji virtuální prostředí..."
source venv/bin/activate

# Install dependencies
echo "📥 Instaluji závislosti..."
pip install -q -r requirements.txt

echo ""
echo "🚀 Spouštím aplikaci..."
echo "📍 URL: http://localhost:8000"
echo "❌ Pro ukončení stiskněte Ctrl+C"
echo ""

# Run the application
python main.py

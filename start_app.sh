#!/bin/bash

# Script de lancement de l'application ICG

echo "🚀 Démarrage de l'application ICG..."

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
source venv/bin/activate

# Vérifier si les dépendances sont installées
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📦 Installation des dépendances..."
    pip install --upgrade pip
    pip install streamlit pandas numpy matplotlib langchain-openai openai openpyxl --no-deps
    pip install altair protobuf requests pillow==11.0.0 tornado watchdog click blinker cachetools jsonschema pytz tzdata python-dateutil et-xmlfile langchain-core tiktoken gitpython pydeck toml distro jiter tqdm contourpy cycler fonttools kiwisolver pyparsing
fi

echo ""
echo "✅ Application prête !"
echo ""
echo "📊 L'application sera accessible à l'adresse :"
echo "   👉 http://localhost:8501"
echo ""
echo "⚠️  N'oubliez pas de configurer votre clé API OpenAI dans:"
echo "   📝 .streamlit/secrets.toml"
echo ""
echo "Pour arrêter l'application, appuyez sur Ctrl+C"
echo ""

# Lancer Streamlit
streamlit run app.py


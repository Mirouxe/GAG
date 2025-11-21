#!/bin/bash
# Script d'installation automatique pour Mac/Linux
# Usage: ./install.sh

echo "════════════════════════════════════════════════════════════"
echo "  🚀 Installation de ICG - Générateur de Graphiques"
echo "════════════════════════════════════════════════════════════"
echo ""

# Vérifier que Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé !"
    echo "📥 Téléchargez Python sur : https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python trouvé : $(python3 --version)"
echo ""

# Créer l'environnement virtuel
echo "📦 Création de l'environnement virtuel..."
python3 -m venv venv

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📚 Installation des bibliothèques (peut prendre 2-5 minutes)..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  ✅ Installation terminée avec succès !"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "⚠️  IMPORTANT : Configuration requise"
echo ""
echo "1️⃣  Créez le fichier .streamlit/secrets.toml avec :"
echo "    OPENAI_API_KEY = \"votre-cle-api\""
echo "    LLM_MODEL = \"gpt-4o-mini\""
echo ""
echo "2️⃣  Pour lancer l'application :"
echo "    source venv/bin/activate"
echo "    streamlit run app.py"
echo ""
echo "📖 Consultez GUIDE_TRANSFERT.md pour plus d'informations"
echo "════════════════════════════════════════════════════════════"


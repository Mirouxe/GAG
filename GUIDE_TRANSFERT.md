# 📦 Guide de transfert vers un autre PC

## 📋 Fichiers à transférer

### ✅ Fichiers essentiels (OBLIGATOIRES)

Transférez ces fichiers dans un nouveau dossier sur l'autre PC :

```
ICG/
├── app.py                          # Application principale Streamlit
├── ICG_utils.py                    # Fonctions utilitaires
├── requirements.txt                # Liste des dépendances Python
├── README.md                       # Documentation du projet
├── donnees_test.csv               # Fichier de test (optionnel)
└── .streamlit/
    ├── secrets.toml               # ⚠️ IMPORTANT : Vos clés API
    └── config.toml                # Configuration Streamlit (optionnel)
```

### 📁 Fichiers optionnels

Ces fichiers peuvent être utiles mais ne sont pas obligatoires :

```
├── start_app.sh                   # Script de démarrage (Mac/Linux)
├── graphique.png                  # Exemple de sortie (pas nécessaire)
└── documentation/                 # Documentation supplémentaire
    ├── DEPLOIEMENT.md
    ├── EXEMPLES_DEMANDES.md
    └── autres fichiers .md
```

### ❌ Ne PAS transférer

- `venv/` : Environnement virtuel (à recréer sur le nouveau PC)
- `__pycache__/` : Cache Python (sera recréé automatiquement)
- `graphique.png` : Fichiers temporaires générés

---

## 🚀 Installation sur le nouveau PC

### Étape 1 : Prérequis

Assurez-vous d'avoir installé :
- **Python 3.8 ou supérieur** : Téléchargez sur [python.org](https://www.python.org/downloads/)
- **pip** : Normalement inclus avec Python

Pour vérifier :
```bash
python --version    # ou python3 --version
pip --version       # ou pip3 --version
```

### Étape 2 : Transférer les fichiers

**Option A : Via clé USB ou réseau**
- Copiez tous les fichiers listés ci-dessus dans un nouveau dossier sur le PC

**Option B : Via GitHub (recommandé)**
```bash
git clone https://github.com/VOTRE-USERNAME/VOTRE-REPO.git
cd VOTRE-REPO
```

### Étape 3 : Créer l'environnement virtuel

Sur le nouveau PC, ouvrez un terminal dans le dossier du projet :

**Sur Windows :**
```bash
python -m venv venv
venv\Scripts\activate
```

**Sur Mac/Linux :**
```bash
python3 -m venv venv
source venv/bin/activate
```

Vous devriez voir `(venv)` au début de votre ligne de commande.

### Étape 4 : Installer les dépendances

```bash
pip install -r requirements.txt
```

Cette commande va installer automatiquement :
- streamlit
- pandas
- numpy
- matplotlib
- seaborn
- langchain
- langchain-openai
- openai
- openpyxl

**⏱️ Temps d'installation : 2-5 minutes**

### Étape 5 : Configurer les secrets

Créez le dossier `.streamlit` s'il n'existe pas :

**Sur Windows :**
```bash
mkdir .streamlit
```

**Sur Mac/Linux :**
```bash
mkdir -p .streamlit
```

Créez le fichier `.streamlit/secrets.toml` avec ce contenu :

```toml
OPENAI_API_KEY = "votre-cle-api-openai-ici"
LLM_MODEL = "gpt-4o-mini"
```

⚠️ **IMPORTANT : Remplacez `votre-cle-api-openai-ici` par votre vraie clé API OpenAI !**

Si vous n'avez pas de clé API :
1. Allez sur [platform.openai.com](https://platform.openai.com/api-keys)
2. Créez un compte ou connectez-vous
3. Générez une nouvelle clé API
4. Copiez-la dans le fichier `secrets.toml`

### Étape 6 : Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse :
- http://localhost:8501

---

## 📦 Liste complète des bibliothèques

Ces bibliothèques seront installées automatiquement via `requirements.txt` :

| Bibliothèque | Version | Utilité |
|-------------|---------|---------|
| streamlit | ≥1.28.0 | Framework web pour l'interface |
| pandas | ≥2.0.0 | Manipulation de données CSV/XLSX |
| numpy | ≥1.24.0 | Calculs numériques |
| matplotlib | ≥3.7.0 | Génération de graphiques |
| seaborn | ≥0.12.0 | Graphiques statistiques élégants |
| langchain | ≥0.1.0 | Orchestration des agents IA |
| langchain-openai | ≥0.0.5 | Intégration OpenAI avec LangChain |
| openai | ≥1.0.0 | API OpenAI |
| openpyxl | ≥3.1.0 | Lecture de fichiers Excel |

---

## 🔧 Dépannage

### Problème : `command not found: python`
**Solution :** Essayez `python3` au lieu de `python`

### Problème : Erreur lors de l'installation de `matplotlib`
**Solution Windows :** Installez [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

### Problème : `No module named 'streamlit'`
**Solution :** Vérifiez que l'environnement virtuel est activé (vous devez voir `(venv)`)

### Problème : L'application ne démarre pas
**Solution :** 
1. Vérifiez que la clé API OpenAI est correcte dans `.streamlit/secrets.toml`
2. Vérifiez que tous les fichiers ont été transférés
3. Relancez l'installation : `pip install -r requirements.txt --force-reinstall`

### Problème : Erreur `API key not found`
**Solution :** Assurez-vous que le fichier `.streamlit/secrets.toml` existe et contient votre clé API

---

## ✅ Checklist de transfert

Avant de transférer, vérifiez que vous avez :

- [ ] Copié `app.py`
- [ ] Copié `ICG_utils.py`
- [ ] Copié `requirements.txt`
- [ ] Copié `.streamlit/secrets.toml` (avec votre clé API)
- [ ] Copié `README.md`
- [ ] Copié un fichier de test (ex: `donnees_test.csv`)
- [ ] Noté votre clé API OpenAI

Sur le nouveau PC :

- [ ] Python 3.8+ installé
- [ ] Environnement virtuel créé
- [ ] Dépendances installées
- [ ] Fichier `secrets.toml` configuré avec la clé API
- [ ] Application lancée avec succès

---

## 🎯 Résumé rapide

```bash
# 1. Transférer les fichiers
# 2. Sur le nouveau PC :
python3 -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
# 3. Créer .streamlit/secrets.toml avec votre clé API
# 4. Lancer
streamlit run app.py
```

---

## 💡 Astuce : Script d'installation automatique

Pour faciliter l'installation sur le nouveau PC, vous pouvez créer un script :

**`install.sh` (Mac/Linux) :**
```bash
#!/bin/bash
echo "🚀 Installation de l'application ICG..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "✅ Installation terminée !"
echo "⚠️  N'oubliez pas de configurer .streamlit/secrets.toml avec votre clé API"
echo "🎯 Lancez l'application avec : streamlit run app.py"
```

**`install.bat` (Windows) :**
```batch
@echo off
echo Installation de l'application ICG...
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
echo Installation terminee !
echo N'oubliez pas de configurer .streamlit\secrets.toml avec votre cle API
echo Lancez l'application avec : streamlit run app.py
pause
```

Rendez le script exécutable et lancez-le pour installer automatiquement !

---

**Besoin d'aide ? Consultez README.md pour plus d'informations.**


# ICG - Interactive Chart Generator 📊

Application web interactive permettant de générer et modifier des graphiques scientifiques en temps réel par dialogue avec un chatbot IA.

## Fonctionnalités

✨ **Upload de fichiers** : Support des fichiers CSV et Excel (XLSX)

💬 **Interface de chat intuitive** : Dialoguez naturellement pour créer et modifier vos graphiques

🔄 **Modifications en temps réel** : Voyez instantanément les changements appliqués à vos graphiques

🤖 **Système multi-agent intelligent** :
- **Interpréteur** : Analyse votre demande et la structure en JSON
- **Codeur** : Génère le code Python pour créer le graphique
- **Vérificateur** : S'assure de la cohérence du code
- **Debugger** : Corrige automatiquement les erreurs éventuelles

📥 **Export facile** : Téléchargez vos graphiques en PNG

## Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Clonez ou téléchargez ce dépôt**

2. **Installez les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurez vos secrets**

Éditez le fichier `.streamlit/secrets.toml` et ajoutez votre clé API OpenAI :

```toml
OPENAI_API_KEY = "sk-votre_clé_api_openai"
LLM_MODEL = "gpt-4o-mini"  # Ou "gpt-4", "gpt-3.5-turbo", etc.
```

💡 **Obtenir votre clé API OpenAI :**
- Rendez-vous sur [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- Créez un compte ou connectez-vous
- Générez une nouvelle clé API
- Copiez-la dans le fichier `secrets.toml`

## Utilisation

### Lancer l'application

**Option 1 : Script de lancement automatique (recommandé)**
```bash
./start_app.sh
```

**Option 2 : Lancement manuel**
```bash
source venv/bin/activate
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`.

⚠️ **Important** : N'oubliez pas de configurer votre clé API OpenAI dans `.streamlit/secrets.toml` avant la première utilisation !

### Guide d'utilisation

1. **Uploadez votre fichier de données** (CSV ou XLSX) dans la sidebar
2. **Décrivez le graphique** que vous souhaitez créer dans la zone de chat
3. **Visualisez le résultat** en temps réel dans la zone de droite
4. **Affinez votre graphique** en dialoguant avec l'assistant
5. **Téléchargez** le graphique final

### Exemples de demandes

- "Trace la température en fonction du temps"
- "Crée un graphique avec deux courbes : pression et volume"
- "Ajoute une légende et des unités sur les axes"
- "Change la couleur de la courbe en rouge"
- "Ajoute une barre verticale à t=10s"
- "Trace le carré de la température en fonction du temps"

## Structure du projet

```
ICG/
├── app.py                  # Application Streamlit principale
├── icg_webapp.py          # Script original (pipeline complet)
├── ICG_utils.py           # Fonctions utilitaires
├── requirements.txt       # Dépendances Python
├── .streamlit/
│   └── secrets.toml       # Configuration des secrets (à configurer)
└── README.md              # Ce fichier
```

## Architecture technique

L'application utilise un système multi-agent basé sur LangChain :

1. **Lecteur** : Analyse le fichier de données et extrait les métadonnées
2. **Interpréteur** : Convertit la demande utilisateur en structure JSON
3. **Codeur** : Génère le code Python avec matplotlib
4. **Vérificateur** : Valide la cohérence du code
5. **Debugger** : Corrige automatiquement les erreurs

## Technologies utilisées

- **Streamlit** : Framework pour l'interface web
- **LangChain** : Orchestration des agents IA
- **Pandas** : Manipulation des données
- **Matplotlib** : Génération des graphiques
- **NumPy** : Calculs scientifiques

## Licence

Ce projet est fourni à des fins éducatives et de recherche.

## Support

Pour toute question ou problème, veuillez créer une issue dans le dépôt du projet.

---

Développé avec ❤️ pour la communauté scientifique


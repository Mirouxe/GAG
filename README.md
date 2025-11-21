# 📊 Interactive Chart Generator (ICG)

Application web interactive pour générer et modifier des graphiques scientifiques à partir de fichiers de données, propulsée par l'intelligence artificielle.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)

## ✨ Fonctionnalités

- 🤖 **Génération automatique de code** : Décrivez le graphique en langage naturel, l'IA génère le code Python
- 🔄 **Modifications itératives** : Affinez votre graphique par dialogue avec le chatbot
- ✏️ **Édition manuelle** : Modifiez le code généré directement dans l'interface
- 📊 **Support multi-formats** : CSV et XLSX
- 🎨 **Visualisations avancées** : Matplotlib et Seaborn
- 💾 **Téléchargement** : Exportez vos graphiques en PNG

## 🚀 Installation rapide

### Prérequis
- Python 3.8+
- Clé API OpenAI

### Installation

```bash
# Cloner le repository
git clone https://github.com/VOTRE-USERNAME/icg-chart-generator.git
cd icg-chart-generator

# Installation automatique
./install.sh          # Mac/Linux
# ou
install.bat           # Windows
```

### Configuration

Créez le fichier `.streamlit/secrets.toml` :

```toml
OPENAI_API_KEY = "votre-cle-api-openai"
LLM_MODEL = "gpt-4o-mini"
```

### Lancement

```bash
source venv/bin/activate  # Mac/Linux (ou venv\Scripts\activate sur Windows)
streamlit run app.py
```

L'application sera accessible sur [http://localhost:8501](http://localhost:8501)

## 📖 Guide d'utilisation

1. **Upload de données** : Téléchargez votre fichier CSV ou XLSX dans la sidebar
2. **Première demande** : Décrivez le graphique souhaité (ex: "Trace la température en fonction du temps")
3. **Modifications** : Affinez le graphique en dialoguant avec le chatbot
4. **Édition manuelle** : Le code s'affiche automatiquement, vous pouvez le modifier
5. **Export** : Téléchargez votre graphique final

## 🏗️ Architecture

### Pipeline complète (première demande)
1. **Lecteur** : Analyse le fichier de données
2. **Interpréteur** : Comprend la demande utilisateur
3. **Codeur** : Génère le code Python
4. **Vérificateur** : Valide le code
5. **Debugger** : Corrige les erreurs si nécessaire

### Pipeline de modification (demandes suivantes)
1. **Modificateur** : Adapte le code existant selon la nouvelle demande
2. **Debugger** : Intervient si nécessaire

## 🛠️ Technologies utilisées

- **Frontend** : Streamlit
- **Visualisation** : Matplotlib, Seaborn
- **Data** : Pandas, NumPy
- **IA** : OpenAI GPT-4, LangChain
- **Langages** : Python 3.8+

## 📁 Structure du projet

```
ICG/
├── app.py                      # Application principale Streamlit
├── ICG_utils.py                # Fonctions utilitaires
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation complète
├── install.sh / install.bat    # Scripts d'installation
├── GUIDE_TRANSFERT.md          # Guide de déploiement
├── donnees_test.csv           # Fichier de test
├── .streamlit/
│   ├── config.toml            # Configuration Streamlit
│   └── secrets.toml.example   # Exemple de configuration des secrets
└── documentation/              # Documentation supplémentaire
```

## 🌐 Déploiement

### Streamlit Cloud (gratuit)

1. Créez un compte sur [share.streamlit.io](https://share.streamlit.io)
2. Connectez votre repository GitHub
3. Configurez les secrets (clé API OpenAI)
4. Déployez !

Consultez [documentation/DEPLOIEMENT.md](documentation/DEPLOIEMENT.md) pour le guide complet.

## 📚 Documentation

- **[GUIDE_TRANSFERT.md](GUIDE_TRANSFERT.md)** : Installation et transfert
- **[documentation/EXEMPLES_DEMANDES.md](documentation/EXEMPLES_DEMANDES.md)** : 50+ exemples de requêtes
- **[documentation/DEPLOIEMENT.md](documentation/DEPLOIEMENT.md)** : Guide de déploiement
- **[FICHIERS_A_TRANSFERER.txt](FICHIERS_A_TRANSFERER.txt)** : Checklist de transfert

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📄 Licence

Ce projet est sous licence MIT.

## 🙏 Remerciements

- [Streamlit](https://streamlit.io) pour le framework web
- [OpenAI](https://openai.com) pour les modèles de langage
- [LangChain](https://www.langchain.com) pour l'orchestration des agents

## 📞 Support

Pour toute question ou problème :
- Consultez la documentation
- Ouvrez une issue sur GitHub
- Consultez la [documentation Streamlit](https://docs.streamlit.io)

---

Fait avec ❤️ et 🤖


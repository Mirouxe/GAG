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

## 🚀 Déploiement sur Streamlit Cloud

Cette application est prête à être déployée sur Streamlit Cloud. Consultez [DEPLOIEMENT.md](DEPLOIEMENT.md) pour les instructions complètes.

### Configuration rapide

1. **Cloner ce repository**
```bash
git clone https://github.com/VOTRE-USERNAME/VOTRE-REPO.git
cd VOTRE-REPO
```

2. **Déployer sur Streamlit Cloud**
   - Allez sur [share.streamlit.io](https://share.streamlit.io)
   - Connectez-vous avec GitHub
   - Créez une nouvelle app en sélectionnant ce repository
   - Configurez les secrets :
     ```toml
     OPENAI_API_KEY = "votre-cle-api"
     LLM_MODEL = "gpt-4o-mini"
     ```

3. **C'est tout !** Votre app est en ligne 🎉

## 💻 Installation locale

### Prérequis
- Python 3.8+
- Clé API OpenAI

### Installation

```bash
# Cloner le repository
git clone https://github.com/VOTRE-USERNAME/VOTRE-REPO.git
cd VOTRE-REPO

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les secrets
mkdir -p .streamlit
echo 'OPENAI_API_KEY = "votre-cle-api"' > .streamlit/secrets.toml
echo 'LLM_MODEL = "gpt-4o-mini"' >> .streamlit/secrets.toml

# Lancer l'application
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
- **Langages** : Python 3.14+

## 📋 Configuration

### Variables d'environnement (Secrets)

```toml
OPENAI_API_KEY = "sk-..."  # Votre clé API OpenAI
LLM_MODEL = "gpt-4o-mini"   # Modèle à utiliser
```

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
- Consultez [DEPLOIEMENT.md](DEPLOIEMENT.md) pour les instructions de déploiement
- Ouvrez une issue sur GitHub
- Consultez la [documentation Streamlit](https://docs.streamlit.io)

---

Fait avec ❤️ et 🤖


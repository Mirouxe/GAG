# 🚀 Guide de déploiement sur Streamlit Cloud

## Prérequis
- Un compte GitHub
- Un compte Streamlit Cloud (gratuit sur [share.streamlit.io](https://share.streamlit.io))
- Votre clé API OpenAI

## Étape 1 : Préparer le repository GitHub

### 1.1 Créer un repository sur GitHub
1. Allez sur [github.com](https://github.com)
2. Cliquez sur "New repository"
3. Nommez-le par exemple `icg-chart-generator`
4. Choisissez "Public" (pour le plan gratuit de Streamlit Cloud)
5. Ne cochez pas "Add a README" (nous en avons déjà un)
6. Cliquez sur "Create repository"

### 1.2 Pousser votre code sur GitHub

Dans votre terminal, dans le dossier du projet :

```bash
# Initialiser Git (si pas déjà fait)
git init

# Ajouter tous les fichiers (le .gitignore exclura automatiquement les fichiers sensibles)
git add .

# Créer le premier commit
git commit -m "Initial commit - ICG Chart Generator"

# Ajouter le remote (remplacez USERNAME et REPO par vos valeurs)
git remote add origin https://github.com/USERNAME/REPO.git

# Pousser le code
git branch -M main
git push -u origin main
```

**IMPORTANT** : Vérifiez que `.streamlit/secrets.toml` n'est PAS poussé sur GitHub (il est dans `.gitignore`).

## Étape 2 : Déployer sur Streamlit Cloud

### 2.1 Se connecter à Streamlit Cloud
1. Allez sur [share.streamlit.io](https://share.streamlit.io)
2. Cliquez sur "Sign in with GitHub"
3. Autorisez Streamlit à accéder à vos repositories

### 2.2 Créer une nouvelle app
1. Cliquez sur "New app"
2. Sélectionnez votre repository GitHub
3. Branch : `main`
4. Main file path : `app.py`
5. Cliquez sur "Advanced settings..."

### 2.3 Configurer les secrets (IMPORTANT)
Dans "Secrets", ajoutez :

```toml
OPENAI_API_KEY = "votre-cle-api-openai-ici"
LLM_MODEL = "gpt-4o-mini"
```

**Remplacez `votre-cle-api-openai-ici` par votre vraie clé API OpenAI.**

### 2.4 Déployer
1. Cliquez sur "Deploy!"
2. Attendez quelques minutes (le déploiement initial peut prendre 3-5 minutes)
3. Votre app sera accessible à l'URL : `https://USERNAME-REPO-xxxxx.streamlit.app`

## Étape 3 : Utiliser votre application

Une fois déployée, vous pouvez :
- ✅ Partager l'URL avec qui vous voulez
- ✅ L'utiliser depuis n'importe où
- ✅ Uploader des fichiers CSV/XLSX
- ✅ Générer des graphiques interactifs

## 🔄 Mettre à jour l'application

Pour mettre à jour l'application après des modifications :

```bash
git add .
git commit -m "Description de vos modifications"
git push
```

Streamlit Cloud détectera automatiquement les changements et redéployera l'application !

## ⚙️ Gestion des secrets

Pour modifier les secrets (clé API, modèle, etc.) :
1. Allez sur [share.streamlit.io](https://share.streamlit.io)
2. Cliquez sur votre app
3. Menu "⋮" → "Settings"
4. Onglet "Secrets"
5. Modifiez et sauvegardez

## 🐛 Dépannage

### L'app ne démarre pas
- Vérifiez les logs dans l'interface Streamlit Cloud
- Assurez-vous que `requirements.txt` est à la racine
- Vérifiez que la clé API OpenAI est correcte dans les secrets

### Erreur de mémoire
- Streamlit Cloud offre 1GB de RAM en gratuit
- Utilisez `gpt-4o-mini` plutôt que `gpt-4` pour économiser des ressources

### App qui s'endort
- Les apps gratuites s'endorment après inactivité
- Elles se réveillent automatiquement au prochain accès (peut prendre 10-20 secondes)

## 📊 Limites du plan gratuit

- 1 GB de RAM
- Nombre limité d'apps simultanées
- L'app s'endort après inactivité
- Repository doit être public

Pour lever ces limites, consultez les [plans payants de Streamlit](https://streamlit.io/cloud).

## 🎉 C'est tout !

Votre application est maintenant en ligne et accessible de partout ! 🚀


# 📚 Documentation Technique - Interactive Chart Generator (ICG)

## 📋 Table des matières

1. [Architecture générale](#architecture-générale)
2. [Structure du code](#structure-du-code)
3. [Agents IA et contextes](#agents-ia-et-contextes)
4. [Pipelines de traitement](#pipelines-de-traitement)
5. [Gestion de l'état](#gestion-de-létat)
6. [Système d'historique](#système-dhistorique)
7. [Fonctions principales](#fonctions-principales)
8. [Interface utilisateur](#interface-utilisateur)
9. [Flux de données](#flux-de-données)
10. [Dépendances](#dépendances)

---

## 🏗️ Architecture générale

L'application ICG est une application web Streamlit qui utilise un système multi-agents basé sur LangChain et OpenAI GPT pour générer et modifier des graphiques scientifiques à partir de fichiers de données.

### Composants principaux

```
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT APP (app.py)                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Frontend   │────│  Multi-Agent │────│   Backend    │  │
│  │   (Streamlit)│    │   Pipeline   │    │ (Matplotlib) │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                    │                    │          │
│         │                    │                    │          │
│    ┌────▼────┐         ┌────▼────┐         ┌────▼────┐    │
│    │ Session │         │   LLM   │         │  Files  │    │
│    │  State  │         │ (OpenAI)│         │ (PNG)   │    │
│    └─────────┘         └─────────┘         └─────────┘    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Structure du code

### Fichiers principaux

- **`app.py`** (857 lignes) : Application Streamlit principale
- **`ICG_utils.py`** (85 lignes) : Fonctions utilitaires
- **`requirements.txt`** : Dépendances Python
- **`.streamlit/secrets.toml`** : Configuration des clés API
- **`.streamlit/config.toml`** : Configuration Streamlit

### Organisation de `app.py`

```python
# 1. Imports et configuration (lignes 1-17)
# 2. CSS personnalisé (lignes 20-78)
# 3. Définition du LLM (lignes 80-95)
# 4. Gestion de l'historique (lignes 97-167)
# 5. Contextes des agents (lignes 169-250)
# 6. Fonctions des agents (lignes 252-350)
# 7. Pipelines de traitement (lignes 352-550)
# 8. Interface principale (lignes 552-857)
```

---

## 🤖 Agents IA et contextes

L'application utilise **6 agents IA spécialisés** orchestrés par LangChain :

### 1. **Lecteur** (`lecteur`)
**Rôle** : Analyse le fichier de données

```python
def lecteur(data_file_path):
    """
    Lit et analyse un fichier CSV/XLSX
    Retourne un dictionnaire avec les métadonnées
    """
    data_info = read_data(data_file_path)
    return {
        'shape': data_info['shape'],
        'columns': data_info['columns'],
        'head': data_info['head']
    }
```

**Sortie** : Structure JSON avec les informations du fichier

### 2. **Interpréteur** (`interpreteur`)
**Rôle** : Comprend la demande utilisateur et la structure en JSON

**Contexte** :
```python
INTERPRETER_CONTEXT = """
Tu es un interpréteur scientifique spécialisé en physique.
Ton rôle est d'analyser la demande utilisateur et produire une structure JSON.
"""
```

**Entrée** : 
- Demande utilisateur (texte libre)
- Métadonnées du fichier de données

**Sortie** : JSON structuré décrivant le graphique à créer

**Exemple** :
```json
{
  "type": "line",
  "x_column": "temps",
  "y_columns": ["temperature"],
  "title": "Temperature en fonction du temps",
  "xlabel": "Temps (s)",
  "ylabel": "Temperature (°C)"
}
```

### 3. **Codeur** (`codeur`)
**Rôle** : Génère le code Python à partir du JSON

**Contexte** :
```python
CODEUR_CONTEXT = """
Tu es un générateur de code scientifique Python.
Bibliothèques disponibles : matplotlib, seaborn, pandas, numpy
- Ne génère QUE du code Python
- Utilise plt.savefig('graphique.png')
- N'utilise PAS plt.show()
"""
```

**Entrée** : JSON structuré de l'interpréteur

**Sortie** : Code Python complet et exécutable

**Traitement** :
- Nettoyage des balises markdown (```python...```)
- Extraction du code pur

### 4. **Vérificateur** (`verificateur`)
**Rôle** : Vérifie la syntaxe et la cohérence du code

**Contexte** :
```python
VERIFICATEUR_CONTEXT = """
Tu es un vérificateur de code Python scientifique.
Vérifie : syntaxe, imports, logique, cohérence avec les données.
"""
```

**Entrée** : Code Python généré

**Sortie** : 
- `"OK"` si le code est valide
- Message d'erreur détaillé sinon

### 5. **Debugger** (`debugger`)
**Rôle** : Corrige les erreurs d'exécution

**Contexte** :
```python
DEBUGGER_CONTEXT = """
Tu es un expert en débogage Python.
Analyse l'erreur et propose un code corrigé.
IMPORTANT : Renvoie SEULEMENT le code Python corrigé.
"""
```

**Entrée** :
- Code qui a échoué
- Message d'erreur d'exécution
- Métadonnées des données

**Sortie** : Code Python corrigé

### 6. **Modificateur** (`modificateur`)
**Rôle** : Modifie un code existant selon une nouvelle demande

**Contexte** :
```python
MODIFICATEUR_CONTEXT = """
Tu es un agent spécialisé dans la modification de code Python.
IMPORTANT : Modifie SEULEMENT les parties nécessaires.
Conserve la structure existante et les imports.
"""
```

**Entrée** :
- Code Python existant
- Nouvelle demande utilisateur
- Métadonnées des données

**Sortie** : Code Python modifié

---

## 🔄 Pipelines de traitement

### Pipeline 1 : Génération initiale (première demande)

```
┌────────────┐    ┌──────────────┐    ┌────────┐    ┌──────────────┐
│  Utilisateur│───▶│   Lecteur    │───▶│Interpré│───▶│   Codeur     │
│   Demande  │    │(Lit données) │    │  teur  │    │(Génère code) │
└────────────┘    └──────────────┘    └────────┘    └──────────────┘
                                                             │
                                                             ▼
┌────────────┐    ┌──────────────┐    ┌────────┐    ┌──────────────┐
│  Graphique │◀───│  Exécution   │◀───│Debugger│◀───│ Vérificateur │
│    PNG     │    │   (Python)   │    │(si err)│    │(Valide code) │
└────────────┘    └──────────────┘    └────────┘    └──────────────┘
```

**Étapes détaillées** :

1. **Lecture** (`lecteur`) : Analyse du fichier de données
2. **Interprétation** (`interpreteur`) : Compréhension de la demande
3. **Codage** (`codeur`) : Génération du code Python
4. **Vérification** (`verificateur`) : Validation du code
5. **Exécution** (`run_script`) : Exécution du code
6. **Débogage** (si erreur) (`debugger`) : Correction et réexécution

### Pipeline 2 : Modification (demandes suivantes)

```
┌────────────┐    ┌──────────────┐    ┌──────────────┐
│  Utilisateur│───▶│   Lecteur    │───▶│ Modificateur │
│   Demande  │    │(Lit données) │    │(Modifie code)│
└────────────┘    └──────────────┘    └──────────────┘
                                              │
                                              ▼
┌────────────┐    ┌──────────────┐    ┌──────────────┐
│  Graphique │◀───│  Exécution   │◀───│  Debugger    │
│    PNG     │    │   (Python)   │    │  (si erreur) │
└────────────┘    └──────────────┘    └──────────────┘
```

**Avantages** :
- ⚡ Plus rapide (3 agents au lieu de 6)
- 🎯 Modifications ciblées
- 💰 Moins coûteux en tokens

### Fonction principale : `generate_chart()`

```python
def generate_chart(llm, user_prompt, data_file_path, 
                   is_first_request, previous_code=None):
    """
    Point d'entrée principal pour la génération de graphiques
    
    Args:
        llm: Instance ChatOpenAI
        user_prompt: Demande de l'utilisateur
        data_file_path: Chemin vers le fichier de données
        is_first_request: True si première demande
        previous_code: Code précédent (pour modifications)
    
    Returns:
        (success: bool, chart_path: str, report: dict)
    """
    if is_first_request or previous_code is None:
        return generate_chart_initial(llm, user_prompt, data_file_path)
    else:
        return generate_chart_modification(llm, user_prompt, 
                                           previous_code, data_file_path)
```

---

## 🗃️ Gestion de l'état

### Variables de session (`st.session_state`)

L'application utilise Streamlit session state pour maintenir l'état entre les interactions :

```python
st.session_state = {
    'messages': [],              # Historique de conversation
    'current_chart': None,       # Chemin du graphique actuel
    'data_file': None,           # Chemin du fichier de données
    'llm': ChatOpenAI(...),      # Instance du modèle LLM
    'generated_code': None,      # Code Python généré
    'show_code_editor': False,   # Afficher l'éditeur de code
    'is_first_request': True,    # Première demande ou non
    'history': []                # Historique des états (max 10)
}
```

### Structure d'un message

```python
message = {
    'role': 'user'|'assistant',
    'content': 'texte du message'
}
```

---

## ⏮️ Système d'historique

### Fonctionnement

Le système d'historique permet de revenir en arrière en cas de modification non satisfaisante.

### Fonction : `save_current_state()`

```python
def save_current_state():
    """
    Sauvegarde l'état actuel avant une nouvelle modification
    
    Sauvegarde :
    - Code Python généré
    - Graphique PNG (copie avec nom unique)
    - Historique de conversation
    
    Limite : 10 états maximum (FIFO)
    """
    if st.session_state.current_chart:
        history_chart_path = f"graphique_history_{len(history)}.png"
        shutil.copy(st.session_state.current_chart, history_chart_path)
        
        state = {
            'code': st.session_state.generated_code,
            'chart_path': history_chart_path,
            'messages': st.session_state.messages.copy()
        }
        
        st.session_state.history.append(state)
        
        # Limite à 10 états
        if len(st.session_state.history) > 10:
            old_state = st.session_state.history.pop(0)
            os.remove(old_state['chart_path'])
```

### Fonction : `restore_previous_state()`

```python
def restore_previous_state():
    """
    Restaure l'état précédent depuis l'historique
    
    Restaure :
    - Code Python
    - Graphique PNG
    - Historique de conversation
    
    Returns:
        True si restauration réussie, False sinon
    """
    if st.session_state.history:
        previous_state = st.session_state.history.pop()
        
        st.session_state.generated_code = previous_state['code']
        st.session_state.messages = previous_state['messages']
        
        # Restaurer le graphique
        shutil.copy(previous_state['chart_path'], 'graphique.png')
        st.session_state.current_chart = os.path.join(os.getcwd(), 
                                                       'graphique.png')
        
        os.remove(previous_state['chart_path'])
        return True
    return False
```

### Schéma de fonctionnement

```
État 1          État 2          État 3          État 4
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ Code 1  │───▶│ Code 2  │───▶│ Code 3  │───▶│ Code 4  │
│ Graph 1 │    │ Graph 2 │    │ Graph 3 │    │ Graph 4 │
│ Msgs 1  │    │ Msgs 2  │    │ Msgs 3  │    │ Msgs 4  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
    │              │              │              │
    └──────────────┴──────────────┴──────────────┘
              Bouton "◀️ Retour"
         (restaure n'importe quel état)
```

---

## 🔧 Fonctions principales

### 1. `initialize_llm()`

```python
def initialize_llm() -> ChatOpenAI:
    """
    Initialise le modèle de langage OpenAI
    
    Configuration depuis st.secrets :
    - OPENAI_API_KEY : Clé API OpenAI
    - LLM_MODEL : Modèle à utiliser (gpt-4o-mini par défaut)
    
    Returns:
        Instance ChatOpenAI configurée
    
    Raises:
        st.stop() si clé API manquante
    """
```

### 2. Fonctions des agents

#### `lecteur(data_file_path: str) -> dict`
- Lit le fichier CSV/XLSX
- Retourne métadonnées (shape, columns, head)

#### `interpreteur(llm, interpreteur_input: str) -> str`
- Analyse la demande utilisateur
- Retourne JSON structuré

#### `codeur(llm, codeur_input: str) -> str`
- Génère code Python
- Nettoie les balises markdown

#### `verificateur(llm, verificateur_input: str) -> str`
- Vérifie la validité du code
- Retourne "OK" ou message d'erreur

#### `debugger(llm, debugger_input: str) -> str`
- Corrige les erreurs
- Retourne code corrigé

#### `modificateur(llm, modificateur_input: str) -> str`
- Modifie code existant
- Retourne code modifié

### 3. Pipelines

#### `generate_chart_initial(llm, user_prompt, data_file_path)`
Pipeline complet pour la première demande :
1. Lecteur → 2. Interpréteur → 3. Codeur → 4. Vérificateur → 5. Exécution → 6. Debugger (si erreur)

**Returns** : `(success: bool, chart_path: str, report: dict)`

#### `generate_chart_modification(llm, user_prompt, previous_code, data_file_path)`
Pipeline simplifié pour les modifications :
1. Lecteur → 2. Modificateur → 3. Exécution → 4. Debugger (si erreur)

**Returns** : `(success: bool, chart_path: str, report: dict)`

### 4. Fonctions utilitaires (ICG_utils.py)

#### `read_data(file_path: str) -> dict`
```python
def read_data(file_path):
    """
    Lit un fichier CSV ou XLSX
    
    Returns:
        {
            'shape': (lignes, colonnes),
            'columns': ['col1', 'col2', ...],
            'head': DataFrame.head(5)
        }
    """
```

#### `run_script(script_path: str) -> str`
```python
def run_script(script_path):
    """
    Exécute un script Python
    
    Returns:
        Message d'erreur si échec, '' si succès
    """
```

#### Fonctions de contexte
- `interpreteur_context()`
- `codeur_context()`
- `verificateur_context()`
- `debugger_context()`

---

## 🎨 Interface utilisateur

### Structure de la page

```
┌─────────────────────────────────────────────────────────┐
│                     HEADER (Titre)                      │
├────────────────┬────────────────────────────────────────┤
│                │                                         │
│   SIDEBAR      │         MAIN AREA                      │
│                │                                         │
│ ┌────────────┐ │ ┌──────────────┬──────────────────┐   │
│ │  Upload    │ │ │              │                  │   │
│ │  Fichier   │ │ │  Chat        │   Graphique      │   │
│ └────────────┘ │ │  Zone        │   + Boutons      │   │
│                │ │              │                  │   │
│ ┌────────────┐ │ └──────────────┴──────────────────┘   │
│ │  Actions   │ │                                         │
│ │ - Nouvelle │ │ ┌────────────────────────────────┐    │
│ │ - Guide    │ │ │   Éditeur de Code (optionnel)  │    │
│ └────────────┘ │ └────────────────────────────────┘    │
│                │                                         │
└────────────────┴─────────────────────────────────────────┘
```

### Composants principaux

#### 1. Sidebar
```python
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Upload de fichier
    uploaded_file = st.file_uploader(...)
    
    # Bouton nouvelle conversation
    if st.button("🔄 Nouvelle conversation"):
        # Réinitialisation complète
    
    # Guide d'utilisation
    st.markdown("### 📖 Guide d'utilisation")
    
    # Indicateurs
    if st.session_state.generated_code:
        st.info("🔧 Mode modification")
    if len(st.session_state.history) > 0:
        st.success(f"📚 {len(history)} version(s)")
```

#### 2. Zone de chat
```python
with col1:
    st.subheader("💬 Conversation")
    
    # Affichage des messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            # Style bleu
        else:
            # Style gris
    
    # Input utilisateur
    user_input = st.chat_input("Décrivez le graphique...")
```

#### 3. Zone graphique
```python
with col2:
    st.subheader("📊 Graphique")
    
    if st.session_state.current_chart:
        # Affichage du graphique
        st.image(st.session_state.current_chart)
        
        # Boutons d'action
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button("📥 Télécharger")
        
        with col2:
            st.button("🔧 Voir code")
        
        with col3:
            if len(st.session_state.history) > 0:
                st.button("◀️ Retour")
```

#### 4. Éditeur de code
```python
if st.session_state.show_code_editor:
    st.divider()
    st.subheader("💻 Code Python généré")
    
    # Zone de texte éditable avec clé dynamique
    code_hash = hash(st.session_state.generated_code)
    edited_code = st.text_area(
        "Code Python (éditable)",
        value=st.session_state.generated_code,
        key=f"code_editor_{code_hash}"
    )
    
    # Détection de modification
    if edited_code != st.session_state.generated_code:
        st.button("💾 Sauvegarder les modifications")
    
    # Bouton d'exécution
    st.button("▶️ Exécuter le code")
```

### CSS personnalisé

```css
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
}

.chat-container {
    height: 500px;
    overflow-y: auto;
    background-color: #fafafa;
}

.user-message {
    background-color: #e3f2fd;
    border-left-color: #1976d2;
}

.assistant-message {
    background-color: #f5f5f5;
    border-left-color: #757575;
}
```

---

## 📊 Flux de données

### Flux complet d'une demande

```
1. UPLOAD
   ┌─────────────┐
   │ Utilisateur │
   │ upload CSV  │
   └──────┬──────┘
          ▼
   ┌─────────────┐
   │ Streamlit   │
   │ save temp   │
   └──────┬──────┘
          ▼
   session_state.data_file = "/tmp/data.csv"

2. DEMANDE
   ┌─────────────┐
   │ Utilisateur │
   │ "Trace..."  │
   └──────┬──────┘
          ▼
   ┌─────────────┐
   │save_current │  ← Sauvegarde état actuel
   │   _state()  │
   └──────┬──────┘
          ▼
   ┌─────────────┐
   │ generate_   │  ← Pipeline IA
   │   chart()   │
   └──────┬──────┘
          ▼
   ┌─────────────┐
   │ run_script  │  ← Exécution Python
   │     ()      │
   └──────┬──────┘
          ▼
   graphique.png créé

3. AFFICHAGE
   ┌─────────────┐
   │  Streamlit  │
   │st.image(...) │
   └─────────────┘
```

### Flux du système d'historique

```
AVANT modification :
┌─────────────────┐
│ État actuel     │
│ - Code          │
│ - Graphique     │
│ - Messages      │
└────────┬────────┘
         │
         ▼ save_current_state()
┌─────────────────┐
│ history.append()│
│ - Copie PNG     │
│ - Clone état    │
└─────────────────┘

APRÈS retour :
┌─────────────────┐
│ history.pop()   │
└────────┬────────┘
         │
         ▼ restore_previous_state()
┌─────────────────┐
│ Restauration    │
│ - Copie PNG     │
│ - Restaure état │
└─────────────────┘
```

---

## 📦 Dépendances

### requirements.txt

```txt
streamlit>=1.28.0       # Framework web
pandas>=2.0.0           # Manipulation de données
numpy>=1.24.0           # Calculs numériques
matplotlib>=3.7.0       # Génération de graphiques
seaborn>=0.12.0         # Graphiques statistiques
langchain>=0.1.0        # Orchestration LLM
langchain-openai>=0.0.5 # Intégration OpenAI
openai>=1.0.0           # API OpenAI
openpyxl>=3.1.0         # Lecture Excel
```

### Versions Python

- **Minimum** : Python 3.8
- **Recommandé** : Python 3.10+
- **Testé** : Python 3.14

---

## 🔐 Configuration

### secrets.toml

```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "sk-..."
LLM_MODEL = "gpt-4o-mini"
```

### config.toml

```toml
# .streamlit/config.toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"

[server]
headless = true
port = 8501
```

---

## 🐛 Gestion des erreurs

### Niveaux d'erreur

1. **Erreur de syntaxe** : Détectée par le vérificateur
2. **Erreur d'exécution** : Capturée par `run_script()`
3. **Erreur après débogage** : Affichée à l'utilisateur

### Exemple de gestion

```python
try:
    # Exécution du code
    log = run_script(temp_code_file)
    
    if log:
        # Tentative de débogage
        fixed_code = debugger(llm, debug_input)
        log_debug = run_script(fixed_code_file)
        
        if log_debug:
            # Échec après débogage
            return (False, None, {'log_debug': log_debug})
        else:
            # Succès après débogage
            return (True, 'graphique.png', {...})
    else:
        # Succès direct
        return (True, 'graphique.png', {...})
        
except Exception as e:
    return (False, None, {'error': str(e)})
```

---

## 🚀 Performance

### Optimisations

1. **Pipeline allégée** : Modification vs génération initiale
   - Initial : 6 agents (~2-3s, ~2000 tokens)
   - Modification : 3 agents (~1-2s, ~1000 tokens)

2. **Cache de session** : 
   - LLM initialisé une seule fois
   - Données chargées une seule fois

3. **Historique limité** :
   - Maximum 10 versions
   - Suppression automatique des anciennes

### Temps de réponse typiques

- **Première demande** : 3-5 secondes
- **Modification** : 1-2 secondes
- **Retour arrière** : < 1 seconde (instantané)

---

## 📝 Bonnes pratiques

### Pour les développeurs

1. **Toujours tester** avec des données réelles
2. **Nettoyer** les fichiers temporaires
3. **Limiter** la taille de l'historique
4. **Valider** les entrées utilisateur
5. **Gérer** toutes les exceptions

### Pour les utilisateurs

1. **Commencer simple** : Une demande claire
2. **Itérer** : Affiner progressivement
3. **Utiliser le retour** : Annuler si besoin
4. **Éditer le code** : Modifications manuelles possibles
5. **Tester** : Vérifier le résultat avant export

---

## 🔄 Cycle de vie d'une session

```
1. INITIALISATION
   ├─ Chargement Streamlit
   ├─ Initialisation LLM
   └─ Création session_state

2. UPLOAD FICHIER
   ├─ Sélection fichier
   ├─ Sauvegarde temporaire
   └─ Lecture métadonnées

3. PREMIÈRE DEMANDE
   ├─ Pipeline complète (6 agents)
   ├─ Génération graphique
   └─ Affichage résultat

4. MODIFICATIONS (boucle)
   ├─ Sauvegarde état actuel
   ├─ Pipeline modification (3 agents)
   ├─ Mise à jour graphique
   └─ Option retour arrière

5. EXPORT
   ├─ Téléchargement PNG
   ├─ Copie code (optionnel)
   └─ Fin session

6. NETTOYAGE
   ├─ Suppression fichiers temp
   ├─ Réinitialisation état
   └─ Nouvelle conversation
```

---

## 📖 Exemples d'utilisation

### Exemple 1 : Graphique simple

**Demande** : "Trace la température en fonction du temps"

**Traitement** :
1. Lecteur : Identifie colonnes `temps` et `temperature`
2. Interpréteur : JSON → `{"type": "line", "x": "temps", "y": ["temperature"]}`
3. Codeur : Génère code matplotlib
4. Exécution : Création `graphique.png`

### Exemple 2 : Modification

**Demande** : "Ajoute la pression sur le même graphique"

**Traitement** :
1. Modificateur : Ajoute `plt.plot(df['pression'])` au code existant
2. Exécution : Mise à jour `graphique.png`

### Exemple 3 : Retour arrière

**Action** : Clic sur "◀️ Retour"

**Traitement** :
1. `restore_previous_state()` : Pop historique
2. Copie PNG précédent
3. Restaure code et messages
4. Rerun Streamlit

---

## 🎓 Conclusion

Cette documentation couvre l'intégralité de l'architecture et du fonctionnement de l'application ICG. Pour toute question ou amélioration, consultez le code source ou ouvrez une issue sur GitHub.

**Repository** : https://github.com/Mirouxe/GAG

**Version** : 1.0.0 (avec système d'historique)

**Dernière mise à jour** : Novembre 2025

---

*Développé avec ❤️ et 🤖*


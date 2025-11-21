import streamlit as st
import os
import tempfile
from langchain_openai import ChatOpenAI
from ICG_utils import read_data, run_script, verificateur_context, interpreteur_context, codeur_context, debugger_context

# Configuration de matplotlib pour éviter les problèmes d'affichage
import matplotlib
matplotlib.use('Agg')

# Configuration de la page
st.set_page_config(
    page_title="ICG - Interactive Chart Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour améliorer l'UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .chat-container {
        height: 500px;
        overflow-y: auto;
        padding: 1rem;
        background-color: #fafafa;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid;
        color: #000000;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #1976d2;
        color: #000000;
    }
    .user-message strong {
        color: #1976d2;
        font-weight: 600;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left-color: #757575;
        color: #000000;
    }
    .assistant-message strong {
        color: #757575;
        font-weight: 600;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

#################################### Définition du LLM ####################################
def initialize_llm():
    """Initialise le modèle LLM"""
    API_KEY = st.secrets.get("OPENAI_API_KEY", "")
    LLM_MODEL = st.secrets.get("LLM_MODEL", "gpt-4o-mini")
    
    if not API_KEY:
        st.error("⚠️ Veuillez configurer OPENAI_API_KEY dans .streamlit/secrets.toml")
        st.stop()
    
    llm = ChatOpenAI(
        api_key=API_KEY,
        model=LLM_MODEL,
        temperature=0.7
    )
    return llm

#################################### Gestion de l'historique ####################################
def save_current_state():
    """Sauvegarde l'état actuel dans l'historique avant une modification"""
    import shutil
    
    # Ne sauvegarder que si on a au moins un graphique
    if st.session_state.current_chart and os.path.exists(st.session_state.current_chart):
        # Créer une copie du graphique avec un nom unique
        history_chart_path = f"graphique_history_{len(st.session_state.history)}.png"
        try:
            shutil.copy(st.session_state.current_chart, history_chart_path)
            
            # Sauvegarder l'état complet
            state = {
                "code": st.session_state.generated_code,
                "chart_path": history_chart_path,
                "messages": st.session_state.messages.copy(),
            }
            
            st.session_state.history.append(state)
            
            # Limiter l'historique à 10 états pour éviter de consommer trop de mémoire
            if len(st.session_state.history) > 10:
                # Supprimer le plus ancien état et son fichier
                old_state = st.session_state.history.pop(0)
                if os.path.exists(old_state["chart_path"]):
                    try:
                        os.remove(old_state["chart_path"])
                    except:
                        pass
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'historique: {e}")

def restore_previous_state():
    """Restaure l'état précédent depuis l'historique"""
    if st.session_state.history:
        # Récupérer le dernier état
        previous_state = st.session_state.history.pop()
        
        # Restaurer l'état
        st.session_state.generated_code = previous_state["code"]
        st.session_state.messages = previous_state["messages"]
        
        # Copier le graphique de l'historique vers le graphique actuel
        if os.path.exists(previous_state["chart_path"]):
            import shutil
            shutil.copy(previous_state["chart_path"], "graphique.png")
            st.session_state.current_chart = os.path.join(os.getcwd(), "graphique.png")
            
            # Supprimer le fichier de l'historique
            try:
                os.remove(previous_state["chart_path"])
            except:
                pass
        
        return True
    return False

#################################### Contextes des agents ####################################
INTERPRETER_CONTEXT = """
Tu es un interpréteur scientifique spécialisé en physique.

Ton rôle est d'analyser la demande utilisateur concernant l'affichage
de graphique et de produire une structure JSON.

Ne génère pas de code, ne fais aucune explication textuelle, écris seulement le JSON.
"""

CODEUR_CONTEXT = """
Tu es un générateur de code scientifique Python.

À partir d'une description structurée en JSON, tu dois produire
un code clair, commenté et autonome utilisant numpy, matplotlib et seaborn.
Le code doit produire un graphique physique cohérent.
Attention à bien afficher toutes les grandeurs demandées et les légendes.

Bibliothèques disponibles :
- matplotlib.pyplot (plt) : pour les graphiques standards
- seaborn (sns) : pour les graphiques statistiques élégants (distribution, heatmap, pairplot, etc.)
- pandas (pd) : pour la manipulation des données
- numpy (np) : pour les calculs numériques

Ne fais aucune explication textuelle : écris seulement le code Python.
Ta réponse doit pouvoir être directement exécutée donc ne renvoie que
du code python pur !

Pour charger les données, utilise pandas.

Tu peux utiliser seaborn pour créer des graphiques plus esthétiques quand c'est approprié.
N'oublie pas d'importer seaborn si tu l'utilises : import seaborn as sns

Sauvegarde le graphique dans le dossier de travail sous le nom graphique.png

IMPORTANT : N'utilise PAS plt.show() car le code s'exécute en mode non-interactif.
Utilise seulement plt.savefig('graphique.png') puis plt.close()
"""

VERIFICATEUR_CONTEXT = """
Tu es un vérificateur de code python.

Tu compares la demande initiale, la structure JSON et le code généré.

Tu évalues la cohérence physique, conceptuelle et graphique.

Tu vérifies que le code affiche toutes les grandeurs demandées.

Tu fais attention à ce que le code ne contienne pas de texte qui n'est pas du code.

Tu rends un rapport JSON ayant la même structure que celui ci-dessous mais avec tes corrections

Ne réécris pas le code, ne fais aucune explication textuelle,

rend uniquement un JSON si le code n'est pas conforme sinon ne renvoie qu'un message disant 'CODE CONFORME'
"""

DEBUGGER_CONTEXT = """
Tu es un agent spécialisé dans le débogage de code Python scientifique.

Ton rôle intervient après l'exécution du code :
- Si le code a échoué à l'exécution, tu reçois le code source et le message d'erreur.
- Tu dois identifier précisément la cause de l'erreur et corriger le code en conséquence.

Règles impératives :
1. Ta sortie doit contenir uniquement le code Python corrigé (aucun texte explicatif).
2. Ne modifie pas le contenu au-delà de ce qui est nécessaire pour corriger l'erreur.
3. Si plusieurs corrections sont possibles, choisis la plus simple et robuste.
4. Si une information est manquante pour corriger l'erreur, laisse "???" et ajoute un commentaire dans le code à cet endroit.
5. Ne reformate pas entièrement le fichier : conserve le style existant.
6. N'ajoute ni préambule, ni conclusion, ni phrase du type "Voici le code corrigé".

Tu renvoies uniquement le code corrigé, sans aucun texte autour.
"""

MODIFICATEUR_CONTEXT = """
Tu es un agent spécialisé dans la modification de code Python scientifique pour matplotlib et seaborn.

Ton rôle est de MODIFIER le code existant selon la nouvelle demande de l'utilisateur.

IMPORTANT : Tu travailles sur un code DÉJÀ FONCTIONNEL. Tu dois :
1. Conserver toute la structure existante du code (imports, chargement des données, etc.)
2. MODIFIER uniquement les parties nécessaires pour répondre à la nouvelle demande
3. AJOUTER les éléments demandés sans supprimer ce qui fonctionne déjà
4. Maintenir la cohérence du style de code
5. Tu peux utiliser seaborn (sns) si cela améliore le graphique

Exemples de modifications possibles avec matplotlib :
- Changer les couleurs : modifier les paramètres color= dans plt.plot()
- Ajouter des lignes : ajouter plt.axvline() ou plt.axhline()
- Modifier les titres/labels : changer plt.title(), plt.xlabel(), plt.ylabel()
- Ajouter des courbes : ajouter de nouveaux plt.plot()
- Changer le style : modifier linestyle=, marker=, linewidth=
- Modifier les échelles : ajouter plt.xlim(), plt.ylim()
- Ajouter des annotations : ajouter plt.text(), plt.annotate()

Exemples de modifications possibles avec seaborn :
- Passer de matplotlib à seaborn : remplacer plt.plot() par sns.lineplot()
- Ajouter un style seaborn : sns.set_style(), sns.set_palette()
- Créer des graphiques statistiques : sns.boxplot(), sns.violinplot(), sns.heatmap()
- Améliorer l'esthétique : utiliser seaborn pour des graphiques plus élégants

Règles impératives :
1. Ta sortie doit contenir UNIQUEMENT le code Python complet modifié
2. NE génère AUCUN texte explicatif, AUCUN commentaire sur les modifications
3. Le code doit être directement exécutable
4. CONSERVE plt.savefig('graphique.png') et plt.close() à la fin
5. N'utilise PAS plt.show()
6. Si tu ajoutes seaborn, n'oublie pas d'ajouter l'import : import seaborn as sns
7. Si la demande n'est pas claire, fais une modification raisonnable

Tu renvoies UNIQUEMENT le code Python modifié complet, sans aucun texte autour.
"""

#################################### Fonctions des agents ####################################
def interpreteur(llm, interpreteur_input):
    response = llm.invoke(input=interpreteur_input)
    return response.content

def codeur(llm, codeur_input):
    response = llm.invoke(input=codeur_input)
    code = response.content
    
    # Nettoyer le code des balises markdown
    if "```python" in code:
        # Extraire le code entre ```python et ```
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        # Extraire le code entre ``` et ```
        code = code.split("```")[1].split("```")[0].strip()
    
    return code

def verificateur(llm, verificateur_input):
    response = llm.invoke(input=verificateur_input)
    return response.content

def debugger(llm, debugger_input):
    response = llm.invoke(input=debugger_input)
    code = response.content
    
    # Nettoyer le code des balises markdown
    if "```python" in code:
        # Extraire le code entre ```python et ```
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        # Extraire le code entre ``` et ```
        code = code.split("```")[1].split("```")[0].strip()
    
    return code

def modificateur(llm, modificateur_input):
    """Agent qui modifie le code existant selon une nouvelle demande"""
    response = llm.invoke(input=modificateur_input)
    code = response.content
    
    # Nettoyer le code des balises markdown
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()
    
    return code

#################################### Pipeline de génération ####################################
def generate_chart_initial(llm, user_prompt, data_file_path):
    """
    Pipeline COMPLÈTE pour la première génération de graphique
    
    Returns:
        tuple: (success: bool, chart_path: str, report: dict)
    """
    report = {"pipeline": "initial"}
    
    try:
        # Lecture du fichier de données
        with st.spinner("📖 Lecture du fichier de données..."):
            lecteur_output = read_data(data_file_path)
            report["lecteur_output"] = lecteur_output
        
        # Interprétation
        with st.spinner("🧠 Interprétation de votre demande..."):
            interpreteur_input = interpreteur_context(INTERPRETER_CONTEXT, user_prompt, lecteur_output)
            interpreteur_output = interpreteur(llm, interpreteur_input)
            report["interpreteur_output"] = interpreteur_output
        
        # Codage
        with st.spinner("💻 Génération du code Python..."):
            codeur_input = codeur_context(CODEUR_CONTEXT, interpreteur_output, lecteur_output)
            codeur_output = codeur(llm, codeur_input)
            report["codeur_output"] = codeur_output
            report["clean_code"] = codeur_output  # Code nettoyé sans les balises markdown
        
        # Vérification
        with st.spinner("✅ Vérification du code..."):
            verificateur_input = verificateur_context(VERIFICATEUR_CONTEXT, user_prompt, interpreteur_output, codeur_output)
            verificateur_output = verificateur(llm, verificateur_input)
            report["verificateur_output"] = verificateur_output
        
        # Exécution du code
        with st.spinner("🚀 Exécution du code et génération du graphique..."):
            # Créer un fichier temporaire pour le code
            # Ajouter la configuration matplotlib au début du code
            code_with_matplotlib = """import matplotlib
matplotlib.use('Agg')
""" + codeur_output
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, dir=os.getcwd()) as f:
                f.write(code_with_matplotlib)
                code_file = f.name
            
            log = run_script(code_file)
            report["log"] = log
            
            # Si erreur, lancer le debugger
            if log:
                with st.spinner("🔧 Débogage en cours..."):
                    debugger_input = debugger_context(DEBUGGER_CONTEXT, codeur_output, log)
                    debugger_output = debugger(llm, debugger_input)
                    report["debugger_output"] = debugger_output
                    
                    # Réexécuter le code débogué
                    # Ajouter la configuration matplotlib au début du code
                    debug_code_with_matplotlib = """import matplotlib
matplotlib.use('Agg')
""" + debugger_output
                    
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, dir=os.getcwd()) as f:
                        f.write(debug_code_with_matplotlib)
                        debug_code_file = f.name
                    
                    log_debug = run_script(debug_code_file)
                    report["log_debug"] = log_debug
                    
                    # Nettoyer les fichiers temporaires
                    try:
                        os.remove(debug_code_file)
                    except:
                        pass
                    
                    if log_debug:
                        # Nettoyer le fichier de code
                        try:
                            os.remove(code_file)
                        except:
                            pass
                        return False, None, report
            
            # Nettoyer le fichier de code
            try:
                os.remove(code_file)
            except:
                pass
            
            # Vérifier si le graphique a été créé
            chart_path = os.path.join(os.getcwd(), "graphique.png")
            if os.path.exists(chart_path):
                return True, chart_path, report
            else:
                return False, None, report
                
    except Exception as e:
        report["error"] = str(e)
        return False, None, report

def generate_chart_modification(llm, user_prompt, previous_code, data_file_path):
    """
    Pipeline SIMPLIFIÉE pour la modification d'un graphique existant
    
    Args:
        llm: Le modèle de langage
        user_prompt: La nouvelle demande de l'utilisateur
        previous_code: Le code précédemment généré
        data_file_path: Le chemin vers le fichier de données
    
    Returns:
        tuple: (success: bool, chart_path: str, report: dict)
    """
    report = {"pipeline": "modification"}
    
    try:
        # Lecture du fichier de données (pour avoir les métadonnées)
        lecteur_output = read_data(data_file_path)
        report["lecteur_output"] = lecteur_output
        
        # Construction du contexte pour le modificateur
        with st.spinner("✏️ Modification du code existant..."):
            modificateur_input = f"""{MODIFICATEUR_CONTEXT}

Voici le CODE ACTUEL qui fonctionne :
```python
{previous_code}
```

Voici les MÉTADONNÉES du fichier de données :
{lecteur_output}

Voici la NOUVELLE DEMANDE de l'utilisateur :
{user_prompt}

Ta tâche : Modifie le code ci-dessus pour intégrer cette nouvelle demande.
Renvoie le code Python complet modifié, sans aucun texte explicatif.
"""
            
            modificateur_output = modificateur(llm, modificateur_input)
            report["modificateur_output"] = modificateur_output
            report["clean_code"] = modificateur_output
        
        # Exécution du code modifié
        with st.spinner("🚀 Exécution du code modifié..."):
            # Ajouter la configuration matplotlib
            code_with_matplotlib = """import matplotlib
matplotlib.use('Agg')
""" + modificateur_output
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, dir=os.getcwd()) as f:
                f.write(code_with_matplotlib)
                code_file = f.name
            
            log = run_script(code_file)
            report["log"] = log
            
            # Si erreur, lancer le debugger
            if log:
                with st.spinner("🔧 Débogage en cours..."):
                    debugger_input = debugger_context(DEBUGGER_CONTEXT, modificateur_output, log)
                    debugger_output = debugger(llm, debugger_input)
                    report["debugger_output"] = debugger_output
                    
                    # Réexécuter le code débogué
                    debug_code_with_matplotlib = """import matplotlib
matplotlib.use('Agg')
""" + debugger_output
                    
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, dir=os.getcwd()) as f:
                        f.write(debug_code_with_matplotlib)
                        debug_code_file = f.name
                    
                    log_debug = run_script(debug_code_file)
                    report["log_debug"] = log_debug
                    
                    # Nettoyer les fichiers temporaires
                    try:
                        os.remove(debug_code_file)
                    except:
                        pass
                    
                    if log_debug:
                        # Nettoyer le fichier de code
                        try:
                            os.remove(code_file)
                        except:
                            pass
                        return False, None, report
                    
                    # Si le debugger a réussi, utiliser son code
                    report["clean_code"] = debugger_output
            
            # Nettoyer le fichier de code
            try:
                os.remove(code_file)
            except:
                pass
            
            # Vérifier si le graphique a été créé
            chart_path = os.path.join(os.getcwd(), "graphique.png")
            if os.path.exists(chart_path):
                return True, chart_path, report
            else:
                return False, None, report
                
    except Exception as e:
        report["error"] = str(e)
        return False, None, report

def generate_chart(llm, user_prompt, data_file_path, is_first_request, previous_code=None):
    """
    Point d'entrée principal pour la génération de graphiques
    
    Args:
        llm: Le modèle de langage
        user_prompt: La demande de l'utilisateur
        data_file_path: Le chemin vers le fichier de données
        is_first_request: True si c'est la première demande, False sinon
        previous_code: Le code précédemment généré (None si première demande)
    
    Returns:
        tuple: (success: bool, chart_path: str, report: dict)
    """
    if is_first_request or previous_code is None:
        # Pipeline complète pour la première demande
        return generate_chart_initial(llm, user_prompt, data_file_path)
    else:
        # Pipeline de modification pour les demandes suivantes
        return generate_chart_modification(llm, user_prompt, previous_code, data_file_path)

#################################### Interface Streamlit ####################################
def main():
    # En-tête
    st.markdown('<h1 class="main-header">📊 Interactive Chart Generator</h1>', unsafe_allow_html=True)
    st.markdown("### Générez et modifiez des graphiques scientifiques en temps réel par dialogue")
    
    # Initialisation de la session
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_chart" not in st.session_state:
        st.session_state.current_chart = None
    if "data_file" not in st.session_state:
        st.session_state.data_file = None
    if "llm" not in st.session_state:
        st.session_state.llm = initialize_llm()
    if "generated_code" not in st.session_state:
        st.session_state.generated_code = None
    if "show_code_editor" not in st.session_state:
        st.session_state.show_code_editor = False
    if "is_first_request" not in st.session_state:
        st.session_state.is_first_request = True
    if "history" not in st.session_state:
        st.session_state.history = []  # Historique des états (code, graphique, messages)
    
    # Sidebar pour l'upload et la configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Upload de fichier
        uploaded_file = st.file_uploader(
            "📁 Choisissez un fichier de données",
            type=['csv', 'xlsx'],
            help="Téléchargez un fichier CSV ou Excel contenant vos données"
        )
        
        if uploaded_file is not None:
            # Sauvegarder temporairement le fichier
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            st.session_state.data_file = temp_path
            
            # Afficher les informations du fichier
            st.success(f"✅ Fichier chargé : {uploaded_file.name}")
            
            # Afficher un aperçu des données
            with st.expander("👁️ Aperçu des données"):
                data_info = read_data(temp_path)
                st.write(f"**Dimensions:** {data_info['shape'][0]} lignes × {data_info['shape'][1]} colonnes")
                st.write(f"**Colonnes:** {', '.join(data_info['columns'])}")
        
        st.divider()
        
        # Bouton pour réinitialiser la conversation
        if st.button("🔄 Nouvelle conversation"):
            st.session_state.messages = []
            st.session_state.current_chart = None
            st.session_state.generated_code = None
            st.session_state.is_first_request = True
            st.session_state.show_code_editor = False
            
            # Nettoyer l'historique et supprimer les fichiers
            for state in st.session_state.history:
                if "chart_path" in state and os.path.exists(state["chart_path"]):
                    try:
                        os.remove(state["chart_path"])
                    except:
                        pass
            st.session_state.history = []
            
            # Supprimer le graphique actuel
            if os.path.exists("graphique.png"):
                try:
                    os.remove("graphique.png")
                except:
                    pass
            st.rerun()
        
        st.divider()
        st.markdown("### 📖 Guide d'utilisation")
        st.markdown("""
        1. **Uploadez** votre fichier de données (CSV/XLSX)
        2. **Décrivez** le graphique que vous voulez créer
        3. **Dialoguez** pour affiner et modifier le graphique
        4. **Téléchargez** le résultat final
        """)
        
        # Indicateur de mode
        if st.session_state.generated_code is not None:
            st.info("🔧 **Mode modification** : Les prochaines demandes modifieront le graphique actuel de manière incrémentale.")
        
        # Indicateur d'historique
        if len(st.session_state.history) > 0:
            st.success(f"📚 **Historique** : {len(st.session_state.history)} version(s) sauvegardée(s)")
            st.caption("Utilisez le bouton '◀️ Retour' pour revenir en arrière")
    
    # Zone principale - Chat et graphique
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("💬 Conversation")
        
        # Conteneur scrollable pour l'historique des messages
        chat_html = '<div class="chat-container">'
        
        if len(st.session_state.messages) == 0:
            chat_html += '<div style="text-align: center; padding: 2rem; color: #666;">Aucun message pour le moment. Commencez par uploader un fichier et décrire votre graphique !</div>'
        else:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    chat_html += f'<div class="chat-message user-message"><strong>👤 Vous:</strong><br>{message["content"]}</div>'
                else:
                    chat_html += f'<div class="chat-message assistant-message"><strong>🤖 Assistant:</strong><br>{message["content"]}</div>'
        
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)
        
        # Zone de saisie
        user_input = st.chat_input("Décrivez le graphique que vous souhaitez créer ou les modifications à apporter...")
        
        if user_input:
            if st.session_state.data_file is None:
                st.error("❌ Veuillez d'abord télécharger un fichier de données dans la sidebar.")
            else:
                # Sauvegarder l'état actuel avant de générer un nouveau graphique
                save_current_state()
                
                # Ajouter le message utilisateur
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Générer le graphique (pipeline différente selon si c'est la première demande)
                success, chart_path, report = generate_chart(
                    st.session_state.llm,
                    user_input,
                    st.session_state.data_file,
                    st.session_state.is_first_request,
                    st.session_state.generated_code
                )
                
                if success:
                    st.session_state.current_chart = chart_path
                    # Sauvegarder le code généré
                    if "clean_code" in report:
                        st.session_state.generated_code = report["clean_code"]
                        # Afficher automatiquement l'éditeur de code après une génération réussie
                        st.session_state.show_code_editor = True
                    
                    # Marquer qu'on a fait au moins une requête
                    if st.session_state.is_first_request:
                        st.session_state.is_first_request = False
                    
                    # Message différent selon le type de pipeline
                    pipeline_type = report.get("pipeline", "initial")
                    if pipeline_type == "initial":
                        message = "✅ Graphique généré avec succès ! Vous pouvez le voir dans la zone de droite."
                    else:
                        message = "✅ Graphique modifié avec succès ! Les changements ont été appliqués."
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": message
                    })
                else:
                    error_msg = "❌ Une erreur s'est produite lors de la génération du graphique."
                    if "error" in report:
                        error_msg += f"\n\nDétails: {report['error']}"
                    elif "log_debug" in report:
                        error_msg += f"\n\nErreur après débogage: {report['log_debug']}"
                    elif "log" in report:
                        error_msg += f"\n\nErreur: {report['log']}"
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
                
                st.rerun()
    
    with col2:
        st.subheader("📊 Graphique")
        
        if st.session_state.current_chart and os.path.exists(st.session_state.current_chart):
            # Afficher le graphique
            st.image(st.session_state.current_chart, width="stretch")
            
            # Boutons d'actions
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                # Bouton de téléchargement
                with open(st.session_state.current_chart, "rb") as file:
                    st.download_button(
                        label="📥 Télécharger",
                        data=file,
                        file_name="graphique.png",
                        mime="image/png"
                    )
            
            with col_btn2:
                # Bouton pour masquer/afficher le code
                if st.session_state.generated_code:
                    button_label = "👁️ Masquer" if st.session_state.show_code_editor else "🔧 Voir code"
                    if st.button(button_label):
                        st.session_state.show_code_editor = not st.session_state.show_code_editor
                        st.rerun()
            
            with col_btn3:
                # Bouton retour (actif seulement s'il y a un historique)
                if len(st.session_state.history) > 0:
                    if st.button("◀️ Retour", help=f"Revenir à l'état précédent ({len(st.session_state.history)} version(s))"):
                        if restore_previous_state():
                            st.success("✅ État précédent restauré !")
                            st.rerun()
                else:
                    st.button("◀️ Retour", disabled=True, help="Pas d'historique disponible")
            
            # Éditeur de code (mis à jour automatiquement)
            if st.session_state.show_code_editor and st.session_state.generated_code:
                st.divider()
                st.subheader("💻 Code Python généré")
                st.caption("✨ Le code se met à jour automatiquement à chaque génération. Vous pouvez le modifier et l'exécuter manuellement.")
                
                # Zone de texte éditable avec le code (clé dynamique pour forcer la mise à jour)
                code_hash = hash(st.session_state.generated_code)
                edited_code = st.text_area(
                    "Code Python (éditable)",
                    value=st.session_state.generated_code,
                    height=400,
                    key=f"code_editor_{code_hash}"
                )
                
                # Détecter si l'utilisateur a modifié le code
                if edited_code != st.session_state.generated_code:
                    st.info("✏️ **Code modifié** : Les prochaines modifications seront basées sur votre code personnalisé.")
                    # Mettre à jour le code généré avec la version éditée
                    # Cela sera utilisé comme base pour les modifications suivantes
                    if st.button("💾 Sauvegarder les modifications", type="secondary", key="save_code"):
                        st.session_state.generated_code = edited_code
                        st.success("✅ Code sauvegardé ! Les prochaines demandes modifieront ce code.")
                        st.rerun()
                
                # Boutons pour exécuter ou réinitialiser
                col_exec1, col_exec2 = st.columns(2)
                
                with col_exec1:
                    if st.button("▶️ Exécuter le code", type="primary"):
                        if edited_code.strip():
                            with st.spinner("🚀 Exécution du code..."):
                                # Ajouter la configuration matplotlib
                                code_to_run = """import matplotlib
matplotlib.use('Agg')
""" + edited_code
                                
                                # Créer un fichier temporaire
                                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, dir=os.getcwd()) as f:
                                    f.write(code_to_run)
                                    temp_code_file = f.name
                                
                                # Exécuter
                                log = run_script(temp_code_file)
                                
                                # Nettoyer
                                try:
                                    os.remove(temp_code_file)
                                except:
                                    pass
                                
                                # Vérifier le résultat
                                if log:
                                    st.error(f"❌ Erreur lors de l'exécution:\n```\n{log}\n```")
                                else:
                                    # Vérifier si le graphique a été généré
                                    if os.path.exists("graphique.png"):
                                        st.session_state.current_chart = os.path.join(os.getcwd(), "graphique.png")
                                        st.success("✅ Code exécuté avec succès ! Le graphique a été mis à jour.")
                                        st.rerun()
                                    else:
                                        st.warning("⚠️ Le code s'est exécuté mais aucun graphique n'a été généré.")
                        else:
                            st.warning("⚠️ Le code est vide.")
                
                with col_exec2:
                    if st.button("🔄 Réinitialiser"):
                        st.session_state.show_code_editor = False
                        st.rerun()
                
                # Informations utiles
                st.info("💡 **Conseils :**\n"
                       "- Modifiez le code directement dans la zone ci-dessus\n"
                       "- Le graphique doit être sauvegardé avec `plt.savefig('graphique.png')`\n"
                       "- Cliquez sur 'Exécuter' pour regénérer le graphique")
        else:
            # Message d'instruction
            st.info("👈 Uploadez un fichier de données et décrivez le graphique que vous souhaitez créer dans la zone de chat.")
            st.markdown("""
            **Exemples de demandes:**
            - "Trace la température en fonction du temps"
            - "Crée un graphique avec deux courbes : pression et volume"
            - "Ajoute une légende et des unités sur les axes"
            - "Change la couleur de la courbe en rouge"
            - "Ajoute une barre verticale à t=10s"
            """)

if __name__ == "__main__":
    main()


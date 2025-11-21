import pandas as pd
import subprocess
 
#################################### Useful functions ####################################
# Read csv or excel file (just the first sheet)
def read_data(data_file):
    ext = data_file.split('.')[-1]
   
    if ext == "xlsx":
        data = pd.read_excel(data_file)
    elif ext == "csv":
        data = pd.read_csv(data_file)
   
    # Recuperation des infos utiles
    infos = {
        "file_name": data_file,
        "shape": data.shape,
        "columns": data.columns.tolist(),
        "dtypes": data.dtypes.astype(str).to_dict()
            }
   
    return infos
 
def run_script(path):
    process = subprocess.run(
        ["python", path],
        capture_output=True,
        text=True
    )
    return process.stderr  # Contient l’erreur si crash
 
 
#################################### Context builder ####################################
def interpreteur_context(INTERPRETER_CONTEXT, initial_prompt, lecteur_output):
    interp_context = f"""
                            {INTERPRETER_CONTEXT}
                           
                            Voici la demande utilisateur :
                            {initial_prompt}
 
                            Voici le JSON récapitulant le contenu du fichier contenant les données à afficher :
                            {lecteur_output}
 
                            """
    return interp_context
 
def codeur_context(CODEUR_CONTEXT, interpreteur_output, lecteur_output):
    code_context = f"""
                            {CODEUR_CONTEXT}
                           
                            Voici le JSON structuré de la demande utilisateur :
                            {interpreteur_output}
 
                            Voici les metadonnees du dataframe contenant les données :
                            {lecteur_output}
 
                            """
    return code_context
 
def verificateur_context(VERIFICATEUR_CONTEXT, initial_prompt, interpreteur_output, codeur_output):
    verif_context = f"""
                            {VERIFICATEUR_CONTEXT}
                           
                            Voici la demande utilisateur :
                            {initial_prompt}
 
                            Voici le json structuré de la demande utilisateur :
                            {interpreteur_output}
 
                            Voici le code python :
                            {codeur_output}
                            """
    return verif_context
 
def debugger_context(DEBUGGER_CONTEXT, codeur_output, log):
    debug_context = f"""
                            {DEBUGGER_CONTEXT}
                            
                            Voici la code python contenant une ou plusieurs erreurs :
                            {codeur_output}
 
                            Voici le log d'erreur après l'avoir lancé :
                            {log}
                            """
    return debug_context
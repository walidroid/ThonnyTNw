from thonny import get_workbench
import tkinter as tk

def init_plugin():
    wb = get_workbench()
    wb.bind("WorkbenchReady", on_ready)
    wb.bind("EditorTextCreated", on_editor_created)
    print("✅ Plugin Snippets & Autoclose Intelligent chargé")

def on_ready(event):
    wb = get_workbench()
    # Récupérer l'éditeur actif s'il y en a un au démarrage
    editor_notebook = wb.get_editor_notebook()
    if editor_notebook:
        editor = editor_notebook.get_current_editor()
        if editor:
            bind_events(editor.get_text_widget())

def on_editor_created(event):
    bind_events(event.text_widget)

def bind_events(text_widget):
    # 1. Fermeture auto des paires ( (, [, ', " )
    text_widget.bind("<KeyPress>", on_key_press, add="+")
    
    # 2. Expansion IMMÉDIATE des mots-clés (Snippets)
    text_widget.bind("<KeyRelease>", on_key_release_trigger, add="+")
    
    # 3. Suppression intelligente des paires vides (Ajouté)
    # On utilise <BackSpace> sans "KeyPress" pour mieux intercepter l'événement
    text_widget.bind("<BackSpace>", on_backspace, add="+")

def on_backspace(event):
    """
    Supprime automatiquement la paire complète (ex: "|") si on efface l'ouvrant.
    """
    text_widget = event.widget
    
    try:
        # On récupère les caractères autour du curseur
        prev_char = text_widget.get("insert-1c", "insert")
        next_char = text_widget.get("insert", "insert+1c")
    except:
        return

    # Liste des paires à gérer
    pairs = {"(": ")", "[": "]", "'": "'", '"': '"', "{": "}"}
    
    # Si on est exactement entre une paire vide (ex: entre " et ")
    if prev_char in pairs and next_char == pairs[prev_char]:
        # On supprime TOUT (l'ouvrant et le fermant) d'un coup
        text_widget.delete("insert-1c", "insert+1c")
        
        # IMPORTANT : On bloque l'événement standard ("break") pour éviter que
        # Thonny n'essaie d'effacer encore une fois ou ne déplace le curseur bizarrement.
        return "break"

def on_key_release_trigger(event):
    """Vérifie et remplace le mot-clé immédiatement après la frappe"""
    text = event.widget
    
    # Optimisation : On ne vérifie que si nécessaire
    if not event.char or (not event.char.isalnum() and event.char not in [" ", "_"]):
        return

    if text.index("insert") == "1.0":
        return

    cursor_pos = text.index("insert")
    line_start = text.index("insert linestart")
    line_text = text.get(line_start, cursor_pos)
    
    # Dictionnaire des raccourcis
    snippets = {
        "for":     ("for i in range():", 2),
        "while":   ("while :", 1),
        "if":      ("if :", 1),
        "elif":    ("elif :", 1),
        "else":    ("else :", 0),
        "def":     ("def ():", 3),
        "true":    ("True", 0),
        "false":   ("False", 0),
        "print":   ("print()", 1),
        "input":   ("input()", 1),
        "randint": ("randint(,)", 2),
        "numpy":   ("numpy import array ", 0),
        "random":  ("random import randint ", 0),
        "set":     ("setText()", 1)
    }
    
    sorted_keys = sorted(snippets.keys(), key=len, reverse=True)
    
    match = None
    for key in sorted_keys:
        if line_text.endswith(key):
            # Vérification frontière (mot entier)
            start_index = len(line_text) - len(key)
            if start_index > 0:
                char_before = line_text[start_index - 1]
                if char_before.isalnum() or char_before == "_":
                    continue 
            
            match = key
            break
            
    if match:
        content, back_step = snippets[match]
        # On calcule la position de début du mot clé à remplacer
        start_delete = f"insert-{len(match)}c"
        text.delete(start_delete, "insert")
        text.insert("insert", content)
        if back_step > 0:
            text.mark_set("insert", f"insert-{back_step}c")

def on_key_press(event):
    """
    Gère la fermeture automatique intelligente.
    Ne double pas les guillemets si on est en train de fermer un mot.
    """
    char = event.char
    text_widget = event.widget
    pairs = {"(": ")", "[": "]", "'": "'", '"': '"'}
    
    if char in pairs:
        # --- 1. Vérification du SUIVANT (pour insertion au début d'un mot) ---
        try:
            next_char = text_widget.get("insert", "insert+1c")
        except:
            next_char = ""
            
        allowed_followers = ["", "\n", " ", "\t", ")", "]", "}", ",", ":", ";"]
        
        # Si le curseur est collé devant un mot (ex: |text), on n'autocomplète pas
        if next_char not in allowed_followers:
             return None 
        
        # --- 2. Vérification du PRÉCÉDENT (Spécial Guillemets) ---
        # Si on tape " ou ' juste après une lettre, on suppose qu'on veut FERMER la string
        if char in ['"', "'"]:
            try:
                prev_char = text_widget.get("insert-1c", "insert")
            except:
                prev_char = ""
            
            # Si le caractère précédent est une lettre ou un chiffre
            if prev_char.isalnum() or prev_char == "_":
                # Exception : Les préfixes f", r", b", u" doivent fonctionner
                is_prefix = False
                if prev_char.lower() in ['f', 'r', 'b', 'u']:
                    try:
                        # On vérifie qu'avant le 'f', ce n'est pas une autre lettre (ex: 'if"')
                        prev_prev = text_widget.get("insert-2c", "insert-1c")
                        if not prev_prev.isalnum() and prev_prev != "_":
                            is_prefix = True
                    except:
                        is_prefix = True # Début de fichier
                
                # Si ce n'est pas un préfixe (f,r..), c'est une fermeture de mot -> BLOQUER
                if not is_prefix:
                    return None

        # Si toutes les conditions sont remplies, on insère la paire
        text_widget.insert("insert", char + pairs[char])
        text_widget.mark_set("insert", "insert-1c")
        return "break"

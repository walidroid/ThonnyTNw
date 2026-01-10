from thonny import get_workbench
import tkinter as tk

def init_plugin():
    wb = get_workbench()
    wb.bind("WorkbenchReady", on_ready)
    wb.bind("EditorTextCreated", on_editor_created)
    print("✅ Plugin Snippets & Autoclose Intelligent chargé")

def on_ready(event):
    wb = get_workbench()
    editor = wb.get_editor_notebook().get_current_editor()
    if editor:
        bind_events(editor.get_text_widget())

def on_editor_created(event):
    bind_events(event.text_widget)

def bind_events(text_widget):
    # 1. Fermeture auto des paires ( (, [, ', " )
    # On garde KeyPress pour intercepter AVANT l'écriture
    text_widget.bind("<KeyPress>", on_key_press, add="+")
    
    # 2. Expansion IMMÉDIATE des mots-clés
    # On utilise KeyRelease pour vérifier le texte juste APRÈS que la lettre soit tapée
    text_widget.bind("<KeyRelease>", on_key_release_trigger, add="+")

def on_key_release_trigger(event):
    """Vérifie et remplace le mot-clé immédiatement après la frappe"""
    text = event.widget
    
    if not event.char or (not event.char.isalnum() and event.char not in [" ", "_"]):
        return

    if text.index("insert") == "1.0":
        return

    cursor_pos = text.index("insert")
    line_start = text.index("insert linestart")
    line_text = text.get(line_start, cursor_pos)
    
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
            start_index = len(line_text) - len(key)
            if start_index > 0:
                char_before = line_text[start_index - 1]
                if char_before.isalnum() or char_before == "_":
                    continue 
            
            match = key
            break
            
    if match:
        content, back_step = snippets[match]
        start_delete = f"insert-{len(match)}c"
        text.delete(start_delete, "insert")
        text.insert("insert", content)
        if back_step > 0:
            text.mark_set("insert", f"insert-{back_step}c")

def on_key_press(event):
    """
    Gère la fermeture automatique des parenthèses, crochets et guillemets.
    INTELLIGENT : N'agit que si le curseur est devant un espace ou une fin de ligne.
    """
    char = event.char
    text_widget = event.widget
    pairs = {"(": ")", "[": "]", "'": "'", '"': '"'}
    
    if char in pairs:
        # 1. On regarde ce qu'il y a juste après le curseur
        next_char = text_widget.get("insert", "insert+1c")
        
        # 2. Liste des caractères "sûrs" qui autorisent l'autocomplétion
        # On autorise l'autoclose si on est à la fin d'une ligne, devant un espace, 
        # ou devant une autre fermeture ), ], }
        allowed_followers = ["", "\n", " ", "\t", ")", "]", "}", ",", ":", ";"]
        
        # 3. Si le caractère suivant n'est PAS dans la liste (ex: c'est une lettre), 
        # on désactive l'autoclose pour ne pas gêner l'édition.
        if next_char not in allowed_followers:
            return None # Laisse Thonny insérer le caractère normalement (une seule fois)
            
        # Sinon, on insère la paire complète et on recule le curseur
        text_widget.insert("insert", char + pairs[char])
        text_widget.mark_set("insert", "insert-1c")
        return "break"

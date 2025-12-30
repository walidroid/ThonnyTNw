from thonny import get_workbench
import tkinter as tk

def init_plugin():
    wb = get_workbench()
    wb.bind("WorkbenchReady", on_ready)
    wb.bind("EditorTextCreated", on_editor_created)
    print("✅ Plugin Snippets chargé") # Message de confirmation dans le Shell

def on_ready(event):
    wb = get_workbench()
    editor = wb.get_editor_notebook().get_current_editor()
    if editor:
        bind_events(editor.get_text_widget())

def on_editor_created(event):
    bind_events(event.text_widget)

def bind_events(text_widget):
    # 1. Fermeture auto des paires ( (, [, ', " )
    text_widget.bind("<KeyPress>", on_key_press, add="+")
    
    # 2. Expansion des mots-clés avec la barre ESPACE
    text_widget.bind("<KeyPress-space>", on_space_trigger, add="+")

def on_space_trigger(event):
    text = event.widget
    
    # Sécurité position curseur
    if text.index("insert") == "1.0":
        return

    # 1. On récupère tout le texte de la ligne actuelle jusqu'au curseur
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
        "def":     ("def :", 1),
        "true":    ("True", 0),
        "false":   ("False", 0),
        "print":   ("print()", 1),
        "input":   ("input()", 1),
        "randint": ("randint(,)", 2),
        "numpy":   ("numpy import array", 0),
        "random":  ("random import randint", 0),
        "set":     ("setText()", 1)
    }
    
    # 2. On cherche si la ligne se termine par un de nos mots-clés
    # On trie par longueur pour vérifier les plus longs d'abord (ex: "from random" avant "random")
    sorted_keys = sorted(snippets.keys(), key=len, reverse=True)
    
    match = None
    for key in sorted_keys:
        if line_text.endswith(key):
            # Vérification frontière: pour éviter que "whatif" déclenche "if"
            # On vérifie que le caractère juste avant le mot n'est pas une lettre
            start_index = len(line_text) - len(key)
            if start_index > 0:
                char_before = line_text[start_index - 1]
                if char_before.isalnum() or char_before == "_":
                    continue # C'est un morceau d'un autre mot, on ignore
            
            match = key
            break
            
    if match:
        content, back_step = snippets[match]
        
        # 3. Supprimer le mot-clé tapé
        # On calcule la position de début de suppression
        start_delete = f"insert-{len(match)}c"
        text.delete(start_delete, "insert")
        
        # 4. Insérer le snippet complet
        text.insert("insert", content)
        
        # 5. Placer le curseur
        if back_step > 0:
            text.mark_set("insert", f"insert-{back_step}c")
            
        # IMPORTANT : empêche l'espace d'être inséré
        return "break"

def on_key_press(event):
    char = event.char
    text_widget = event.widget
    pairs = {"(": ")", "[": "]", "'": "'", '"': '"'}
    
    if char in pairs:
        text_widget.insert("insert", char + pairs[char])
        text_widget.mark_set("insert", "insert-1c")
        return "break"

from thonny import get_workbench
import tkinter as tk

def init_plugin():
    wb = get_workbench()
    wb.bind("WorkbenchReady", on_ready)
    wb.bind("EditorTextCreated", on_editor_created)
    print("✅ Plugin Snippets (Mode Instantané) chargé")

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
    
    # Optimisation : On ne vérifie que si la touche relâchée est une lettre, un chiffre ou un symbole visible
    # Cela évite de lancer le script sur "Shift", "Ctrl", etc.
    if not event.char or (not event.char.isalnum() and event.char not in [" ", "_"]):
        return

    # Sécurité position
    if text.index("insert") == "1.0":
        return

    # 1. On récupère la ligne actuelle jusqu'au curseur
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
    
    # 2. Analyse (On trie pour vérifier les mots les plus longs en premier)
    sorted_keys = sorted(snippets.keys(), key=len, reverse=True)
    
    match = None
    for key in sorted_keys:
        if line_text.endswith(key):
            # Vérification frontière (mot entier)
            # On vérifie que le caractère juste avant le mot n'est pas une lettre
            start_index = len(line_text) - len(key)
            if start_index > 0:
                char_before = line_text[start_index - 1]
                if char_before.isalnum() or char_before == "_":
                    continue # C'est la fin d'un autre mot (ex: "whatif" pour "if"), on ignore
            
            match = key
            break
            
    if match:
        content, back_step = snippets[match]
        
        # 3. Supprimer le mot-clé qui vient d'être tapé
        start_delete = f"insert-{len(match)}c"
        text.delete(start_delete, "insert")
        
        # 4. Insérer le snippet complet
        text.insert("insert", content)
        
        # 5. Placer le curseur
        if back_step > 0:
            text.mark_set("insert", f"insert-{back_step}c")

def on_key_press(event):
    """Gère la fermeture automatique des parenthèses"""
    char = event.char
    text_widget = event.widget
    pairs = {"(": ")", "[": "]", "'": "'", '"': '"'}
    
    if char in pairs:
        text_widget.insert("insert", char + pairs[char])
        text_widget.mark_set("insert", "insert-1c")
        return "break"

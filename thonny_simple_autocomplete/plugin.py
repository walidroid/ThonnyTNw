from thonny import get_workbench
import tkinter as tk

def init_plugin():
    wb = get_workbench()
    wb.bind("WorkbenchReady", on_ready)
    wb.bind("EditorTextCreated", on_editor_created)

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
    
    # 2. Expansion des mots-clés avec la barre ESPACE (Snippets)
    text_widget.bind("<KeyPress-space>", on_space_trigger, add="+")
    
    # (L'autocomplétion native <KeyRelease> a été supprimée)

def on_space_trigger(event):
    """Gère l'insertion automatique des structures (for, if, while...)"""
    text = event.widget
    
    # Sécurité si on est au tout début du fichier
    if text.index("insert") == "1.0":
        return

    # On récupère le mot juste avant le curseur
    word_start = "insert-1c wordstart"
    word = text.get(word_start, "insert")
    
    # Dictionnaire des raccourcis
    # Clé = mot tapé
    # Valeur = (Texte à insérer, Nombre de caractères pour reculer le curseur)
    snippets = {
        "for":   ("for i in range():", 2),  # Recule de 2 pour être dans ()
        "while": ("while :", 1),            # Recule de 1 pour être avant :
        "if":    ("if :", 1),               # Recule de 1 pour être avant :
        "elif":  ("elif :", 1),             # Recule de 1 pour être avant :
        "else":  ("else :", 0),             # Reste à la fin
        "def":   ("def :", 1),
        "print": ("print()", 1),
        "input": ("input()", 1),
        "randint": ("randint(,)", 2),
        "numpy": ("numpy import array",0),
        "random": ("random import randint",0)
        
    }
    
    if word in snippets:
        content, back_step = snippets[word]
        
        # 1. Supprimer le mot-clé tapé
        text.delete(word_start, "insert")
        
        # 2. Insérer le snippet complet
        text.insert("insert", content)
        
        # 3. Placer le curseur intelligemment
        if back_step > 0:
            text.mark_set("insert", f"insert-{back_step}c")
            
        # IMPORTANT : "break" empêche l'espace d'être inséré après le snippet
        return "break"

def on_key_press(event):
    """Gère la fermeture automatique des parenthèses, crochets et guillemets"""
    char = event.char
    text_widget = event.widget
    
    pairs = {
        "(": ")",
        "[": "]",
        "'": "'",
        '"': '"'
    }
    
    if char in pairs:
        # Insère la paire complète et recule le curseur
        text_widget.insert("insert", char + pairs[char])
        text_widget.mark_set("insert", "insert-1c")
        return "break"

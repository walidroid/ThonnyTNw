from thonny import get_workbench
import tkinter as tk

def init_plugin():
    wb = get_workbench()
    # On surveille l'ouverture de Thonny et la création de nouveaux onglets
    wb.bind("WorkbenchReady", on_ready)
    wb.bind("EditorTextCreated", on_editor_created)

def on_ready(event):
    wb = get_workbench()
    editor = wb.get_editor_notebook().get_current_editor()
    if editor:
        bind_events(editor.get_text_widget())

def on_editor_created(event):
    # event.text_widget est l'éditeur de texte du nouvel onglet
    bind_events(event.text_widget)

def bind_events(text_widget):
    # On utilise <Key> qui capte TOUTES les touches de manière brute
    # add="+" est crucial pour ne pas écraser les fonctions natives de Thonny
    text_widget.bind("<Key>", on_key_press, add="+")
    # On garde l'autocomplétion au relâchement
    text_widget.bind("<KeyRelease>", on_key_release, add="+")

def on_key_press(event):
    """Gère l'insertion manuelle des paires"""
    char = event.char
    text_widget = event.widget
    
    # Dictionnaire des caractères à fermer
    pairs = {
        "(": "()",
        "[": "[]",
        "'": "''",
        '"': '""'
    }
    
    if char in pairs:
        # 1. On insère la paire complète à la position du curseur
        text_widget.insert("insert", pairs[char])
        # 2. On déplace le curseur d'un caractère vers la gauche (au milieu)
        text_widget.mark_set("insert", "insert-1c")
        # 3. "break" dit à Thonny d'ignorer la touche originale pour éviter d'avoir ((
        return "break"

def on_key_release(event):
    """Déclenche la liste d'autocomplétion native de Thonny"""
    # On déclenche seulement si on tape du texte utile
    if event.char and (event.char.isalnum() or event.char in [".", "_"]):
        try:
            # Simule Ctrl+Espace pour ouvrir la petite liste de Thonny
            event.widget.event_generate("<Control-space>")
        except Exception:
            pass

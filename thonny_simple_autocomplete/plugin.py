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
    # 1. Gestion des fermetures automatiques
    # On utilise <KeyPress> générique pour capter le caractère réel (event.char)
    # "add='+'" permet de ne pas supprimer les autres raccourcis existants
    text_widget.bind("<KeyPress>", on_key_press, add="+")
    
    # 2. Autocomplétion Automatique
    # On écoute le relâchement de la touche
    text_widget.bind("<KeyRelease>", on_key_release, add="+")

def on_key_press(event):
    """Insère automatiquement la paire correspondante"""
    char = event.char
    widget = event.widget
    
    # Dictionnaire des paires à fermer
    pairs = {
        "(": "()",
        "[": "[]",
        "'": "''",
        '"': '""'
    }
    
    # Si le caractère tapé est dans notre liste
    if char in pairs:
        # 1. On insère la paire complète (ex: [])
        widget.insert("insert", pairs[char])
        # 2. On recule le curseur d'un caractère pour le placer au milieu
        widget.mark_set("insert", "insert-1c")
        # 3. IMPORTANT : "break" empêche Tkinter d'écrire le caractère une 2ème fois
        return "break"

def on_key_release(event):
    """Déclenche l'autocomplétion native de Thonny"""
    # Si c'est une lettre, un chiffre, un point ou un underscore
    if event.char and (event.char.isalnum() or event.char in [".", "_"]):
        try:
            # Simule l'appui sur Ctrl+Espace
            event.widget.event_generate("<Control-space>")
        except Exception:
            pass

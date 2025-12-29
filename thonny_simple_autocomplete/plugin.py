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
    # On intercepte la touche (KeyPress) pour insérer nous-mêmes la paire
    text_widget.bind("<KeyPress-parenleft>", on_open_paren)      # (
    text_widget.bind("<KeyPress-bracketleft>", on_open_bracket)  # [
    text_widget.bind("<KeyPress-apostrophe>", on_single_quote)   # '
    text_widget.bind("<KeyPress-quotedbl>", on_double_quote)     # "
    
    # 2. Autocomplétion Automatique
    # On écoute le relâchement de la touche (KeyRelease)
    text_widget.bind("<KeyRelease>", on_key_release)

def insert_close_char(text_widget, char_pair):
    """Fonction utilitaire pour insérer une paire et reculer le curseur"""
    # Insère la paire complète (ex: [])
    text_widget.insert("insert", char_pair)
    # Recule le curseur d'un caractère pour le placer au milieu
    text_widget.mark_set("insert", "insert-1c")
    # Empêche Tkinter d'insérer le caractère une deuxième fois
    return "break"

def on_open_paren(event):
    return insert_close_char(event.widget, "()")

def on_open_bracket(event):
    return insert_close_char(event.widget, "[]")

def on_single_quote(event):
    return insert_close_char(event.widget, "''")

def on_double_quote(event):
    return insert_close_char(event.widget, '""')

def on_key_release(event):
    """Déclenche l'autocomplétion native de Thonny"""
    # Déclenche l'autocomplétion seulement si on tape des lettres, chiffres, . ou _
    # On ignore les quote/crochets pour ne pas gêner
    if event.char and (event.char.isalnum() or event.char in [".", "_"]):
        text_widget = event.widget
        try:
            # Simule l'appui sur Ctrl+Espace pour ouvrir la liste native
            text_widget.event_generate("<Control-space>")
        except Exception:
            pass

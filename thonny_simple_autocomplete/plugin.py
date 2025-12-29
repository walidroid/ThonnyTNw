from thonny import get_workbench
import tkinter as tk

def init_plugin():
    wb = get_workbench()
    # On s'assure de l'ajouter sur les éditeurs déjà ouverts et les futurs
    wb.bind("WorkbenchReady", on_ready)
    wb.bind("EditorTextCreated", on_editor_created)

def on_ready(event):
    wb = get_workbench()
    editor = wb.get_editor_notebook().get_current_editor()
    if editor:
        bind_events(editor.get_text_widget())

def on_editor_created(event):
    # event.text_widget est fourni par Thonny lors de la création d'un onglet
    bind_events(event.text_widget)

def bind_events(text_widget):
    # On écoute TOUTES les touches pressées
    text_widget.bind("<Key>", on_key_press, add="+")
    # On garde le déclenchement de l'autocomplétion au relâchement
    text_widget.bind("<KeyRelease>", on_key_release, add="+")

def on_key_press(event):
    """Vérifie le caractère inséré juste après la frappe"""
    text = event.widget
    # On attend 1ms que le caractère soit réellement écrit dans le widget
    text.after(1, lambda: check_and_close(text))

def check_and_close(text):
    """Insère la fermeture si un ouvrant vient d'être tapé"""
    try:
        # On regarde le caractère juste avant le curseur
        pos = text.index("insert")
        last_char = text.get("insert-1c")
        
        pairs = {
            "(": ")",
            "[": "]",
            "'": "'",
            '"': '"'
        }
        
        if last_char in pairs:
            # On insère le caractère de fermeture
            text.insert("insert", pairs[last_char])
            # On replace le curseur entre les deux
            text.mark_set("insert", pos)
    except Exception:
        pass

def on_key_release(event):
    """Déclenche l'autocomplétion native de Thonny (sans l'aide intrusive)"""
    # Déclenche seulement pour les lettres, chiffres, points et underscores
    if event.char and (event.char.isalnum() or event.char in [".", "_"]):
        try:
            # Simule Ctrl+Espace pour ouvrir la liste standard de Thonny
            event.widget.event_generate("<Control-space>")
        except Exception:
            pass

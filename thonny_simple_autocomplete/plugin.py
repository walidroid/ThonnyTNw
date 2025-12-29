from thonny import get_workbench
import builtins
import inspect
from .popup import show_popup

def init_plugin():
    wb = get_workbench()
    # S'exécute au démarrage de Thonny
    wb.bind("WorkbenchReady", on_ready)
    # S'exécute chaque fois qu'un nouvel onglet/fichier est ouvert
    wb.bind("EditorTextCreated", on_editor_created)

def on_ready(event):
    wb = get_workbench()
    editor = wb.get_editor_notebook().get_current_editor()
    if editor:
        bind_events(editor.get_text_widget())

def on_editor_created(event):
    # event.text_widget est la zone de texte du nouvel onglet
    bind_events(event.text_widget)

def bind_events(text_widget):
    # Garder le raccourci manuel Ctrl+Espace
    text_widget.bind("<Control-space>", on_autocomplete)
    # AJOUT : Déclenchement automatique lorsqu'on relâche une touche
    text_widget.bind("<KeyRelease>", on_automatic_trigger)

def on_automatic_trigger(event):
    # On ne déclenche que si la touche est une lettre, un chiffre ou un underscore.
    # Cela évite les popups intempestifs sur les touches Shift, Ctrl, Flèches, etc.
    if event.char and (event.char.isalnum() or event.char == "_"):
        on_autocomplete(event)

def on_autocomplete(event):
    # event.widget récupère la zone de texte active
    text = event.widget

    code = text.get("1.0", "insert")
    word = get_last_word(code)

    if not word:
        return

    # Recherche dans les fonctions natives (builtins) comme print, len, etc.
    fn = getattr(builtins, word, None)
    if fn:
        try:
            # Récupère la signature (ex: print(value, ...))
            signature = word + str(inspect.signature(fn))
            show_popup(text, signature)
        except:
            pass

def get_last_word(code):
    word = ""
    # On parcourt le texte à l'envers depuis le curseur
    for ch in reversed(code):
        if ch.isalnum() or ch == "_":
            word = ch + word
        else:
            break
    return word

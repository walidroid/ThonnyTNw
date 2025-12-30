from thonny import get_workbench
import tkinter as tk

def init_plugin():
    wb = get_workbench()
    # On bind sur les éditeurs existants et les futurs
    wb.bind("WorkbenchReady", on_ready)
    wb.bind("EditorTextCreated", on_editor_created)

def on_ready(event):
    wb = get_workbench()
    editor = wb.get_editor_notebook().get_current_editor()
    if editor:
        bind_events(editor.get_text_widget())

def on_editor_created(event):
    # event.text_widget est fourni par Thonny pour chaque nouvel onglet
    bind_events(event.text_widget)

def bind_events(text_widget):
    # On utilise KeyPress pour la fermeture automatique
    text_widget.bind("<KeyPress>", on_key_press, add="+")
    # On utilise KeyRelease pour l'autocomplétion
    text_widget.bind("<KeyRelease>", on_key_release, add="+")

def on_key_press(event):
    """Gère la fermeture automatique des parenthèses, crochets et guillemets"""
    char = event.char
    text_widget = event.widget
    
    # Dictionnaire des paires
    pairs = {
        "(": ")",
        "[": "]",
        "'": "'",
        '"': '"',
        "while":":",
        "if":":",
        "else":":",
        "elif":":",
        "for":"i in range"
    }
    
    if char in pairs:
        # On insère le caractère ouvrant ET le fermant d'un coup
        # Puis on place le curseur au milieu
        text_widget.insert("insert", char + pairs[char])
        text_widget.mark_set("insert", "insert-1c")
        
        # 'break' est CRUCIAL : il empêche Thonny d'insérer 
        # le caractère une deuxième fois (ce qui ferait (( )
        return "break"

def on_key_release(event):
    """Déclenche l'autocomplétion native de Thonny"""
    # On ne déclenche que pour les caractères alphanumériques (lettres/chiffres)
    if event.char and (event.char.isalnum() or event.char in [".", "_"]):
        try:
            # Simule l'appui sur Ctrl+Espace pour ouvrir la liste de Thonny
            event.widget.event_generate("<Control-space>")
        except:
            pass

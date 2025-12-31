from thonny import get_workbench
import tkinter as tk

def update_ui(event=None):
    """
    Met à jour le texte du bouton. 
    L'argument 'event' est nécessaire pour le binding.
    """
    wb = get_workbench()
    # On récupère le backend actuel
    backend = wb.get_option("run.backend_name")
    
    # Définition du texte (On utilise 'in' pour plus de souplesse)
    if "ESP32" in backend:
        btn_text = "ESP32"
    else:
        btn_text = "PYTHON 3"
        
    # 1. Mise à jour de la commande interne (pour les menus)
    if "toggle_py3_esp32" in wb._commands:
        cmd = wb._commands["toggle_py3_esp32"]
        cmd.caption = btn_text
        cmd.command_label = btn_text

    # 2. Mise à jour visuelle du bouton dans la barre d'outils
    toolbar = wb.get_toolbar()
    for child in toolbar.winfo_children():
        # Thonny marque ses boutons de toolbar avec 'command_id'
        if getattr(child, "command_id", None) == "toggle_py3_esp32":
            try:
                # Force le texte sur le widget Tkinter
                child.configure(text=btn_text)
                # Force le rafraîchissement graphique immédiat
                child.update_idletasks()
            except Exception:
                pass
            break

def switch_interpreter():
    """Bascule l'interpréteur"""
    wb = get_workbench()
    current_backend = wb.get_option("run.backend_name")
    
    
    if "ESP32" in current_backend:
        wb.set_option("run.backend_name", "LocalCPython")
    else:
        wb.set_option("run.backend_name", "ESP32")

   
    try:
        wb.restart_backend(clean=True)
    except:
        pass
    
    # Feedback immédiat sur le titre de la fenêtre
    wb.update_title()

def load_plugin():
    """Initialise le plugin"""
    wb = get_workbench()
    
    current = wb.get_option("run.backend_name")
    initial_text = "ESP32" if "ESP32" in current else "PYTHON 3"

    wb.add_command(
        command_id="toggle_py3_esp32",
        menu_name="tools",
        command_label=initial_text,
        handler=switch_interpreter,
        caption=initial_text,
        include_in_toolbar=True
    )
    

    wb.bind("BackendRestarted", update_ui, True)
    
    wb.after_idle(update_ui)

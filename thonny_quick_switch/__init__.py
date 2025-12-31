from thonny import get_workbench
import tkinter as tk

def update_ui(event=None):
    """Met à jour le texte du bouton. Accepte un argument 'event' pour le binding."""
    wb = get_workbench()
    current_backend = wb.get_option("run.backend_name")
    
    # Choix du texte
    if current_backend == "ESP32":
        btn_text = "ESP32"
    else:
        btn_text = "PYTHON 3"
        
    # 1. Mise à jour de l'objet commande interne (pour la persistance)
    if "toggle_py3_esp32" in wb._commands:
        cmd = wb._commands["toggle_py3_esp32"]
        cmd.caption = btn_text
        cmd.command_label = btn_text

    # 2. Mise à jour visuelle du bouton Tkinter
    toolbar = wb.get_toolbar()
    for child in toolbar.winfo_children():
        if getattr(child, "command_id", None) == "toggle_py3_esp32":
            try:
                child.configure(text=btn_text)
            except Exception:
                pass
            break

def switch_interpreter():
    """Bascule l'option et lance le redémarrage"""
    wb = get_workbench()
    current_backend = wb.get_option("run.backend_name")
    
    # Bascule
    if current_backend == "LocalCPython":
        wb.set_option("run.backend_name", "ESP32")
    else:
        wb.set_option("run.backend_name", "LocalCPython")

    # Redémarrage (C'est ce qui déclenchera 'BackendRestarted' plus tard)
    try:
        wb.restart_backend(clean=True)
    except:
        pass
    
    # On met à jour le titre tout de suite pour donner un feedback immédiat
    wb.update_title()

def load_plugin():
    """Initialise le plugin"""
    wb = get_workbench()
    
    current = wb.get_option("run.backend_name")
    initial_text = "ESP32" if current == "ESP32" else "PYTHON 3"

    wb.add_command(
        command_id="toggle_py3_esp32",
        menu_name="tools",
        command_label=initial_text,
        handler=switch_interpreter,
        caption=initial_text,
        include_in_toolbar=True
    )
    
    # C'est LA clé du succès :
    # On demande à Thonny d'appeler update_ui à chaque fois que le backend a fini de redémarrer.
    # Le 'True' à la fin signifie qu'on veut recevoir l'événement même si on n'est pas au premier plan.
    wb.bind("BackendRestarted", update_ui, True)
    
    # Mise à jour initiale au lancement
    wb.after_idle(update_ui)

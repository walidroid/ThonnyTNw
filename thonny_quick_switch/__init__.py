from thonny import get_workbench

def update_ui():
    """Force la mise à jour immédiate du texte du bouton dans la barre d'outils"""
    wb = get_workbench()
    current_backend = wb.get_option("run.backend_name")
    
    # Définition du texte selon le mode actif
    if current_backend == "ESP32":
        btn_text = "ESP32"
    else:
        btn_text = "PYTHON 3"
        
    # 1. Mise à jour de la logique interne (pour les menus)
    if "toggle_py3_esp32" in wb._commands:
        cmd = wb._commands["toggle_py3_esp32"]
        cmd.caption = btn_text
        cmd.command_label = btn_text

    # 2. Mise à jour visuelle du bouton dans la barre d'outils
    # On récupère la barre d'outils de Thonny
    toolbar = wb.get_toolbar()
    for child in toolbar.winfo_children():
        # Thonny stocke l'ID de la commande dans l'attribut 'command_id' du widget
        if getattr(child, "command_id", None) == "toggle_py3_esp32":
            # On change le texte du bouton Tkinter directement
            child.config(text=btn_text)
            break

def switch_interpreter():
    """Bascule l'interpréteur et rafraîchit l'UI"""
    wb = get_workbench()
    current_backend = wb.get_option("run.backend_name")
    
    # Changement de l'option Thonny
    if current_backend == "LocalCPython":
        wb.set_option("run.backend_name", "ESP32")
    else:
        wb.set_option("run.backend_name", "LocalCPython")

    # On force le redémarrage du moteur Python
    try:
        wb.restart_backend(clean=True)
    except:
        pass
        
    # Mise à jour immédiate de l'affichage
    update_ui()
    wb.update_title()

def load_plugin():
    """Initialise le plugin au chargement de Thonny"""
    wb = get_workbench()
    
    # Détecter l'état actuel au lancement
    current = wb.get_option("run.backend_name")
    initial_text = "ESP32" if current == "ESP32" else "PYTHON 3"

    # Création de la commande initiale
    wb.add_command(
        command_id="toggle_py3_esp32",
        menu_name="tools",
        command_label=initial_text,
        handler=switch_interpreter,
        caption=initial_text,
        include_in_toolbar=True
    )

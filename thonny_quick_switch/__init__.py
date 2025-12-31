from thonny import get_workbench

def update_menu_status(event=None):
    """Met à jour les coches (checkmarks) dans le menu Outils selon l'interpréteur actif"""
    wb = get_workbench()
    current_backend = wb.get_option("run.backend_name")
    
    # On accède aux commandes pour changer leur état 'checked'
    # 'switch_to_python3' et 'switch_to_esp32' sont les IDs définis dans load_plugin
    try:
        if "switch_to_python3" in wb._commands:
            wb._commands["switch_to_python3"].checked = (current_backend == "LocalCPython")
        
        if "switch_to_esp32" in wb._commands:
            wb._commands["switch_to_esp32"].checked = (current_backend == "ESP32")
    except Exception:
        pass

def select_python3():
    """Action pour activer Python 3"""
    wb = get_workbench()
    wb.set_option("run.backend_name", "LocalCPython")
    try:
        wb.restart_backend(clean=True)
    except:
        pass
    # Mise à jour immédiate des coches
    update_menu_status()

def select_esp32():
    """Action pour activer l'ESP32"""
    wb = get_workbench()
    wb.set_option("run.backend_name", "ESP32")
    try:
        wb.restart_backend(clean=True)
    except:
        pass
    # Mise à jour immédiate des coches
    update_menu_status()

def load_plugin():
    """Initialise le plugin avec deux options dans le menu Outils"""
    wb = get_workbench()
    
    # 1. Ajouter l'option Python 3 dans le menu Outils (Tools)
    wb.add_command(
        command_id="switch_to_python3",
        menu_name="tools",
        command_label="Mode : Python 3",
        handler=select_python3,
        include_in_toolbar=False, # On retire de la barre d'outils
        group=110                 # Groupement pour mettre les deux options ensemble
    )
    
    wb.add_command(
        command_id="switch_to_esp32",
        menu_name="tools",
        command_label="Mode : ESP32",
        handler=select_esp32,
        include_in_toolbar=False, # On retire de la barre d'outils
        group=110
    )
    
  
    wb.bind("BackendRestarted", update_menu_status, True)
    
    # 4. Initialisation visuelle au démarrage de Thonny
    wb.after_idle(update_menu_status)

from thonny import get_workbench

def is_python3_active():
    """Retourne True si l'interpréteur actuel est Python 3"""
    return get_workbench().get_option("run.backend_name") == "LocalCPython"

def is_esp32_active():
    """Retourne True si l'interpréteur actuel est l'ESP32"""
    # On vérifie si le nom contient ESP32
    return get_workbench().get_option("run.backend_name") == "ESP32"

def select_python3():
    """Bascule vers Python 3"""
    wb = get_workbench()
    wb.set_option("run.backend_name", "LocalCPython")
    try:
        wb.restart_backend(clean=True)
    except:
        pass

def select_esp32():
    """Bascule vers l'ESP32"""
    wb = get_workbench()
    wb.set_option("run.backend_name", "ESP32")
    try:
        wb.restart_backend(clean=True)
    except:
        pass

def load_plugin():
    """Initialise le plugin avec les options cochables dans le menu Outils"""
    wb = get_workbench()
    
    # Option Python 3
    wb.add_command(
        command_id="switch_to_python3",
        menu_name="tools",
        command_label="Mode : Python 3",
        handler=select_python3,
        tester=is_python3_active, # Thonny ajoute le ✓ si cette fonction renvoie True
        include_in_toolbar=False,
        group=110
    )
    
    # Option ESP32
    wb.add_command(
        command_id="switch_to_esp32",
        menu_name="tools",
        command_label="Mode : ESP32",
        handler=select_esp32,
        tester=is_esp32_active,   # Thonny ajoute le ✓ si cette fonction renvoie True
        include_in_toolbar=False,
        group=110
    )

from thonny import get_workbench

def is_python3_active():
    """Vérifie si Python 3 est l'interpréteur actuel"""
    try:
        return get_workbench().get_option("run.backend_name") == "LocalCPython"
    except Exception:
        return False

def is_esp32_active():
    """Vérifie si ESP32 est l'interpréteur actuel"""
    try:
        # On vérifie la valeur exacte utilisée dans vos paramètres
        return get_workbench().get_option("run.backend_name") == "ESP32"
    except Exception:
        return False

def select_python3():
    """Bascule vers Python 3 et redémarre"""
    wb = get_workbench()
    wb.set_option("run.backend_name", "LocalCPython")
    try:
        wb.restart_backend(clean=True)
    except:
        pass

def select_esp32():
    """Bascule vers ESP32 et redémarre"""
    wb = get_workbench()
    wb.set_option("run.backend_name", "ESP32")
    try:
        wb.restart_backend(clean=True)
    except:
        pass

def load_plugin():
    """Initialise le menu avec des options cochables"""
    wb = get_workbench()
    
    # Option Python 3
    wb.add_command(
        command_id="switch_to_python3",
        menu_name="tools",
        command_label="Utiliser Python 3",
        handler=select_python3,
        tester=is_python3_active, # Affiche le ✓ si True
        group=110,
        include_in_toolbar=False
    )
    
    # Option ESP32
    wb.add_command(
        command_id="switch_to_esp32",
        menu_name="tools",
        command_label="Utiliser ESP32",
        handler=select_esp32,
        tester=is_esp32_active,   # Affiche le ✓ si True
        group=110,
        include_in_toolbar=False
    )

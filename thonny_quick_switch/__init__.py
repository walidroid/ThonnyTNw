from thonny import get_workbench

# --- Détection du mode actif ---

def is_python3_active():
    return get_workbench().get_option("run.backend_name") == "LocalCPython"

def is_esp32_active():
    return get_workbench().get_option("run.backend_name") == "ESP32"


# --- Actions ---

def select_python3():
    wb = get_workbench()
    if not is_python3_active():
        wb.set_option("run.backend_name", "LocalCPython")
        try:
            wb.restart_backend(clean=True)
        except:
            pass

def select_esp32():
    wb = get_workbench()
    if not is_esp32_active():
        wb.set_option("run.backend_name", "ESP32")
        try:
            wb.restart_backend(clean=True)
        except:
            pass


# --- Menu radio (✓ = actif) ---

def load_plugin():
    wb = get_workbench()

    wb.add_command(
        command_id="radio_python3",
        menu_name="tools",
        command_label="● Mode Python 3",
        handler=select_python3,
        tester=is_python3_active,
        group=110
    )

    wb.add_command(
        command_id="radio_esp32",
        menu_name="tools",
        command_label="● Mode ESP32",
        handler=select_esp32,
        tester=is_esp32_active,
        group=110
    )

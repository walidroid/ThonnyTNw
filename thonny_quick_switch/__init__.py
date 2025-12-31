from thonny import get_workbench

# --- Helpers ---

def get_backend():
    return get_workbench().get_option("run.backend_name")

def refresh_menu():
    wb = get_workbench()

    python_label = "◉ Mode Python 3" if get_backend() == "LocalCPython" else "◯ Mode Python 3"
    esp_label = "◉ Mode ESP32" if get_backend() == "ESP32" else "◯ Mode ESP32"

    wb.remove_command("tools", "mode_python3")
    wb.remove_command("tools", "mode_esp32")

    wb.add_command(
        command_id="mode_python3",
        menu_name="tools",
        command_label=python_label,
        handler=select_python3,
        group=110
    )

    wb.add_command(
        command_id="mode_esp32",
        menu_name="tools",
        command_label=esp_label,
        handler=select_esp32,
        group=110
    )


# --- Actions ---

def select_python3():
    wb = get_workbench()
    wb.set_option("run.backend_name", "LocalCPython")
    try:
        wb.restart_backend(clean=True)
    except:
        pass
    refresh_menu()

def select_esp32():
    wb = get_workbench()
    wb.set_option("run.backend_name", "ESP32")
    try:
        wb.restart_backend(clean=True)
    except:
        pass
    refresh_menu()


# --- Plugin init ---

def load_plugin():
    refresh_menu()

from thonny import get_workbench

def always_enabled():
    return True

def select_python3():
    wb = get_workbench()
    wb.set_option("run.backend_name", "LocalCPython")
    try:
        wb.restart_backend(clean=True)
    except:
        pass

def select_esp32():
    wb = get_workbench()
    wb.set_option("run.backend_name", "ESP32")
    try:
        wb.restart_backend(clean=True)
    except:
        pass

def load_plugin():
    wb = get_workbench()

    wb.add_command(
        command_id="switch_to_python3",
        menu_name="tools",
        command_label="Mode : Python 3",
        handler=select_python3,
        tester=always_enabled,
        group=110
    )

    wb.add_command(
        command_id="switch_to_esp32",
        menu_name="tools",
        command_label="Mode : ESP32",
        handler=select_esp32,
        tester=always_enabled,
        group=110
    )

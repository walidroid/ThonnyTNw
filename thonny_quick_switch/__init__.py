from thonny import get_workbench
from tkinter import messagebox

# -------------------------------------------------
# Utilitaires
# -------------------------------------------------

def get_backend():
    return get_workbench().get_option("run.backend_name")


def update_labels():
    """Met à jour l'affichage radio (◉ / ◯)"""
    wb = get_workbench()

    python_label = (
        "◉ Mode Python (ordinateur)"
        if get_backend() == "LocalCPython"
        else "◯ Mode Python (ordinateur)"
    )

    esp_label = (
        "◉ Mode ESP32 (carte)"
        if get_backend() == "ESP32"
        else "◯ Mode ESP32 (carte)"
    )

    wb.set_command_label("mode_python", python_label)
    wb.set_command_label("mode_esp32", esp_label)


# -------------------------------------------------
# Actions
# -------------------------------------------------

def select_python():
    wb = get_workbench()
    wb.set_option("run.backend_name", "LocalCPython")

    try:
        wb.restart_backend(clean=True)
    except:
        pass

    messagebox.showinfo(
        "Mode Python",
        "Le programme s'exécutera sur l'ordinateur."
    )

    update_labels()


def select_esp32():
    wb = get_workbench()
    wb.set_option("run.backend_name", "ESP32")

    try:
        wb.restart_backend(clean=True)
    except:
        pass

    messagebox.showinfo(
        "Mode ESP32",
        "Le programme s'exécutera sur la carte ESP32.\n\n"
        "Vérifie que la carte est branchée."
    )

    update_labels()


# -------------------------------------------------
# Initialisation du plugin
# -------------------------------------------------

def load_plugin():
    wb = get_workbench()

    wb.add_command(
        command_id="mode_python",
        menu_name="tools",
        command_label="Mode Python",
        handler=select_python,
        group=110
    )

    wb.add_command(
        command_id="mode_esp32",
        menu_name="tools",
        command_label="Mode ESP32",
        handler=select_esp32,
        group=110
    )

    update_labels()

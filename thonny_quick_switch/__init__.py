from thonny import get_workbench
from tkinter import messagebox

MENU_PYTHON = None
MENU_ESP32 = None


# -------------------------------------------------
# Utilitaires
# -------------------------------------------------

def get_backend():
    return get_workbench().get_option("run.backend_name")


def update_menu_labels():
    """
    Met à jour les symboles ◉ / ◯ dans le menu Outils
    en utilisant Tkinter directement (méthode stable)
    """
    global MENU_PYTHON, MENU_ESP32

    wb = get_workbench()
    tools_menu = wb.get_menu("tools")

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

    tools_menu.entryconfig(MENU_PYTHON, label=python_label)
    tools_menu.entryconfig(MENU_ESP32, label=esp_label)


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

    update_menu_labels()


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

    update_menu_labels()


# -------------------------------------------------
# Initialisation du plugin
# -------------------------------------------------

def load_plugin():
    global MENU_PYTHON, MENU_ESP32

    wb = get_workbench()
    tools_menu = wb.get_menu("tools")

    # Ajouter les commandes normalement
    tools_menu.add_command(
        label="Mode Python (ordinateur)",
        command=select_python
    )
    MENU_PYTHON = tools_menu.index("end")

    tools_menu.add_command(
        label="Mode ESP32 (carte)",
        command=select_esp32
    )
    MENU_ESP32 = tools_menu.index("end")

    update_menu_labels()

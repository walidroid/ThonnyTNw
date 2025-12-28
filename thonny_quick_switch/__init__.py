from thonny import get_workbench

def update_ui():
    """Met à jour le texte du bouton selon l'interpréteur actif"""
    wb = get_workbench()
    current_backend = wb.get_option("run.backend_name")
    
    # Définition du texte selon le mode
    if current_backend == "ESP32":
        btn_text = "⚡ ESP32"
    else:
        btn_text = "🐍 PYTHON"
        
    # CORRECTION : On accède à la commande via le workbench
    # Thonny stocke les commandes dans _commands
    if "toggle_py3_esp32" in wb._commands:
        cmd = wb._commands["toggle_py3_esp32"]
        # Mise à jour directe des attributs de l'objet commande
        cmd.caption = btn_text
        cmd.command_label = btn_text

def switch_interpreter():
    """Bascule entre Python local et ESP32"""
    wb = get_workbench()
    current_backend = wb.get_option("run.backend_name")
    
    # Logique de bascule
    if current_backend == "LocalCPython":
        wb.set_option("run.backend_name", "ESP32")
    else:
        wb.set_option("run.backend_name", "LocalCPython")

    # Redémarrage du backend
    try:
        wb.restart_backend(clean=True)
    except:
        pass
        
    # Mise à jour de l'interface
    update_ui()
    wb.update_title()

def load_plugin():
    """Initialise le plugin au démarrage"""
    wb = get_workbench()
    
    current = wb.get_option("run.backend_name")
    initial_text = "⚡ MODE : ESP32" if current == "ESP32" else "🐍 MODE : PYTHON 3"

    wb.add_command(
        command_id="toggle_py3_esp32",
        menu_name="tools",
        command_label=initial_text,
        handler=switch_interpreter,
        caption=initial_text,
        include_in_toolbar=True
    )

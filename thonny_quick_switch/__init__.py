from thonny import get_workbench

def update_ui():
    """Met à jour le texte du bouton selon l'interpréteur actif"""
    wb = get_workbench()
    current_backend = wb.get_option("run.backend_name")
    
    # On définit un texte explicite avec un symbole pour plus de clarté
    if current_backend == "ESP32":
        btn_text = "⚡ MODE : ESP32"
    else:
        btn_text = "🐍 MODE : PYTHON 3"
        
    # On récupère la commande pour modifier son étiquette (label et caption)
    cmd = wb.get_command("toggle_py3_esp32")
    if cmd:
        cmd.caption = btn_text
        cmd.label = btn_text

def switch_interpreter():
    """Bascule entre Python local et ESP32"""
    wb = get_workbench()
    current_backend = wb.get_option("run.backend_name")
    
    # Logique de bascule
    if current_backend == "LocalCPython":
        wb.set_option("run.backend_name", "ESP32")
    else:
        wb.set_option("run.backend_name", "LocalCPython")

    # Redémarrage du backend pour appliquer le changement
    try:
        wb.restart_backend(clean=True)
    except:
        pass
        
    # Mise à jour immédiate du texte du bouton et du titre de la fenêtre
    update_ui()
    wb.update_title()

def load_plugin():
    """Initialise le plugin au démarrage de Thonny"""
    wb = get_workbench()
    
    # Déterminer le texte initial selon le dernier interpréteur utilisé
    current = wb.get_option("run.backend_name")
    initial_text = "⚡ MODE : ESP32" if current == "ESP32" else "🐍 MODE : PYTHON 3"

    wb.add_command(
        command_id="toggle_py3_esp32",
        menu_name="tools",
        command_label=initial_text,
        handler=switch_interpreter,
        caption=initial_text, # Texte qui s'affiche sur le bouton de la barre d'outils
        include_in_toolbar=True
    )

from thonny import get_workbench
import tkinter as tk

def select_interpreter(backend_name):
    """Change l'interpréteur et force le redémarrage"""
    wb = get_workbench()
    wb.set_option("run.backend_name", backend_name)
    try:
        # Le redémarrage applique le changement d'interpréteur
        wb.restart_backend(clean=True)
    except Exception:
        pass

def load_plugin():
    wb = get_workbench()
    
    # 1. On crée/récupère le menu "Interpréteur" via l'API Thonny.
    # C'est la méthode la plus stable pour éviter les erreurs 'AttributeError'.
    interpreter_menu = wb.get_menu("interpreter_switch", "Interpréteur")
    
    def refresh_menu():
        """Reconstruit le menu avec le symbole ✓ au moment où l'on clique dessus"""
        # On vide le menu existant
        interpreter_menu.delete(0, "end")
        
        # On récupère l'interpréteur actuellement configuré
        current = wb.get_option("run.backend_name")
        
        # Option Python 3
        # On utilise add_command de Tkinter pour qu'il reste TOUJOURS cliquable
        py_label = "✓ Python 3" if current == "LocalCPython" else "    Python 3"
        interpreter_menu.add_command(
            label=py_label, 
            command=lambda: select_interpreter("LocalCPython")
        )
        
        # Option ESP32
        esp_label = "✓ ESP32" if current == "ESP32" else "    ESP32"
        interpreter_menu.add_command(
            label=esp_label, 
            command=lambda: select_interpreter("ESP32")
        )

    # 2. On utilise 'postcommand' de Tkinter : cette fonction s'exécute
    # à chaque fois que l'utilisateur clique sur le mot "Interpréteur".
    # Cela garantit que la coche ✓ est toujours à la bonne place.
    interpreter_menu.configure(postcommand=refresh_menu)

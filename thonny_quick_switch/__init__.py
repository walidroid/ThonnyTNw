from thonny import get_workbench
import tkinter as tk

def select_interpreter(backend_name):
    """Change l'interpréteur et force le redémarrage immédiat"""
    wb = get_workbench()
    wb.set_option("run.backend_name", backend_name)
    try:
        # On force le redémarrage pour appliquer le changement
        wb.restart_backend(clean=True)
    except Exception:
        pass

def load_plugin():
    wb = get_workbench()
    menubar = wb.get_menubar()
    
    # 1. Création d'un nouveau menu "Interprète" dans la barre du haut
    # Ce menu indépendant ne subit pas les restrictions du menu "Outils"
    interpreter_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Interprète", menu=interpreter_menu)
    
    def refresh_menu():
        """Reconstruit le menu avec le symbole ✓ devant l'option active"""
        # On vide le menu
        interpreter_menu.delete(0, "end")
        
        # On récupère l'interpréteur actuel
        current = wb.get_option("run.backend_name")
        
        # Option Python 3
        py_label = "✓ Python 3" if current == "LocalCPython" else "    Python 3"
        interpreter_menu.add_command(
            label=py_label, 
            command=lambda: select_interpreter("LocalCPython")
        )
        
        # Option ESP32
        # Note : Vérifiez si le nom exact est "ESP32" ou "Esp32Backend" dans vos paramètres
        esp_label = "✓ ESP32" if "ESP32" in current else "    ESP32"
        interpreter_menu.add_command(
            label=esp_label, 
            command=lambda: select_interpreter("ESP32")
        )

    # 'postcommand' est une astuce Tkinter : elle exécute 'refresh_menu' 
    # au moment précis où l'utilisateur clique sur le menu "Interprète"
    interpreter_menu.configure(postcommand=refresh_menu)

    # On affiche un message dans la console pour confirmer le chargement
    print("✅ Plugin 'Choix Interprète' chargé (Nouveau menu disponible)")

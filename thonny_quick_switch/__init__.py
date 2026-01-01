from thonny import get_workbench
import tkinter as tk

def set_interpreter(backend_id):
    """Change l'interpréteur et redémarre le backend"""
    wb = get_workbench()
    wb.set_option("run.backend_name", backend_id)
    try:
        wb.restart_backend(clean=True)
    except:
        pass

def load_plugin():
    wb = get_workbench()
    
    def create_custom_menu():
        try:
            # On récupère la barre de menu principale de la fenêtre (root)
            # cget("menu") renvoie le nom du widget menu (ex: ".!menu")
            menu_path = wb.cget("menu")
            if not menu_path:
                # Si le menu n'est pas encore prêt, on réessaie dans 200ms
                wb.after(200, create_custom_menu)
                return
                
            main_menubar = wb.nametowidget(menu_path)
            
            # Création du menu "Mode" (ou "Interpréteur")
            # Ce menu est un objet Tkinter pur, donc il ne sera pas grisé par Thonny
            mode_menu = tk.Menu(main_menubar, tearoff=0)
            
            def refresh_labels():
                """Met à jour les coches ✓ juste avant l'affichage du menu"""
                mode_menu.delete(0, "end")
                current = wb.get_option("run.backend_name")
                
                # Option Python 3
                py_prefix = "✓ " if current == "LocalCPython" else "    "
                mode_menu.add_command(
                    label=f"{py_prefix}Python 3", 
                    command=lambda: set_interpreter("LocalCPython")
                )
                
                # Option ESP32
                esp_prefix = "✓ " if current == "ESP32" else "    "
                mode_menu.add_command(
                    label=f"{esp_prefix}ESP32", 
                    command=lambda: set_interpreter("ESP32")
                )

            # postcommand : Tkinter exécute refresh_labels au moment du clic sur le menu
            mode_menu.configure(postcommand=refresh_labels)
            
            # Ajout du menu à la barre principale
            main_menubar.add_cascade(label="Interpréteur", menu=mode_menu)
            
        except Exception:
            # Sécurité pour éviter de faire crasher Thonny au démarrage
            pass

    # On lance la création avec un léger délai (500ms) pour garantir que l'UI est stable
    wb.after(500, create_custom_menu)

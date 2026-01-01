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
    
    # CORRECTION : On utilise directement l'attribut .menubar (et non une méthode)
    try:
        main_menubar = wb.menubar
    except AttributeError:
        # Fallback pour certaines versions de Thonny/Tkinter
        main_menubar = wb.nametowidget(wb.cget("menu"))
    
    # 1. Création d'un nouveau menu "Interpréteur" dans la barre du haut
    # Ce menu indépendant reste actif même quand un script tourne
    interpreter_menu = tk.Menu(main_menubar, tearoff=0)
    main_menubar.add_cascade(label="Interpréteur", menu=interpreter_menu)
    
    def refresh_menu():
        """Reconstruit le menu avec le symbole ✓ devant l'option active au clic"""
        # On vide le menu avant de le redessiner
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
        esp_label = "✓ ESP32" if current == "ESP32" else "    ESP32"
        interpreter_menu.add_command(
            label=esp_label, 
            command=lambda: select_interpreter("ESP32")
        )

    # 'postcommand' exécute 'refresh_menu' au moment précis où l'on clique sur le menu
    interpreter_menu.configure(postcommand=refresh_menu)

import tkinter as tk
from thonny import get_workbench

# Noms internes des backends Thonny
PYTHON_3 = "LocalCPython"
ESP32 = "ESP32"

def switch_to_backend(backend_name):
    """Bascule l'interpréteur et force l'application immédiate"""
    try:
        wb = get_workbench()
        if wb.get_option("run.backend_name") != backend_name:
            wb.set_option("run.backend_name", backend_name)
            
            # Déconnexion propre de l'ancien backend
            try:
                runner = wb.get_runner()
                if runner:
                    runner.destroy_backend()
            except Exception:
                pass
                
            wb.restart_backend()
            wb.update_title()
    except Exception:
        pass # Évite de faire planter Thonny en cas d'erreur ici

def create_radio_buttons():
    """Crée les boutons avec protection anti-crash"""
    try:
        wb = get_workbench()
        toolbar = wb.get_toolbar()
        
        if toolbar is None:
            return

        # Création du conteneur
        frame = tk.Frame(toolbar)
        
        # TENTATIVE 1 : Utiliser GRID (Standard Thonny)
        try:
            frame.grid(row=0, column=999, sticky="e", padx=10)
            toolbar.columnconfigure(999, weight=1)
        except tk.TclError:
            # TENTATIVE 2 : Fallback sur PACK si GRID échoue (Mode sans échec)
            frame.pack(side="right", fill="y", padx=10)

        # Gestion de la variable (Attachée au frame pour éviter le Garbage Collector)
        current_val = wb.get_option("run.backend_name")
        frame.var = tk.StringVar(value=current_val)
        
        def on_change():
            switch_to_backend(frame.var.get())

        # Création des boutons
        rb_py = tk.Radiobutton(
            frame, 
            text="🐍 Python 3", 
            variable=frame.var, 
            value=PYTHON_3, 
            command=on_change,
            indicatoron=False, 
            relief="raised",
            padx=10, pady=2
        )
        
        rb_esp = tk.Radiobutton(
            frame, 
            text="⚡ ESP32", 
            variable=frame.var, 
            value=ESP32, 
            command=on_change, 
            indicatoron=False, 
            relief="raised",
            padx=10, pady=2
        )
        
        rb_py.pack(side="left")
        rb_esp.pack(side="left")

        # Synchronisation UI
        def sync_ui(event=None):
            try:
                new_val = wb.get_option("run.backend_name")
                if new_val in [PYTHON_3, ESP32]:
                    frame.var.set(new_val)
            except:
                pass
                
        wb.bind("BackendRestarted", sync_ui, True)
        
    except Exception:
        # En cas d'erreur grave, on ne fait rien pour laisser Thonny démarrer
        print("Erreur chargement plugin Quick Switch")

def load_plugin():
    """Point d'entrée sécurisé"""
    try:
        # On attend que l'interface soit totalement chargée
        get_workbench().after_idle(create_radio_buttons)
    except Exception:
        pass

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
    except Exception as e:
        print(f"Erreur switch_to_backend: {e}")

def create_radio_buttons():
    """Crée les boutons avec protection anti-crash"""
    try:
        wb = get_workbench()
        toolbar = wb.get_toolbar()
        
        if toolbar is None:
            print("Toolbar non disponible")
            return
            
        # Vérifier si le plugin est déjà chargé
        for child in toolbar.winfo_children():
            if hasattr(child, '_quick_switch_plugin'):
                print("Plugin déjà chargé, on évite le doublon")
                return
        
        # Création du conteneur
        frame = tk.Frame(toolbar)
        frame._quick_switch_plugin = True  # Marqueur pour éviter les doublons
        
        # Gestion de la variable (Attachée au frame)
        current_val = wb.get_option("run.backend_name")
        frame.var = tk.StringVar(value=current_val)
        
        def on_change():
            try:
                switch_to_backend(frame.var.get())
            except Exception as e:
                print(f"Erreur on_change: {e}")
        
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
        
        rb_py.pack(side="left", padx=2)
        rb_esp.pack(side="left", padx=2)
        
        # Placement du frame dans la toolbar
        try:
            # Essayer PACK en premier (plus stable)
            frame.pack(side="right", fill="y", padx=10)
        except tk.TclError as e:
            print(f"Erreur placement frame: {e}")
            try:
                frame.grid(row=0, column=999, sticky="e", padx=10)
            except:
                pass
        
        # Synchronisation UI
        def sync_ui(event=None):
            try:
                new_val = wb.get_option("run.backend_name")
                if new_val in [PYTHON_3, ESP32]:
                    frame.var.set(new_val)
            except Exception as e:
                print(f"Erreur sync_ui: {e}")
        
        try:
            wb.bind("BackendRestarted", sync_ui, True)
        except Exception as e:
            print(f"Erreur bind event: {e}")
        
        print("Plugin Quick Switch chargé avec succès")
        
    except Exception as e:
        print(f"Erreur critique create_radio_buttons: {e}")
        import traceback
        traceback.print_exc()

def load_plugin():
    """Point d'entrée sécurisé"""
    try:
        wb = get_workbench()
        # Utiliser after avec un délai pour s'assurer que l'UI est prête
        wb.after(500, create_radio_buttons)
    except Exception as e:
        print(f"Erreur load_plugin: {e}")
        import traceback
        traceback.print_exc()

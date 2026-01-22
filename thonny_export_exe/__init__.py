from thonny import get_workbench
import subprocess
import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox, ttk

def run_conversion(filename, is_gui, progress_win, progress_bar):
    """Exécute la compilation dans un thread séparé"""
    work_dir = os.path.dirname(filename)
    script_name = os.path.basename(filename)
    
    # Préparation de la commande
    cmd = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--onefile"]
    cmd.append("--windowed" if is_gui else "--console")
    cmd.append(script_name)

    try:
        # Lancement du processus et capture de la sortie pour le log
        process = subprocess.Popen(
            cmd, 
            cwd=work_dir, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        # On attend la fin
        stdout, _ = process.communicate()

        # Fermeture de la barre de progression (via le thread principal)
        progress_win.after(0, progress_win.destroy)

        if process.returncode == 0:
            dist_folder = os.path.join(work_dir, "dist")
            messagebox.showinfo("Succès", f"Exportation terminée !\nFichier disponible dans :\n{dist_folder}")
            os.startfile(dist_folder)
        else:
            # En cas d'erreur, on crée un fichier log pour comprendre pourquoi
            log_file = os.path.join(work_dir, "export_error_log.txt")
            with open(log_file, "w", encoding="utf-8") as f:
                f.write(stdout)
            messagebox.showerror("Erreur Fatale", 
                f"La conversion a échoué (Code {process.returncode}).\n\n"
                f"Consultez le fichier log pour plus de détails :\n{log_file}")

    except Exception as e:
        progress_win.after(0, progress_win.destroy)
        messagebox.showerror("Erreur", f"Erreur système : {str(e)}")

def export_to_exe():
    wb = get_workbench()
    editor = wb.get_editor_notebook().get_current_editor()
    
    if not editor or not editor.get_filename():
        messagebox.showerror("Erreur", "Veuillez ouvrir et enregistrer un fichier .py avant l'export.")
        return
    
    filename = editor.get_filename()
    is_gui = messagebox.askyesno("Configuration", "Est-ce une application graphique (GUI) ?\n\n(Oui pour cacher la console noire)")

    # Création de la fenêtre de progression
    progress_win = tk.Toplevel(wb)
    progress_win.title("Exportation EXE")
    progress_win.geometry("300x120")
    progress_win.resizable(False, False)
    progress_win.attributes("-topmost", True)
    
    tk.Label(progress_win, text="Conversion en cours...", pady=10).pack()
    
    progress_bar = ttk.Progressbar(progress_win, mode='indeterminate', length=250)
    progress_bar.pack(pady=10)
    progress_bar.start(10)

    # Lancement de la conversion dans un thread pour ne pas bloquer l'UI
    threading.Thread(target=run_conversion, args=(filename, is_gui, progress_win, progress_bar), daemon=True).start()

def load_plugin():
    wb = get_workbench()
    # Ajout au menu 'Outils' (tools)
    wb.add_command(
        command_id="export_to_exe",
        menu_name="tools",
        command_label="Exporter en exécutable (.exe)",
        handler=export_to_exe,
        group=120
    )

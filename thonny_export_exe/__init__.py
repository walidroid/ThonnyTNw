from thonny import get_workbench
import subprocess
import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox, ttk
import importlib.util

def run_conversion(filename, is_gui, progress_win, progress_bar):
    """Exécute la compilation dans un thread séparé"""
    work_dir = os.path.dirname(filename)
    script_name = os.path.basename(filename)
    
    # Préparation de la commande
    # Préparation de la commande
    
    target_script = script_name
    temp_wrapper = None

    if not is_gui:
        # Créer un wrapper pour maintenir la console ouverte
        module_name = os.path.splitext(script_name)[0]
        temp_wrapper = os.path.join(work_dir, f"{module_name}_wrapper.py")
        try:
            with open(temp_wrapper, "w", encoding="utf-8") as f:
                f.write(f"import {module_name}\n")
                f.write("import sys\n")
                f.write("if __name__ == '__main__':\n")
                f.write("    input('\\nAppuyez sur Entrée pour fermer...')\n")
            target_script = f"{module_name}_wrapper.py"
        except Exception as e:
            print(f"Erreur création wrapper: {e}")
            target_script = script_name  # Fallback

    cmd = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--onefile"]
    cmd.append("--windowed" if is_gui else "--console")
    
    # Si on utilise un wrapper, on veut que l'exe final ait le nom original
    if temp_wrapper:
        cmd.extend(["--name", os.path.splitext(script_name)[0]])

    cmd.append(target_script)

    try:
        process = subprocess.Popen(
            cmd, 
            cwd=work_dir, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        stdout, _ = process.communicate()
        progress_win.after(0, progress_win.destroy)

        if process.returncode == 0:
            dist_folder = os.path.join(work_dir, "dist")
            messagebox.showinfo("Succès", f"Exportation terminée !\nFichier disponible dans :\n{dist_folder}")
            os.startfile(dist_folder)
        else:
            log_file = os.path.join(work_dir, "export_error_log.txt")
            with open(log_file, "w", encoding="utf-8") as f:
                f.write(stdout)
            messagebox.showerror("Erreur Fatale", 
                f"La conversion a échoué (Code {process.returncode}).\n\n"
                f"Consultez le fichier log pour plus de détails :\n{log_file}")
    except Exception as e:
        progress_win.after(0, progress_win.destroy)
        messagebox.showerror("Erreur", f"Erreur système : {str(e)}")
    finally:
        # Nettoyage du fichier temporaire wrapper
        if 'temp_wrapper' in locals() and temp_wrapper and os.path.exists(temp_wrapper):
            try:
                os.remove(temp_wrapper)
            except:
                pass

def check_pyinstaller():
    """Vérifie si PyInstaller est installé."""
    return importlib.util.find_spec("PyInstaller") is not None

def install_pyinstaller_thread(progress_win, on_complete):
    """Installe PyInstaller via pip dans un thread."""
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pyinstaller"],
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        success = True
    except Exception as e:
        print(f"Erreur installation PyInstaller: {e}")
        success = False

    progress_win.after(0, lambda: on_complete(success, progress_win))

def install_pyinstaller_gui(wb):
    """Affiche une fenêtre de progression pour l'installation de PyInstaller."""
    progress_win = tk.Toplevel(wb)
    progress_win.title("Installation des dépendances")
    progress_win.geometry("300x120")
    progress_win.resizable(False, False)
    progress_win.attributes("-topmost", True)

    tk.Label(progress_win, text="Installation de PyInstaller en cours...", pady=10).pack()

    progress_bar = ttk.Progressbar(progress_win, mode='indeterminate', length=250)
    progress_bar.pack(pady=10)
    progress_bar.start(10)

    def on_complete(success, win):
        win.destroy()
        if success:
             messagebox.showinfo("Succès", "PyInstaller a été installé avec succès.\nVous pouvez maintenant relancer l'export.")
             export_to_exe()
        else:
             messagebox.showerror("Erreur", "L'installation de PyInstaller a échoué.\nVérifiez votre connexion internet ou vos permissions.")

    threading.Thread(target=install_pyinstaller_thread, args=(progress_win, on_complete), daemon=True).start()

def export_to_exe():
    wb = get_workbench()

    if not check_pyinstaller():
        if messagebox.askyesno("PyInstaller manquant", "L'outil 'PyInstaller' est nécessaire pour créer des exécutables mais n'est pas installé.\n\nVoulez-vous l'installer maintenant ?"):
            install_pyinstaller_gui(wb)
        return

    editor = wb.get_editor_notebook().get_current_editor()
    
    if not editor or not editor.get_filename():
        messagebox.showerror("Erreur", "Veuillez ouvrir et enregistrer un fichier .py avant l'export.")
        return
    
    filename = editor.get_filename()
    is_gui = messagebox.askyesno("Configuration", "Est-ce une application graphique (GUI) ?\n\n(Oui pour cacher la console noire)")

    progress_win = tk.Toplevel(wb)
    progress_win.title("Exportation EXE")
    progress_win.geometry("300x120")
    progress_win.resizable(False, False)
    progress_win.attributes("-topmost", True)
    
    tk.Label(progress_win, text="Conversion en cours...", pady=10).pack()
    
    progress_bar = ttk.Progressbar(progress_win, mode='indeterminate', length=250)
    progress_bar.pack(pady=10)
    progress_bar.start(10)

    threading.Thread(target=run_conversion, args=(filename, is_gui, progress_win, progress_bar), daemon=True).start()

def load_plugin():
    wb = get_workbench()
    # CHANGEMENT : menu_name="file" au lieu de "tools"
    wb.add_command(
        command_id="export_to_exe",
        menu_name="file",
        command_label="Exporter en exécutable (.exe)...",
        handler=export_to_exe,
        group=1000
    )

from thonny import get_workbench
import subprocess
import os
import sys
from tkinter import messagebox

def export_to_exe():
    """Compile le script actuel en exécutable Windows (.exe)"""
    wb = get_workbench()
    editor = wb.get_editor_notebook().get_current_editor()
    
    # 1. Vérifications de base
    if not editor:
        messagebox.showerror("Erreur", "Aucun fichier n'est ouvert.")
        return
    
    filename = editor.get_filename()
    if not filename:
        messagebox.showerror("Erreur", "Veuillez d'abord sauvegarder votre fichier.")
        return
    
    if not filename.endswith(".py"):
        messagebox.showerror("Erreur", "Le fichier doit être un script Python (.py).")
        return

    # 2. Configuration de la commande PyInstaller
    # --onefile : Crée un seul fichier .exe
    # --noconfirm : Écrase le dossier dist s'il existe
    # --windowed : (Optionnel) Pour les GUI (pas de console noire). 
    # Pour les débutants, on laisse souvent la console visible pour voir les erreurs/input.
    
    # On demande à l'utilisateur s'il veut cacher la console (Mode GUI) ou non
    is_gui = messagebox.askyesno("Mode Export", "Voulez-vous cacher la console noire ?\n\nOui : Pour les interfaces graphiques (PyQt, Tkinter)\nNon : Pour les scripts console (print, input)")
    
    cmd = ["pyinstaller", "--noconfirm", "--onefile"]
    if is_gui:
        cmd.append("--windowed")
    else:
        cmd.append("--console")
        
    cmd.append(filename)
    
    # Dossier de sortie (là où est le script)
    work_dir = os.path.dirname(filename)
    
    # 3. Exécution
    try:
        # On affiche un message d'attente (rudimentaire)
        top = messagebox.showinfo("Export en cours", "La conversion est en cours...\nCela peut prendre une minute.\nThonny va geler temporairement.")
        
        # Lancement du processus
        # On utilise sys.executable -m PyInstaller pour être sûr d'utiliser le bon environnement
        subprocess.check_call([sys.executable, "-m"] + cmd, cwd=work_dir)
        
        # 4. Succès
        dist_folder = os.path.join(work_dir, "dist")
        messagebox.showinfo("Succès", f"L'exécutable a été créé dans le dossier :\n{dist_folder}")
        
        # Ouvrir le dossier automatiquement
        os.startfile(dist_folder)
        
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erreur Fatale", f"La conversion a échoué.\nCode erreur : {e.returncode}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur inattendue est survenue :\n{str(e)}")

def load_plugin():
    """Ajoute l'option dans le menu Fichier"""
    wb = get_workbench()
    
    wb.add_command(
        command_id="export_to_exe",
        menu_name="file",              # Ajout dans le menu 'Fichier'
        command_label="Exporter en .EXE...",
        handler=export_to_exe,
        caption="Exporter en EXE",
        group=1000                     # Tout en bas du menu
    )

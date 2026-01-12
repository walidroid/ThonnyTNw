from thonny import get_workbench

def activate_french_errors(event=None):
    """Force Friendly-traceback sur stdout pour contourner le filtrage de Thonny"""
    wb = get_workbench()
    runner = wb.get_runner()
    
    if runner:
        # On utilise stdout (sortie normale) au lieu de stderr (sortie d'erreur)
        # car Thonny traite parfois stderr différemment.
        script = (
            "try:\n"
            "    import friendly_traceback\n"
            "    import sys\n"
            "    \n"
            "    # 1. Configuration\n"
            "    friendly_traceback.set_lang('fr')\n"
            "    \n"
            "    # 2. On force la sortie sur le print normal (stdout)\n"
            "    friendly_traceback.set_stream(sys.stdout)\n"
            "    \n"
            "    # 3. Installation explicite\n"
            "    friendly_traceback.install(include='friendly_tb')\n"
            "    \n"
            "    # 4. Vérification visible (Optionnel, à retirer pour la prod)\n"
            "    # print('Friendly activé sur stdout')\n"
            "except Exception as e:\n"
            "    print(f'Erreur init Friendly: {e}')"
        )
        try:
            # silent=False temporairement pour voir si le script passe bien
            runner.execute_script(script, silent=True)
        except:
            pass

def load_plugin():
    wb = get_workbench()
    # On attend un peu plus longtemps (ToplevelResponse) ou on force au restart
    wb.bind("BackendRestarted", activate_french_errors, True)
    # 1. Supprimer "Proposer automatiquement des compléments pendant la saisie" (Option native de Thonny)
    wb.set_option("edit.propose_completions_while_typing", False)

    # 2. Supprimer l'ouverture automatique de l'Assistant (les deux options)
    # "Ouvrir l'assistant automatiquement quand le programme échoue avec une exception"
    wb.set_option("assistance.open_on_error", False)
    # "Ouvrir l'assistant automatiquement quand il a quelque chose à dire" (Warnings)
    wb.set_option("assistance.open_on_warnings", False)

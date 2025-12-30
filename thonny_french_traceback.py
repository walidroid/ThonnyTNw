from thonny import get_workbench

def activate_french_errors(event=None):
    """Injecte silencieusement friendly-traceback en français dans le Shell"""
    wb = get_workbench()
    runner = wb.get_runner()
    
    if runner:
        # Script Python à exécuter dans le backend (Shell)
        # On utilise un bloc try/except pour éviter les erreurs si le module est absent
        script = (
            "try:\n"
            "    import friendly_traceback\n"
            "    friendly_traceback.install()\n"
            "    friendly_traceback.set_lang('fr')\n"
            "except:\n"
            "    pass"
        )
        try:
            # L'argument silent=True empêche l'élève de voir le code passer dans la console
            runner.execute_script(script, silent=True)
        except:
            pass

def load_plugin():
    """Initialise le plugin au démarrage de Thonny"""
    wb = get_workbench()
    # On lie l'activation à l'événement 'BackendRestarted' 
    # Cela garantit que le français est réactivé même après un "Stop/Restart"
    wb.bind("BackendRestarted", activate_french_errors, True)

from thonny import get_workbench
from tkinter.messagebox import showinfo

def switch_interpreter():
    wb = get_workbench()
    current_backend = wb.get_option("run.backend_name")
    
    # Define the backend names (Internal names in Thonny)
    PYTHON_3 = "LocalCPython"
    ESP32 = "ESP32"  # Note: Requires thonny-esp plugin to be installed
    
    if current_backend == PYTHON_3:
        # Switch to ESP32
        wb.set_option("run.backend_name", ESP32)
        # You might want to auto-set the port if known, otherwise Thonny asks
        msg = "Switched to ESP32"
    else:
        # Switch back to Python 3
        wb.set_option("run.backend_name", PYTHON_3)
        msg = "Switched to Python 3 (Local)"

    # Force the backend to restart to apply changes
    try:
        wb.restart_backend(clean=True)
    except:
        pass # Handle cases where backend isn't running
        
    # Update the UI title or status
    wb.update_title()
    print(msg) # Shows in the shell

def load_plugin():
    # Add the button to the toolbar
    get_workbench().add_command(
        command_id="toggle_py3_esp32",
        menu_name="tools",
        command_label="Switch Py3/ESP32",
        handler=switch_interpreter,
        caption="ESP32 <-> Py3", # Text on the button
        include_in_toolbar=True,
        image=None # Or provide a path to an icon image
    )

from thonny import get_workbench
import builtins
import inspect
from .popup import show_popup


def init_plugin():
    wb = get_workbench()
    wb.bind("WorkbenchReady", on_ready)


def on_ready(event):
    wb = get_workbench()
    editor = wb.get_editor_notebook().get_current_editor()
    text = editor.get_text_widget()

    # Ctrl + Space
    text.bind("<Control-space>", on_autocomplete)


def on_autocomplete(event):
    editor = get_workbench().get_editor_notebook().get_current_editor()
    text = editor.get_text_widget()

    code = text.get("1.0", "insert")
    word = get_last_word(code)

    if not word:
        return

    fn = getattr(builtins, word, None)
    if fn:
        try:
            signature = word + str(inspect.signature(fn))
            show_popup(text, signature)
        except:
            pass


def get_last_word(code):
    word = ""
    for ch in reversed(code):
        if ch.isalnum() or ch == "_":
            word = ch + word
        else:
            break
    return word


from thonny import get_workbench

def init_plugin():
    wb = get_workbench()
    wb.bind("WorkbenchReady", on_ready, True)
    wb.bind("EditorTextCreated", on_editor_created, True)

def on_ready(event):
    wb = get_workbench()
    editor = wb.get_editor_notebook().get_current_editor()
    if editor:
        bind_events(editor.get_text_widget())

def on_editor_created(event):
    bind_events(event.text_widget)

def bind_events(text_widget):
    # Bind specific keys instead of generic <Key>
    pairs = {
        "(": ")",
        "[": "]",
        "'": "'",
        '"': '"'
    }
    
    for opening in pairs:
        text_widget.bind(opening, lambda e, o=opening, c=pairs[opening]: insert_pair(e, o, c), add="+")
    
    # Keep autocomplete on key release
    text_widget.bind("<KeyRelease>", on_key_release, add="+")

def insert_pair(event, opening, closing):
    """Insert matching pair and position cursor between them"""
    text_widget = event.widget
    
    # Check if there's a selection
    try:
        if text_widget.tag_ranges("sel"):
            # Wrap selection with pair
            start = text_widget.index("sel.first")
            end = text_widget.index("sel.last")
            selected_text = text_widget.get(start, end)
            
            text_widget.delete(start, end)
            text_widget.insert(start, opening + selected_text + closing)
            text_widget.mark_set("insert", f"{start}+{len(selected_text)+1}c")
            return "break"
    except:
        pass
    
    # No selection: insert pair and move cursor between them
    insert_pos = text_widget.index("insert")
    text_widget.insert(insert_pos, opening + closing)
    text_widget.mark_set("insert", f"{insert_pos}+1c")
    
    return "break"

def on_key_release(event):
    """Trigger Thonny's native autocomplete"""
    if event.char and (event.char.isalnum() or event.char in [".", "_"]):
        try:
            event.widget.event_generate("<<AutoComplete>>")
        except:
            pass

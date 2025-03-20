import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import sys


def display_changes(changes):
    root = tk.Tk()
    root.title("Code Change Viewer")
    root.geometry("800x500")

    # Frame for Filepath, Start, and End
    top_frame = tk.Frame(root)
    top_frame.pack(pady=10)

    filepath_label = tk.Label(top_frame, text=f"Filepath: {changes['filepath']}", font=("Arial", 12))
    filepath_label.pack(anchor="w")

    start_label = tk.Label(top_frame, text=f"Start Line: {changes['start']}", font=("Arial", 12))
    start_label.pack(anchor="w")

    end_label = tk.Label(top_frame, text=f"End Line: {changes['end']}", font=("Arial", 12))
    end_label.pack(anchor="w")

    # Frame for side-by-side text display
    text_frame = tk.Frame(root)
    text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Modification Textbox
    actual_label = tk.Label(text_frame, text="Actual Code", font=("Arial", 12, "bold"))
    actual_label.pack(side=tk.TOP, padx=10)

    actual_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=40, height=20)
    actual_text.insert(tk.END, changes['actual_code'])
    actual_text.configure(state='disabled')
    actual_text.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

    # Actual Code Textbox
    modification_label = tk.Label(text_frame, text="Modification", font=("Arial", 12, "bold"))
    modification_label.pack(side=tk.TOP, padx=10)

    modification_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=40, height=20)
    modification_text.insert(tk.END, changes['modification'])
    modification_text.configure(state='disabled')
    modification_text.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

    root.mainloop()


def main():
    if len(sys.argv) != 2:
        print("Usage: python tkinter_ui.py '<json_string>'")
        return

    try:
        data = json.loads(sys.argv[1])
        display_changes(data['changes'][0])
    except (json.JSONDecodeError, KeyError):
        print("Invalid JSON input.")


if __name__ == "__main__":
    main()

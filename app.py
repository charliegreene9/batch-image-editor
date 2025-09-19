import math
import tkinter as tk
from tkinter import filedialog, simpledialog

# TODO: read the features from the config
features = ["Rotate", "gogl", "fbr"]
funcs_dict = {
    "Rotate": [],
}
required_args = {
    "func1": ["arg1", "arg2"],
    "func2": ["arg3"],
    "func3": ["arg4"],
    # Add more functions as needed
}


# Function for opening the
# file explorer window
def file_explorer(batch_mode):
    if batch_mode is False:
        path = filedialog.askopenfilename(
            initialdir="/",
            title="Select a File",
            filetypes=(("Text files", "*.txt*"), ("all files", "*.*")),
        )
    else:
        path = tk.filedialog.askdirectory(
            initialdir="/",
            title="Select a Folder",
        )

    # # Change label contents
    # label_file_explorer.configure(text="File Opened: "+filename)
    return path


# Load up splash screen to cover load time
## loading bar?

# Form the window
window = tk.Tk()
window.title("Batch image processor")

selected_path = tk.StringVar(window, "")

# Intro and explanation
greeting = tk.Label(
    text="""Select what processes you want applied,
                    whether it is for a singular image or a folder,
                    and which file/folder to start"""
)
greeting.pack()

batch_mode = tk.BooleanVar(window, False)
# Radio button for singular file or batch
batch_mode_dict = {"singular": False, "multiple": True}
for mode in batch_mode_dict:
    tk.Radiobutton(
        window,
        text=mode,
        variable=batch_mode,
        value=batch_mode_dict[mode],
    ).pack(anchor="w", padx=10, pady=5)

# Include file explorer for directory or file
button_explore = tk.Button(
    window,
    text="Browse Files",
    command=lambda: selected_path.set(file_explorer(batch_mode.get())),
)
button_explore.pack()

# Create a container frame to hold grid-based widgets
grid_frame = tk.Frame(window)
grid_frame.pack()  # Use pack to place the grid_frame in the window
# Check box of functions to be applied
checkboxes = {}
function_dict = {}
for i, item in enumerate(funcs_dict.keys):
    checkboxes[item] = tk.BooleanVar()
    check = tk.Checkbutton(grid_frame, text=item, variable=checkboxes[item])
    check.grid(row=math.floor(i / 3), column=(i % 3), sticky="w")
    # Checking box initiates a new window to take in arguments

    # args are stored in a dict to be fed into function

    # label = tk.Label(grid_frame, text=item)
    # label.grid(row=math.floor(i/3), column=(i%3), sticky="w")
    # checkboxes.append({"var": var})

# Function to handle checkbox changes
# def on_check():
#     selected = []
#     for checkbox in checkboxes:
#         if checkbox["var"].get():
#             selected.append(checkbox["var"].get())
#     print("Selected items:", selected)


# Function to open a new window when a checkbox is selected
def on_checkbox_selected(*args, name):
    is_selected = checkboxes[name].get()

    if is_selected:
        # Open a new Toplevel window
        new_window = tk.Toplevel(window)
        new_window.title(f"Arguments for {name}")

        # Ask for arguments
        args = {}
        for arg_name in required_args[name]:
            arg = simpledialog.askstring(
                title="Input", prompt=f"Enter value for {arg_name}:"
            )
            if arg:
                args[arg_name] = arg
            else:
                # TODO: raise error for missing args
                new_window.destroy()
                return

        # Store the arguments in function_dict
        function_dict[name] = args
    else:
        # If the checkbox is unselected, remove the function from the dict
        if name in function_dict:
            del function_dict[name]


# Bind the checkbox to the function
for item in checkboxes:
    checkboxes[item].trace_add(
        "write",
        lambda *args, name=item: on_checkbox_selected(*args, name=name),
    )

output_format = tk.StringVar(window, "Overwrite")
# Radio button option to save with a new output
output_options = ["Prefix", "Suffix", "Overwrite"]
for option in output_options:
    tk.Radiobutton(
        window,
        text=option,
        variable=output_format,
        value=option,
    ).pack(anchor="w", padx=10, pady=5)
# Create the entry box and hide it initially
entry = tk.Entry(window, width=30)
entry.pack()
entry.pack_forget()  # Hide it at first


# Function to update the entry box visibility based on the selection
def update_entry(*args):
    selected = output_format.get()
    if selected in ["Prefix", "Suffix"]:
        entry.pack()
    else:
        entry.pack_forget()


# Bind the function to the StringVar
output_format.trace_add("write", update_entry)


def run_all():
    for func_name, args in function_dict.items():
        # Call the function using the stored arguments
        func = globals()[func_name]
        # Check functions are in the global scope, safety
        func(**args)
    # Loop over the checkboxes

    # If box is checked run the function


# Start button
start_button = tk.Button(window, text="Start", command=run_all)
start_button.pack()
# Pop up for loading/progress bar
## Stop button

window.mainloop()

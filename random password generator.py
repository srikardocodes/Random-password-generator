import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import pyperclip

CHARACTER_SETS = {
    "Uppercase": string.ascii_uppercase,
    "Lowercase": string.ascii_lowercase,
    "Numbers": string.digits,
    "Symbols": string.punctuation,
}

AMBIGUOUS_CHARACTERS = "0Ool1I"



def get_character_sets():
    

    selected = []

    if uppercase_var.get():
        selected.append(CHARACTER_SETS["Uppercase"])

    if lowercase_var.get():
        selected.append(CHARACTER_SETS["Lowercase"])

    if numbers_var.get():
        selected.append(CHARACTER_SETS["Numbers"])

    if symbols_var.get():
        selected.append(CHARACTER_SETS["Symbols"])

    return selected


def remove_ambiguous(characters):
    

    return "".join(
        character
        for character in characters
        if character not in AMBIGUOUS_CHARACTERS
    )


def generate_password(length, selected_sets):
   

    if exclude_ambiguous_var.get():
        selected_sets = [
            remove_ambiguous(character_set)
            for character_set in selected_sets
        ]

   
    if any(not character_set for character_set in selected_sets):
        raise ValueError(
            "A selected character type contains only excluded characters."
        )

    all_characters = "".join(selected_sets)

    password = []

    for character_set in selected_sets:
        password.append(secrets.choice(character_set))

    for _ in range(length - len(password)):
        password.append(secrets.choice(all_characters))

    for i in range(len(password) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password[i], password[j] = password[j], password[i]

    return "".join(password)


def calculate_strength(password, selected_count):
   
    length = len(password)

    score = 0

   
    if length >= 20:
        score += 3
    elif length >= 14:
        score += 2
    elif length >= 8:
        score += 1

   
    score += selected_count

    if score <= 3:
        return "Weak", "#e74c3c"

    if score <= 5:
        return "Medium", "#f39c12"

    return "Strong", "#27ae60"


def generate():
   

    try:
        length = int(length_var.get())
    except ValueError:
        messagebox.showerror(
            "Invalid Length",
            "Please enter a valid password length."
        )
        return

    if length < 8:
        messagebox.showerror(
            "Invalid Length",
            "Password length must be at least 8 characters."
        )
        return

    selected_sets = get_character_sets()

    if len(selected_sets) < 2:
        messagebox.showerror(
            "Character Types",
            "Please select at least 2 character types."
        )
        return

    if length < len(selected_sets):
        messagebox.showerror(
            "Length Too Short",
            "Password length must be at least the number "
            "of selected character types."
        )
        return

    try:
        password = generate_password(length, selected_sets)
    except ValueError as error:
        messagebox.showerror("Generation Error", str(error))
        return

    password_var.set(password)

   
    strength, color = calculate_strength(
        password,
        len(selected_sets)
    )

    strength_label.config(
        text=f"Strength: {strength}",
        foreground=color
    )

    
    strength_values = {
        "Weak": 30,
        "Medium": 65,
        "Strong": 100
    }

    strength_bar["value"] = strength_values[strength]
    strength_bar.configure(style=f"{strength}.Horizontal.TProgressbar")

   
    try:
        pyperclip.copy(password)
        clipboard_label.config(
            text=" Password copied to clipboard",
            foreground="#27ae60"
        )
    except pyperclip.PyperclipException:
        clipboard_label.config(
            text="Could not access clipboard",
            foreground="#e74c3c"
        )

   
    history.insert(0, password)

    
    del history[5:]

    update_history()


def copy_password():
    

    password = password_var.get()

    if not password:
        messagebox.showwarning(
            "No Password",
            "Generate a password first."
        )
        return

    try:
        pyperclip.copy(password)
        clipboard_label.config(
            text=" Password copied to clipboard",
            foreground="#27ae60"
        )
    except pyperclip.PyperclipException:
        messagebox.showerror(
            "Clipboard Error",
            "Could not access the system clipboard."
        )


def update_history():
    

    history_list.delete(0, tk.END)

    for password in history:
        history_list.insert(tk.END, password)


root = tk.Tk()
root.title("Secure Password Generator")
root.geometry("650x700")
root.resizable(False, False)

root.configure(bg="#1e1e2e")




style = ttk.Style()

try:
    style.theme_use("clam")
except tk.TclError:
    pass

style.configure(
    "TFrame",
    background="#1e1e2e"
)

style.configure(
    "TLabel",
    background="#1e1e2e",
    foreground="#ffffff",
    font=("Arial", 11)
)

style.configure(
    "Title.TLabel",
    background="#1e1e2e",
    foreground="#ffffff",
    font=("Arial", 22, "bold")
)

style.configure(
    "TCheckbutton",
    background="#1e1e2e",
    foreground="#ffffff",
    font=("Arial", 10)
)

style.configure(
    "TButton",
    font=("Arial", 10, "bold"),
    padding=8
)

style.configure(
    "Weak.Horizontal.TProgressbar",
    troughcolor="#333344",
    background="#e74c3c"
)

style.configure(
    "Medium.Horizontal.TProgressbar",
    troughcolor="#333344",
    background="#f39c12"
)

style.configure(
    "Strong.Horizontal.TProgressbar",
    troughcolor="#333344",
    background="#27ae60"
)



length_var = tk.StringVar(value="16")
password_var = tk.StringVar()

uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

exclude_ambiguous_var = tk.BooleanVar(value=False)

history = []



main_frame = ttk.Frame(root, padding=25)
main_frame.pack(fill="both", expand=True)

title = ttk.Label(
    main_frame,
    text="🔐 Secure Password Generator",
    style="Title.TLabel"
)
title.pack(pady=(0, 25))



ttk.Label(
    main_frame,
    text="Generated Password"
).pack(anchor="w")

password_entry = tk.Entry(
    main_frame,
    textvariable=password_var,
    font=("Consolas", 18),
    justify="center",
    bg="#313244",
    fg="#ffffff",
    insertbackground="white",
    relief="flat"
)
password_entry.pack(
    fill="x",
    pady=(5, 15),
    ipady=10
)



ttk.Label(
    main_frame,
    text="Password Length"
).pack(anchor="w")

length_spinbox = tk.Spinbox(
    main_frame,
    from_=8,
    to=128,
    textvariable=length_var,
    font=("Arial", 12),
    width=10,
    justify="center",
    bg="#313244",
    fg="#ffffff",
    buttonbackground="#45475a"
)
length_spinbox.pack(
    anchor="w",
    pady=(5, 15)
)



ttk.Label(
    main_frame,
    text="Character Types"
).pack(anchor="w")

types_frame = ttk.Frame(main_frame)
types_frame.pack(fill="x", pady=(5, 15))

ttk.Checkbutton(
    types_frame,
    text="Uppercase",
    variable=uppercase_var
).grid(row=0, column=0, padx=(0, 20), pady=5, sticky="w")

ttk.Checkbutton(
    types_frame,
    text="Lowercase",
    variable=lowercase_var
).grid(row=0, column=1, padx=(0, 20), pady=5, sticky="w")

ttk.Checkbutton(
    types_frame,
    text="Numbers",
    variable=numbers_var
).grid(row=1, column=0, padx=(0, 20), pady=5, sticky="w")

ttk.Checkbutton(
    types_frame,
    text="Symbols",
    variable=symbols_var
).grid(row=1, column=1, padx=(0, 20), pady=5, sticky="w")


ttk.Checkbutton(
    main_frame,
    text="Exclude ambiguous characters (0, O, o, l, 1, I)",
    variable=exclude_ambiguous_var
).pack(anchor="w", pady=(0, 20))

generate_button = ttk.Button(
    main_frame,
    text="Generate Password",
    command=generate
)
generate_button.pack(fill="x", pady=5)


copy_button = ttk.Button(
    main_frame,
    text="Copy to Clipboard",
    command=copy_password
)
copy_button.pack(fill="x", pady=5)


clipboard_label = ttk.Label(
    main_frame,
    text=""
)
clipboard_label.pack(pady=5)


strength_label = ttk.Label(
    main_frame,
    text="Strength: —",
    font=("Arial", 12, "bold")
)
strength_label.pack(pady=(10, 5))

strength_bar = ttk.Progressbar(
    main_frame,
    length=500,
    maximum=100,
    mode="determinate"
)
strength_bar.pack(pady=(0, 20))



ttk.Label(
    main_frame,
    text="Generation History — Last 5"
).pack(anchor="w")

history_list = tk.Listbox(
    main_frame,
    height=5,
    font=("Consolas", 11),
    bg="#313244",
    fg="#ffffff",
    selectbackground="#585b70",
    relief="flat"
)
history_list.pack(
    fill="x",
    pady=(5, 0)
)


root.mainloop()

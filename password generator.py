import tkinter as tk
from tkinter import messagebox,ttk
import random
import string
import pyperclip

# Password Generator Function
def generate_password():
    length=int(length_var.get())
    include_lowercase=lowercase_var.get()
    include_uppercase=uppercase_var.get()
    include_numbers=numbers_var.get()
    include_symbols=symbols_var.get()

    if not (include_lowercase or include_uppercase or include_numbers or include_symbols):
        messagebox.showerror("Error", "Select at least one character type!")
        return

    # Build the character pool
    char_pool = ""
    if include_lowercase:
        char_pool+=string.ascii_lowercase
    if include_uppercase:
        char_pool+=string.ascii_uppercase
    if include_numbers:
        char_pool+=string.digits
    if include_symbols:
        char_pool+=string.punctuation

    # Generate the password
    password = "".join(random.choices(char_pool, k=length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

# Copy to Clipboard
def copy_to_clipboard():
    password = password_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showerror("Error", "No password to copy!")

# GUI Setup
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("400x300")
root.resizable(False, False)

# Styles
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ccc")

# Widgets
ttk.Label(root, text="Password Length:").grid(column=0, row=0, padx=10, pady=10, sticky="w")
length_var = tk.StringVar(value="12")
length_spinbox = ttk.Spinbox(root, from_=8, to=64, textvariable=length_var, width=5)
length_spinbox.grid(column=1, row=0, padx=10, pady=10, sticky="w")

# Checkbuttons for character types
lowercase_var = tk.BooleanVar(value=True)
uppercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=False)

ttk.Checkbutton(root, text="Include Lowercase", variable=lowercase_var).grid(column=0, row=1, padx=10, pady=5,sticky="w")
ttk.Checkbutton(root, text="Include Uppercase", variable=uppercase_var).grid(column=0, row=2, padx=10, pady=5,sticky="w")
ttk.Checkbutton(root, text="Include Numbers", variable=numbers_var).grid(column=0, row=3, padx=10, pady=5,sticky="w")
ttk.Checkbutton(root, text="Include Symbols", variable=symbols_var).grid(column=0, row=4, padx=10, pady=5,sticky="w")

# Password Entry
password_entry = ttk.Entry(root, width=60)
password_entry.grid(column=0, row=5, columnspan=2, padx=15, pady=10)

# Buttons
ttk.Button(root, text="Generate Password", command=generate_password).grid(column=0, row=6, columnspan=2, pady=5)
ttk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard).grid(column=0, row=7, columnspan=2, pady=5)

# Start the GUI event loop
root.mainloop()
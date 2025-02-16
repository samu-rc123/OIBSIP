import tkinter as tk
from tkinter import messagebox,ttk
import sqlite3
import matplotlib.pyplot as plt

# Database setup
conn = sqlite3.connect("bmi_data.db")
cursor=conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS bmi_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT,
        weight REAL,
        height REAL,
        bmi REAL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# Function to calculate BMI
def calculate_bmi(weight, height):
    bmi=weight/((height/100)**2)
    return round(bmi, 2)

# Function to determine BMI category
def get_bmi_category(bmi):
    if bmi<18.5:
        return "Underweight"
    elif 18.5<=bmi<24.9:
        return "Normal weight"
    elif 25<=bmi<29.9:
        return "Overweight"
    elif 30<=bmi<34.9:
        return "Obesity class 1"
    elif 25<=bmi<39.9:
        return "Obesity class 2"
    else:
        return "Obesity class 3"

# Function to save BMI record to the database
def save_record(user_name, weight, height, bmi):
    cursor.execute("INSERT INTO bmi_records (user_name, weight, height, bmi) VALUES (?, ?, ?, ?)", (user_name, weight, height, bmi))
    conn.commit()

# Function to display historical data
def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("BMI History")
    tree = ttk.Treeview(history_window, columns=("ID", "Name", "Weight", "Height", "BMI", "Date"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Weight", text="Weight (kg)")
    tree.heading("Height", text="Height (m)")
    tree.heading("BMI", text="BMI")
    tree.heading("Date", text="Date")
    tree.pack(fill=tk.BOTH, expand=True)

    cursor.execute("SELECT * FROM bmi_records")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

# Function to show BMI trend analysis
def show_trend():
    cursor.execute("SELECT date, bmi FROM bmi_records")
    data = cursor.fetchall()
    if not data:
        messagebox.showinfo("No Data", "No historical data available for trend analysis.")
        return
    dates = [x[0] for x in data]
    bmis = [x[1] for x in data]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, bmis, marker='o', linestyle='-', color='b')
    plt.title("BMI Trend Analysis")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main GUI setup
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("400x400")

# User input fields
tk.Label(root, text="Name:").pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

tk.Label(root, text="Weight (kg):").pack(pady=5)
weight_entry = tk.Entry(root)
weight_entry.pack(pady=5)

tk.Label(root, text="Height (cm):").pack(pady=5)
height_entry = tk.Entry(root)
height_entry.pack(pady=5)

# Function to handle BMI calculation and display the result
def on_calculate():
    try:
        user_name = name_entry.get()
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        if user_name and weight > 0 and height > 0:
            bmi = calculate_bmi(weight, height)
            category = get_bmi_category(bmi)
            save_record(user_name, weight, height, bmi)
            messagebox.showinfo("BMI Result", f"Name: {user_name}\nBMI: {bmi} ({category})")
        else:
            messagebox.showerror("Invalid Input", "Please enter valid values.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter numeric values for weight and height.")

# Buttons
tk.Button(root, text="Calculate BMI", command=on_calculate).pack(pady=10)
tk.Button(root, text="View History", command=show_history).pack(pady=10)
tk.Button(root, text="Show Trend Analysis", command=show_trend).pack(pady=10)

root.mainloop()

# Close the database connection when done
conn.close()

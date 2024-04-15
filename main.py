import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import requests

HTTP_NO_CONTENT = 204
MESSAGE_RESOURCE_URL = "http://192.168.1.207:8080/api/message/"


def set_message():
    message = {
        "row_one": row_one_string.get(),
        "row_two": row_two_string.get()
    }

    try:
        r = requests.post(MESSAGE_RESOURCE_URL, data=message)
    except requests.exceptions.ConnectionError:
        if messagebox.showerror("Error",
                                message="Couldn't connect to the device.",
                                type="retrycancel") == "retry":
            set_message()
        return

    if r.status_code == HTTP_NO_CONTENT:
        messagebox.showinfo("Success", message="Successfully set.")
    else:
        messagebox.showerror("Error", message="Command failed.")


def clear_message():
    try:
        r = requests.delete(MESSAGE_RESOURCE_URL)
    except requests.exceptions.ConnectionError:
        if messagebox.showerror("Error",
                                message="Couldn't connect to the device.",
                                type="retrycancel") == "retry":
            set_message()
        return

    if r.status_code == HTTP_NO_CONTENT:
        row_one_string.set("")
        row_two_string.set("")
        messagebox.showinfo("Success", message="Successfully cleared.")
    else:
        messagebox.showerror("Error", message="Command failed.")


window = tk.Tk()
window.title("LCD Remote Client")
window.eval("tk::PlaceWindow . center")
window.resizable(False, False)

menu_frame = ttk.Frame(window)
menu_frame.grid(padx=20, pady=20)

row_one_string = tk.StringVar()
row_two_string = tk.StringVar()

row_one_entry = ttk.Entry(menu_frame, textvariable=row_one_string)
row_one_entry.grid(column=0, row=0, columnspan=2, pady=5, sticky="ew")
row_two_entry = ttk.Entry(menu_frame, textvariable=row_two_string, width=27)
row_two_entry.grid(column=0, row=1, columnspan=2, sticky="ew")

clear_button = ttk.Button(menu_frame, text="Clear", command=clear_message)
set_button = ttk.Button(menu_frame, text="Set", command=set_message)
clear_button.grid(column=0, row=2, pady=10, sticky="ew")
set_button.grid(column=1, row=2, sticky="ew")

window.mainloop()

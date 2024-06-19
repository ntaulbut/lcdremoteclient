import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import requests

HTTP_NO_CONTENT = 204
HTTP_OK = 200
MESSAGE_RESOURCE_URL = "http://192.168.1.207:8080/api/message/"


def set_message() -> None:
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
        row_one_remote_string.set(row_one_string.get())
        row_two_remote_string.set(row_two_string.get())
    else:
        messagebox.showerror("Error", message="Command failed.")


def clear_message() -> None:
    try:
        r = requests.delete(MESSAGE_RESOURCE_URL)
    except requests.exceptions.ConnectionError:
        if messagebox.showerror("Error",
                                message="Couldn't connect to the device.",
                                type="retrycancel") == "retry":
            set_message()
        return

    if r.status_code == HTTP_NO_CONTENT:
        row_one_remote_string.set("")
        row_two_remote_string.set("")
    else:
        messagebox.showerror("Error", message="Command failed.")


def get_message() -> None:
    try:
        r = requests.get(MESSAGE_RESOURCE_URL)
    except requests.exceptions.ConnectionError:
        if messagebox.showerror("Error",
                                message="Couldn't connect to the device.",
                                type="retrycancel") == "retry":
            set_message()
        return

    if r.status_code == HTTP_OK:
        message = r.text.split("\n")
        if len(message) == 2:
            row_one_remote_string.set(message[0])
            row_two_remote_string.set(message[1])
        else:
            row_one_remote_string.set("")
            row_two_remote_string.set("")
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

row_one_remote_string = tk.StringVar()
row_two_remote_string = tk.StringVar()

row_one_entry = ttk.Entry(menu_frame, textvariable=row_one_string, width=16)
row_one_entry.grid(column=0, row=0, pady=0)
row_two_entry = ttk.Entry(menu_frame, textvariable=row_two_string, width=16)
row_two_entry.grid(column=0, row=1, pady=0)

row_one_remote_label = ttk.Label(menu_frame, textvariable=row_one_remote_string, width=16, borderwidth=2, relief="sunken")
row_one_remote_label.grid(column=2, row=0, sticky="ew")
row_two_remote_label = ttk.Label(menu_frame, textvariable=row_two_remote_string, width=16, borderwidth=2, relief="sunken")
row_two_remote_label.grid(column=2, row=1, sticky="ew")

set_button = ttk.Button(menu_frame, text="Set", command=set_message)
clear_button = ttk.Button(menu_frame, text="Clear", command=clear_message)
get_button = ttk.Button(menu_frame, text="Get", command=get_message)
set_button.grid(column=0, row=2, sticky="ew")
clear_button.grid(column=0, row=3, sticky="ew")
get_button.grid(column=2, row=2, sticky="ew")

get_message()
window.mainloop()

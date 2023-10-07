from tkinter import *
from tkinter import ttk
import sqlite3
from sqlite3 import Error
from tkinter import Menu
import json
import os
from tkinter import scrolledtext
import re
import mymodules
import spells
from tkinter import messagebox
import threading
# Moved to 'InventoryWindow()'
def inventory_window(name, inventory_window_open, inventory_array, characters_array, root):
    
    if inventory_window_open:
        return
    inventory_window_open = True

    def fill_table_with_inventory_array(inventory_array):
        inv_tree.delete(*inv_tree.get_children())
        counter = 0
        for item in inventory_array:
            inv_tree.insert(parent='', index='end', iid = counter, text="", values=(item[0], item[2], item[1], item[3], item[4]))
            counter += 1

    def query_char_inventory(name, item_name, inventory_array, characters_array):
        if item_name is None:
            item_name = ''
        inventory_array = []
        conn = mymodules.create_connection('./stables.db')
        c = conn.cursor()
        selected_char.set(name)
        print(name)
        if name == 'All':
            c.execute("""SELECT * FROM inventory WHERE itemName LIKE ?""", ('%' + item_name + '%',))
        else:
            c.execute("""SELECT * FROM inventory WHERE charName = ? AND itemName LIKE ?""", (name, '%' + item_name + '%'))
        
        char_inventory = c.fetchall()
        
        for item in char_inventory:
            inventory_array.append(item)
        conn.commit()
        conn.close()
        print(len(inventory_array))
        print(len(inv_tree.get_children()))
        # If char doesnt have inventory, return False
        if len(inventory_array) == 0 and len(inv_tree.get_children()) == 0:
            print('TEST')
            if inv_window is not None and inv_window.winfo_exists():
                inv_window.destroy()
                return False
            
        fill_table_with_inventory_array(inventory_array)
        
    def selected_inventory_changed(*, inventory_array, characters_array):
        inventory_array = []
        name = selected_char.get()
        query_char_inventory(name, '', inventory_array, characters_array)
    
    char_list = fetch_inventory_char_names()
    inv_window = Toplevel(root)
    inv_window.title("Inventory Reader")
    inv_window.grid_rowconfigure(1, weight=1)
    inv_window.grid_columnconfigure(0, weight=1)

    inv_tree = ttk.Treeview(inv_window)
    inv_tree['columns'] = ('Char Name', 'Item Name', 'Location', 'Item ID', 'Count')
    inv_tree.grid(row=1, column=0, columnspan=8, padx=10, pady=10, sticky="nsew")
    inv_search = Entry(inv_window, width=100, bd=5, font = ('Arial Bold', 15))
    inv_search.grid(row=0, column=0, columnspan=7, padx=5, pady=5)
    inv_search.bind("<Return>", lambda event: query_char_inventory(selected_char.get(), inv_search.get(), inventory_array, characters_array))
    inv_tree_scrollbar = Scrollbar(inv_window, orient="vertical", command=inv_tree.yview)
    inv_tree_scrollbar.grid(row=1, column=1, sticky="ns")
    inv_tree.configure(yscrollcommand=inv_tree_scrollbar.set)
    # Cols
    inv_tree.column('#0', width=0, stretch=NO)
    inv_tree.column('Char Name')
    inv_tree.column('Item Name')
    inv_tree.column('Location')
    inv_tree.column('Item ID')
    inv_tree.column('Count')
    # Headings
    inv_tree.heading("#0", text='', )
    inv_tree.heading("Char Name", text='Char Name', command=lambda: mymodules.sort_column("Char Name", False, inv_tree))
    inv_tree.heading("Item Name", text='Item Name', command=lambda: mymodules.sort_column("Item Name", False, inv_tree))
    inv_tree.heading("Location", text='Location', command=lambda: mymodules.sort_column("Location", False, inv_tree))
    inv_tree.heading("Item ID", text='Item ID', command=lambda: mymodules.sort_column("Item ID", False, inv_tree))
    inv_tree.heading("Count", text='Count', command=lambda: mymodules.sort_column("Count", False, inv_tree))
    # Select Char Frame
    select_char_frame = LabelFrame(inv_window, text="Select Character")
    select_char_frame.grid(row=0, column=0, padx=5, pady=5, sticky="W")
    select_char_label = Label(select_char_frame, text="SELECT CHAR:", anchor="w")
    select_char_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    selected_char = StringVar()
    select_char_pulldown = ttk.Combobox(select_char_frame, textvariable=selected_char, values=char_list, state="readonly")
    select_char_pulldown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    selected_char.set('ALL')
    
    # This boolean tells us if the chose char's inventory is length of 0. If so, returns false and closes the window.
    if query_char_inventory(name, '', inventory_array, characters_array) == False:
        return messagebox.showinfo("No Inventory Found", "No inventory was found for the selected character.")
            
    def close_inventory_window(inventory_window_open, inventory_array):
        inventory_window_open = False
        inventory_array = []
        inv_window.destroy()
    
    
    inv_window.protocol("WM_DELETE_WINDOW", lambda event=None: close_inventory_window(inventory_window_open, inventory_array))
    select_char_pulldown.bind("<<ComboboxSelected>>", lambda event, *, tree=inv_tree, inventory_array=inventory_array, characters_array=characters_array: selected_inventory_changed(inventory_array=inventory_array, characters_array=characters_array))
# Moved to 'InventoryWindow()'
def fetch_inventory_char_names():
    res = []
    conn = mymodules.create_connection('./stables.db')
    c = conn.cursor()
    c.execute("""SELECT DISTINCT charName FROM inventory""")
    char_names = c.fetchall()
    conn.commit()
    conn.close()
    for name in char_names:
        res.append(name[0])
    res.append('All')
    res.sort()
    return res
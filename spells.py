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
import inventory

from tkinter import messagebox

def test_fetch_spell(char_name, spell_name):
        conn = mymodules.create_connection('./stables.db')
        c = conn.cursor()
        c.execute("""SELECT DISTINCT charName FROM inventory""")
        results = c.fetchall()
        conn.commit()
        conn.close()
        print(results)
# Moved to SpellsMethods
def delete_spells_db(eq_dir, name):
    conn = mymodules.create_connection('./stables.db')
    c = conn.cursor()
    c.execute("""DELETE FROM classSpells""")
    c.execute("""DELETE FROM spellbooks""")
    c.execute("""DELETE FROM missingSpells""")
    conn.commit()
    conn.close()
    print('Entire Spells DB Deleted.')
# Moved to SpellsMethods
def query_missing_spells():
    conn = mymodules.create_connection('./stables.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM missingSpells WHERE charName = 'Grixus'""")
    res = c.fetchall()
    print('res')
    print(res)
# Moved to SpellsMethods
def create_class_spells_db():
        class_spells = []
        for filename in os.listdir('./classSpells'):
                char_class = filename[:-4]
                with open(f'./classSpells/{filename}', 'r') as file:
                    for line in file:
                        line = line.strip().replace('\n', '').replace('\t', '').split(',')
                        line.insert(0, char_class)
                        class_spells.append(line)                
        # [charClass, spellLevel, spellName]
        conn = mymodules.create_connection('./stables.db')
        c = conn.cursor()
        try:
            c.execute("""DELETE FROM classSpells""")
            print('db.classSpells deleted, preparing to re-write...')
        except Exception as e:
            print(e)
        c.executemany('INSERT INTO classSpells VALUES (?, ?, ?)', (class_spells))
        conn.commit()
        conn.close()
        print('db.classSpells written')
# Moved to SpellsMethods
def create_character_spellbooks(array, name='All', eq_dir='test'):
        char_names = []
        spellbooks_list = []
        spellbooks_object = {}
        
        conn = mymodules.create_connection('./stables.db')
        c = conn.cursor()
        
        if name == 'All':
            char_names = [char['Name'] for char in array]
            c.execute("""DELETE FROM spellbooks""")
            
        else:
            char_names = [name]
            c.execute("""DELETE FROM spellbooks WHERE charName = ?""", (name,))
        
        for char_name in char_names:
            try:
                with open(f'{eq_dir}/{char_name}spells', 'r') as spellbook: 
                    for line in spellbook:
                        line = line.replace('\n', '').split('\t')
                        line.insert(0, char_name)
                        if (len(line) == 3):
                            spellbooks_list.append(line)
                    
            except Exception as e:
                print(e)
                continue 
        try:
            c.executemany("""INSERT INTO spellbooks VALUES (?, ?, ?)""", (spellbooks_list))
        except Exception as e:
            print(e)
          
        # Remove first element (char_name) from list and create 'spellbooks_object'
        for spell in spellbooks_list:
            char_name = spell[0]
            spell.pop(0)
            spell[0] = int(spell[0])
            spell = tuple(spell)
            if char_name in spellbooks_object:
                spellbooks_object[char_name].append(spell)
            else:
                spellbooks_object[char_name] = [spell]
        
        conn.commit()
        conn.close()
        print('create_character_spellbooks() done')
        return spellbooks_object
# Moved to SpellsMethods       
def get_class_spells(char_class):
        # need to return an object that contains key: char_class, val: 2d list
        conn = mymodules.create_connection('./stables.db')
        c = conn.cursor()
        results = []
        class_spells = {}
        
        if char_class == 'All':
            c.execute("""SELECT * FROM classSpells""")
            results = c.fetchall()
        else:
            c.execute("""SELECT * FROM classSpells WHERE charClass = ?""", (char_class,))
            results = c.fetchall()
            
        for spell in results:
            class_name = spell[0]
            if class_name in class_spells:
                spell = spell[1:]
                class_spells[class_name].append(spell) 
            else:
                class_spells[class_name] = [spell[1:]]
        conn.commit()
        conn.close()
        return class_spells
# For debugging
# Moved to SpellsMethods
def get_all_spell_tables():
    conn = mymodules.create_connection('./stables.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM classSpells""")
    res = c.fetchall()
    res2 = []
    print('CLASS SPELLS')
    for spell in res:
        if spell[0] not in res2:
            res2.append(spell[0])
    print(res2)
    
    c.execute("""SELECT * FROM spellbooks""")
    res = c.fetchall()
    res2 = []
    print('CLASS SPELLBOOKS')
    for spell in res:
        if spell[0] not in res2:
            res2.append(spell[0])
    print(res2)
    c.execute("""SELECT * FROM missingSpells""")
    res = c.fetchall()
    res2 = []
    print('MISSING SPELLS')
    for spell in res:
        if spell[0] not in res2:
            res2.append(spell[0])
    print(res2)
    conn.commit()
    conn.close()
# Moved to SpellsMethods
def delete_all_spell_tables():
    conn = mymodules.create_connection('./stables.db')
    c = conn.cursor()
    c.execute("""DELETE FROM classSpells""")
    print('deleted db.classSpells')
    c.execute("""DELETE FROM spellbooks""")
    print('deleted db.spellbooks')
    c.execute("""DELETE FROM missingSpells""")
    print('deleted db.missingSpells')
    conn.commit()
    conn.close()
# Moved to SpellsMethods
def create_missing_spells_db(characters_array, eq_dir='test', name='All'):
        
        # create_all_spells_dbs(characters_array, name, eq_dir)
        characters_classes = []
        class_spells = {}
        missing_spells = []
        
        conn = mymodules.create_connection('./stables.db')
        c = conn.cursor()

        if name == 'All':
            characters_classes = {char['Name']: char['Class'] for char in characters_array}
            class_spells = get_class_spells('All')
            c.execute("""DELETE FROM missingSpells""")
         
        else:
            characters_classes = {char['Name']: char['Class'] for char in characters_array if char['Name'] == name}
            class_spells = get_class_spells(characters_classes[name])
            c.execute("""DELETE FROM missingSpells WHERE charName = ? """, (name,))
        conn.commit()
        conn.close()
        # print(characters_classes)
        character_spellbooks = create_character_spellbooks(characters_array, name, eq_dir)
        # DOES exist:
        #print(class_spells)
        # Doesnt exist:
        #print(characters_classes)
        try:
            
            for char, char_class in characters_classes.items():
                try:
                    for spell in class_spells[char_class]:
                        try: 
                            if spell not in character_spellbooks[char]:
                                spell = (char,) + spell
                                missing_spells.append(spell)
                        except Exception as e:
                            continue
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
        # print(missing_spells)
        conn = mymodules.create_connection('./stables.db')
        c = conn.cursor()
        try:
            c.executemany("""INSERT INTO missingspells VALUES (?, ?, ?)""", (missing_spells))
        except Exception as e:
            print(e)
        conn.commit()
        conn.close()
        # print(class_spells['Wizard'])
        # Returns a list of tuples (char_name, lvl, spell_name)
        return missing_spells
# Moved to 'SpellsWindow()'
def missing_spells_window(characters_array, root, name='All', missing_spells_window_open=None, missing_spells_array=[]):

    if missing_spells_window_open:
        return
    missing_spells_window_open = True
    missing_spells_array = []

    def fill_table_with_missing_spells_array(missing_spells_array):
        
        missing_spells_tree.delete(*missing_spells_tree.get_children())
        counter = 0
        for spell in missing_spells_array:
            missing_spells_tree.insert(parent='', index='end', iid=counter, values=(spell[0], spell[2], spell[1]))
            counter += 1

    def query_missing_spells(char_name, missing_spells_array):
        
        missing_spells_array = []
        conn = mymodules.create_connection('./stables.db')
        c = conn.cursor()
        
        selected_char.set(char_name)
        if char_name == 'All':
            c.execute("""SELECT * FROM missingSpells""")
        else:
            c.execute("""SELECT * FROM missingSpells WHERE charName = ? """, (char_name,))

        missing_spells = c.fetchall()
        conn.commit()
        conn.close()
        
        if len(missing_spells) == 0:
            spells_window.destroy()
            messagebox.showinfo("No SpellBook Found", "No 'missing spells' book found.")
            return   
        
        fill_table_with_missing_spells_array(missing_spells)
        
    def delete_missing_spells_tree():
        for item in missing_spells_tree.get_children():
            missing_spells_tree.delete(item)
            print('row deleted from tree')

    def fetch_missing_spells(name):
        global missing_spells_array
        conn = mymodules.create_connection('./stables.db')
        c = conn.cursor()
        if name == 'All':
            c.execute("""SELECT * FROM missingSpells""")
            missing_spells_array = c.fetchall()
        else:
            c.execute("""SELECT * FROM missingSpells WHERE charName = ? """, (name,))
            missing_spells_array = c.fetchall()
        print(missing_spells_array)

    # Get char names
    char_list = fetch_missing_spells_char_names()

    spells_window = Toplevel(root)
    spells_window.title("Missing Spells")
    # Config row and col heights:
    spells_window.grid_rowconfigure(1, weight=1)
    spells_window.grid_columnconfigure(0, weight=1)
    # Create scrollbar for Treeview
    spells_window_scrollbar = Scrollbar(spells_window, orient="vertical")
    spells_window_scrollbar.grid(row=0, column=1, sticky="ns")
    # Create the Treeview widget
    missing_spells_tree = ttk.Treeview(spells_window)
    missing_spells_tree['columns'] = ('Char Name', 'Spell Name', 'Level')
    missing_spells_tree.grid(row=0, column=0, sticky="nsew")
    # Config Scrollbar
    spells_window_scrollbar.configure(command=missing_spells_tree.yview)
    missing_spells_tree.configure(yscrollcommand=spells_window_scrollbar.set)

    spells_window.rowconfigure(0, weight=1)
    spells_window.columnconfigure(0, weight=1)
    # Cols
    missing_spells_tree.column('#0', width=0, stretch=NO)
    missing_spells_tree.column('Char Name')
    missing_spells_tree.column('Spell Name')
    missing_spells_tree.column('Level')
    # Headings
    missing_spells_tree.heading('Char Name', text='Char Name')
    missing_spells_tree.heading('Spell Name', text='Spell Name')
    missing_spells_tree.heading('Level', text='Level')
    # Select Char Frame
    select_char_frame = LabelFrame(spells_window, text="Select Character")
    select_char_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    select_char_label = Label(select_char_frame, text="SELECT CHAR:", anchor="w")
    select_char_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    selected_char = StringVar()
    select_char_pulldown = ttk.Combobox(select_char_frame, textvariable=selected_char, values=char_list, state="readonly")
    select_char_pulldown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    selected_char.set('ALL')

    def selected_character_changed(*args, missing_spells_array):
        
        missing_spells_array = []
        name = selected_char.get()
        query_missing_spells(name, '')

    def close_spells_window(missing_spells_window_open, missing_spells_array):
        
        missing_spells_window_open = False
        missing_spells_array = []
        spells_window.destroy()

    spells_window.protocol("WM_DELETE_WINDOW", lambda event=None: close_spells_window(missing_spells_window_open, missing_spells_array))
    select_char_pulldown.bind("<<ComboboxSelected>>", lambda event, array=missing_spells_array: selected_character_changed(missing_spells_array=array))

   
    query_missing_spells(name, missing_spells_array)
       

def create_all_spells_dbs(characters_array, eq_dir, name):
    delete_all_spell_tables()
    create_character_spellbooks(characters_array, 'All', eq_dir)
    create_class_spells_db()
    create_missing_spells_db(characters_array, eq_dir, name)

def fetch_missing_spells_char_names():
    res = []
    conn = mymodules.create_connection('./stables.db')
    c = conn.cursor()
    c.execute("""SELECT DISTINCT charName FROM missingSpells""")
    char_names = c.fetchall()
    conn.commit()
    conn.close()
    for name in char_names:
        res.append(name[0])
    res.append('All')
    res.sort()
    return res
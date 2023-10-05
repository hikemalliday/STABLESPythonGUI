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
import inventory
from tkinter import messagebox
import threading
def row_right_click(e):
    item = my_tree.identify_row(e.y)
    if item:
        my_tree.selection_set(item)
        right_click_menu.post(e.x_root, e.y_root)
        name = my_tree.item(item, "values")[0]
        char_class = my_tree.item(item, "values")[1]
        right_click_menu.entryconfig("Edit", command=lambda: menu_item_right_click("Edit", name, '', ''))
        right_click_menu.entryconfig("Delete", command=lambda: menu_item_right_click("Delete", name, '', ''))
        right_click_menu.entryconfig("Open Inventory", command=lambda: menu_item_right_click("Open Inventory", name, '', ''))
        right_click_menu.entryconfig("Parse Inventory File", command=lambda: menu_item_right_click("Parse Inventory File", name, '', eq_dir))
        right_click_menu.entryconfig("Copy UI", command=lambda c=char_class: menu_item_right_click("Copy UI", name, char_class, eq_dir))
        right_click_menu.entryconfig("Get Camp Location", command=lambda : menu_item_right_click("Get Camp Location", name, '', eq_dir))
        right_click_menu.entryconfig("Missing Spells", command=lambda : menu_item_right_click("Missing Spells", name, char_class, eq_dir))
               
class_options = [
        'All',
        'Bard',
        'Cleric',
        'Druid',
        'Enchanter',
        'Mage',
        'Monk',
        'Necromancer',
        'Paladin',
        'Ranger',
        'Rogue',
        'Shadow Knight',
        'Shaman',
        'Warrior',
        'Wizard'
        ]

characters_array = []
inventory_array = []
missing_spells_array = []
new_char_window_open = False
edit_char_window_open = False
# inventory_window_open = False
eq_dir_window_open = False
# missing_spells_window_open = False
eq_dir = 'c:/r99'

root = Tk()
root.title('S T A B L E S')
inputSearch = Entry(root, width=100, bd=5, font = ('Arial Bold', 15))
inputSearch.grid(row=0, column=0, columnspan=7, padx=5, pady=5)
my_tree = ttk.Treeview(root)
my_tree['columns'] = ('Name', 'Class', 'Account', 'Password', 'EmuAccount', 'EmuPassword', 'Server', 'Location')
my_tree.bind("<Button-3>", row_right_click)
my_tree.grid(row=1, column=0, columnspan=8, padx=10, pady=10, sticky="nsew")
tree_scrollbar = Scrollbar(root, orient="vertical", command=my_tree.yview)
tree_scrollbar.grid(row=1, column=8, sticky="ns")
my_tree.configure(yscrollcommand=tree_scrollbar.set)

select_class_frame = LabelFrame(root, text="Select Class")
select_class_frame.grid(row=0, column=0, padx=5, pady=5, sticky="W")
select_class_label = Label(select_class_frame, text="CLASS:", anchor="w")
select_class_label.grid(row=0, column=0, padx=(5, 0), pady=5, sticky="w")
selected_class = StringVar()
selected_class.set(class_options[0])
select_class_pulldown = OptionMenu(select_class_frame, selected_class, *class_options)
select_class_pulldown.grid(row=0, column=1, padx=5, pady=5, sticky="w")

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

right_click_menu = Menu(root, tearoff=0)
right_click_menu.add_command(label = "Edit")
right_click_menu.add_command(label = "Delete")
right_click_menu.add_command(label = "Open Inventory")
right_click_menu.add_command(label = "Parse Inventory File")
right_click_menu.add_command(label = "Copy UI")
right_click_menu.add_command(label = "Get Camp Location")
right_click_menu.add_command(label = "Missing Spells")

def menu_item_right_click(option, name, char_class, eq_dir):
    if option == 'Edit':
        edit_character_window(name)
        
    elif option == 'Delete':
        delete_character(name)
        
    elif option == 'Open Inventory':
        inventory.inventory_window(name, inventory_window_open=False, inventory_array=inventory_array, characters_array=characters_array, root=root)
        
    elif option == 'Parse Inventory File':
        create_inventory(name, eq_dir)
         
    elif option == 'Copy UI':
        copy_ui(eq_dir, char_class, name)
    
    elif option == 'Get Camp Location':
        mymodules.get_camp_location(my_tree, inputSearch, characters_array, selected_class, eq_dir, name)

    elif option == 'Missing Spells':
        spells.missing_spells_window(characters_array, root, name)

# Could put this into module because of passed in global params
def copy_ui(eq_dir, char_class, name):
    print('eq_dir', eq_dir)
    print('char_class', char_class)
    print('name', name)
    
    try:
        with open(f'./classUIs/UI_{char_class}_P1999PVP.ini', 'r') as file:
            ui_file = file.read()
            print('test ui 1')
        with open(f'{eq_dir}/UI_{name}_P1999PVP.ini', 'w') as file:
            file.write(ui_file)
            print('test ui 2')
        with open(f'./classUIs/{char_class}_P1999PVP.ini', 'r') as file:
            ui_file2 = file.read()
            print('test ui 3')
        with open(f'{eq_dir}/{name}_P1999PVP.ini', 'w') as file:
            file.write(ui_file2)
            print('test ui 4')
        print('UI Copy successful?')
    except FileNotFoundError as e:
        print(f'File not found: {e}')
    except PermissionError as e:
        print(f'Permission error: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')
# could modulize this too with parameter passing:
def eq_directory():
    global eq_dir_window_open
    global eq_dir
    if eq_dir_window_open:
        return
    eq_dir_window_open = True

    eq_dir_window = Toplevel(root)
    eq_dir_window.title("Set EQ Directory")
    eq_dir_window.grid_rowconfigure(1, weight=1)
    eq_dir_window.grid_columnconfigure(0, weight=1)
    eq_dir_frame = LabelFrame(eq_dir_window, text="Please Enter EQ Directory")
    eq_dir_frame.grid(row=0, column=0, padx=5, pady=5, sticky="W")
    eq_dir_input = Entry(eq_dir_frame, width=50, bd=5, font=('Ariel', 15))
    eq_dir_input.insert(0, eq_dir)
    eq_dir_input.grid(row=0, column=0, padx=5, pady=5)
    
    def set_eq_dir():
        global eq_dir
        conn = mymodules.create_connection('./stables.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM eqDir")
        row_count = c.fetchone()[0]

        if row_count == 0:
            c.execute("""INSERT INTO eqDir (eqDir) VALUES (?)""", (eq_dir_input.get(),))
        else:
            c.execute("""UPDATE eqDir SET eqDir = ?""", (eq_dir_input.get(),))

        eq_dir = eq_dir_input.get()
        conn.commit()
        conn.close()
        
    def close_eq_dir_window():
        global eq_dir_window_open
        eq_dir_window_open = False
        set_eq_dir()
        print(eq_dir)
        eq_dir_window.destroy()

    ok_button = Button(eq_dir_window, text="OK", command=lambda: close_eq_dir_window())
    ok_button.grid(row=1, columnspan=2, pady=10)
    eq_dir_window.protocol("WM_DELETE_WINDOW", close_eq_dir_window)
    eq_dir_input.bind("<Return>", lambda event: close_eq_dir_window())
    
def selected_class_changed(*args):
    mymodules.query_characters_array(characters_array, None, selected_class.get(), my_tree, inputSearch)

def show_please_wait_window():
    please_wait_window = Toplevel(root)
    please_wait_window.title("Please Wait...")
    label = Label(please_wait_window, text="Parsing/writing, please wait...", padx=20, pady=20)
    label.pack()

    log_text = Text(please_wait_window, wrap=WORD, width=50, height=10)
    log_text.pack()

    return please_wait_window, log_text

def create_inventory(name, eq_dir):
    delete_inventory_db(name)
    please_wait_window, log_text = show_please_wait_window()
    root.update()
    char_names = []
    # Get list of char_names
    if name == 'All':
        char_names = [char['Name'] for char in characters_array]
    else:
        char_names = [char['Name'] for char in characters_array if char['Name'] == name]
    char_names.sort()
    # Parse the eq_dir for the files
    conn = mymodules.create_connection('./stables.db')
    c = conn.cursor()
    count = 0
    try:
        for char in char_names:
            char_inventory_array = []
            file_paths = [f'{eq_dir}/{char}', f'{eq_dir}/{char}.txt']
            for file_path in file_paths:
                try:
                    with open(file_path) as file:
                        file.readline()
                        batch_inserts = [] 
                        for line in file:
                            
                            line = line.strip().split('\t')
                            if line[1] == 'Piece of a medallion':
                                print('line2 found')
                                if line[2] == '19956':
                                    line[1] = 'Piece of a medallion (Pained Soul)'
                                if line[2] == '19957':
                                    line[1] = 'Piece of a medallion (Rotting Skeleton)'
                                if line[2] == '19958':
                                    line[1] = 'Piece of a medallion (A Bloodgill Maurader)'
                                if line[2] == '19960':
                                    line[1] = 'Piece of a medallion (An Ancient Jarsath)'
                                if line[2] == '19961':
                                    line[1] = 'Piece of a medallion (Swamp of No Hope)'
                                if line[2] == '19962':
                                    line[1] = 'Piece of a medallion (Kaesora)'
                                if line[2] == '19963':
                                    line[1] = 'Piece of a medallion (Verix Kyloxs Remains)'
                            
                            char_inventory_array.append(line)
                            if len(line) != 5:
                                continue
                            batch_inserts.append((char, line[0], line[1], line[2], line[3], line[4]))
                            count += 1
                        if batch_inserts:
                            c.executemany("""INSERT INTO inventory (charName, itemLocation, itemName, itemId, itemCount, itemSlots) VALUES (?, ?, ?, ?, ?, ?)""", batch_inserts)
                            conn.commit()
                            log_text.insert(1.0, f'{len(batch_inserts)} rows inserted. ({char}.inventory)\n')
                            log_text.insert(1.0, f'Total inserts:{count}\n')
                            log_text.update()
                except FileNotFoundError:
                    pass
    except Exception as e:
        log_text.insert(1.0, f'Error: {str(e)}\n')
        log_text.update()
        print(e)
    finally:
        log_text.insert(1.0, 'Database created.\n')
        log_text.update()
        please_wait_window.destroy()
        conn.close()
    return

def delete_inventory_db(name):
    conn = mymodules.create_connection('./stables.db')
    c = conn.cursor()
    if name == 'All':
        try:
            c.execute("""DELETE from Inventory""")
            conn.commit()
            print('Entire inventory db deleted')
        except Exception as e:
            print(e)
    else:
        try:
            c.execute("""DELETE from Inventory WHERE charName = ?""", (name,))
            conn.commit()
            print('deleted single db')
        except Exception as e:
            print(e)
    conn.close()

def delete_character(name):
    global characters_array
    try:
        # perform query to delete item
        conn = mymodules.create_connection("./stables.db")
        c = conn.cursor()
        c.execute("""DELETE FROM Characters WHERE charName = ? """, (name,))
        conn.commit()
        conn.close()
        characters_array = [char for char in characters_array if char['Name'] != name]
        selected_item = my_tree.selection()  # Get the selected item(s)
        for item in selected_item:
            my_tree.delete(item)  # Delete the selected item(s)
    except Error as e:
        print('Char Delete Query Failed!')
        print(e)
    return

def edit_character_window(name):
    global edit_char_window_open
    old_name = name
    if edit_char_window_open:
        return
    edit_char_window_open = True

    edit_char_window = Toplevel(root)
    edit_char_window.title("Edit Character")
    labels = ['Name', 'Class', 'Account', 'Password', 'EmuAccount', 'EmuPassword', 'Server', 'Location']
    entry_widgets = {}

    character_to_edit = None
    for character in characters_array:
        if character['Name'] == name:
            character_to_edit = character
            break
    if character_to_edit is None:
        print(f"Character with name '{name}' not found.")
        return

    for label_text in labels:
        label = Label(edit_char_window, text=label_text)
        label.grid(row=labels.index(label_text), column=0, padx=10, pady=5, sticky="w")

        entry_widgets[label_text] = Entry(edit_char_window, width=30)
        print('label text test')
        print(entry_widgets[label_text])
        if character_to_edit.get(label_text, '') == None:
            character_to_edit[label_text] = 'None'
        entry_widgets[label_text].insert(0, character_to_edit.get(label_text, ''))
        entry_widgets[label_text].grid(row=labels.index(label_text), column=1, padx=10, pady=5, sticky="w")

    def edit_character_button(character):
        global edit_char_window_open
        # We have passed in the character object, now we need to mutate it
        class_id_mapping = {
        'Bard': 1,
        'Cleric': 2,
        'Druid': 3,
        'Enchanter': 4,
        'Mage': 5,
        'Monk': 6,
        'Necromancer': 7,
        'Paladin': 8,
        'Ranger': 9,
        'Rogue': 10,
        'Shadow Knight': 11,
        'Shaman': 12,
        'Warrior': 13,
        'Wizard': 14
    }
        character_data = {label: entry_widgets[label].get() for label in labels}
        # Logic to typo handle 'Class' here
        if character_data['Class'] == 'Magician':
            character_data['Class'] = 'Mage'
        if character_data['Class'] == 'Shadowknight':
            character_data['Class'] = 'Shadow Knight'
        char_class_name = character_data['Class']
        char_class_id = class_id_mapping.get(char_class_name, None)
        if char_class_id is not None:
            character_data['Class'] = char_class_id
        else:
            print(f"Warning: Uknown character class '{char_class_name}'")
    
        conn = mymodules.create_connection('./stables.db')
        c = conn.cursor()
        c.execute(""" UPDATE characters SET charName = ? , classID = ?, account = ?, password = ?, emuAccount = ?, emuPassword = ?, server = ?, location = ? WHERE charName = ? """,
                  (
                    character_data['Name'],
                    character_data['Class'],
                    character_data['Account'],
                    character_data['Password'],
                    character_data['EmuAccount'],
                    character_data['EmuPassword'],
                    character_data['Server'],
                    character_data['Location'],
                    old_name,
                ))
       
        conn.commit()
        conn.close()

        # Mutate the local 'character' object:
        character['Name'] = character_data['Name']
        character['Class'] = char_class_name
        character['Account'] = character_data['Account']
        character['Password'] = character_data['Password']
        character['EmuAccount'] = character_data['EmuPassword']
        character['EmuPassowrd'] = character_data['EmuPassword']
        character['Server'] = character_data['Server']
        character['Location'] = character_data['Location']

        edit_char_window_open = False
        # Change value back after SQL insert
        character_data['Class'] = char_class_name
        mymodules.query_characters_array(characters_array, 'e', selected_class.get(), my_tree, inputSearch)
        edit_char_window.destroy()

    def close_edit_char_window():
        global edit_char_window_open
        edit_char_window_open = False
        edit_char_window.destroy()

    create_button = Button(edit_char_window, text="Edit Character", command=lambda: edit_character_button(character))
    create_button.grid(row=len(labels), columnspan=2, pady=10)
    edit_char_window.protocol("WM_DELETE_WINDOW", close_edit_char_window)
    
def create_new_character_window():
    global new_char_window_open
    if new_char_window_open:
        return
    new_char_window_open = True

    new_char_window = Toplevel(root)
    new_char_window.title("New Character")
    labels = ['Name', 'Class', 'Account', 'Password', 'EmuAccount', 'EmuPassword', 'Server', 'Location']
    entry_widgets = {}

    for label_text in labels:
        label = Label(new_char_window, text=label_text)
        label.grid(row=labels.index(label_text), column=0, padx=10, pady=5, sticky="w")

        entry_widgets[label_text] = Entry(new_char_window, width=30)
        entry_widgets[label_text].grid(row=labels.index(label_text), column=1, padx=10, pady=5, sticky="w")

    def create_new_character_button():
        global new_char_window_open
        class_id_mapping = {
            'Bard': 1,
            'Cleric': 2,
            'Druid': 3,
            'Enchanter': 4,
            'Mage': 5,
            'Monk': 6,
            'Necromancer': 7,
            'Paladin': 8,
            'Ranger': 9,
            'Rogue': 10,
            'Shadow Knight': 11,
            'Shaman': 12,
            'Warrior': 13,
            'Wizard': 14
        }
        character_data = {label: entry_widgets[label].get() for label in labels}
        if character_data['Class'] == 'Magician':
            character_data['Class'] = 'Mage'
        if character_data['Class'] == 'Shadowknight':
            character_data['Class'] = 'Shadow Knight'
        insert_new_character(character_data)
        char_class_name = character_data['Class']
        char_class_id = class_id_mapping.get(char_class_name, None)
        if char_class_id is not None:
            character_data['Class'] = char_class_id
        else:
            print(f"Warning: Unknown character class '{char_class_name}")
        print("New Character Data:", character_data)
        # Convert charClass to charID
        # Connect to DB:
        conn = mymodules.create_connection('./stables.db')
        c = conn.cursor()
        c.execute(""" INSERT INTO Characters (charName, classID, emuAccount, emuPassword, account, password, server, location)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (
        character_data['Name'],
        character_data['Class'],
        character_data['Account'],
        character_data['Password'],
        character_data['EmuAccount'],
        character_data['EmuPassword'],
        character_data['Server'],
        character_data['Location'],
     ))
        
        conn.commit()
        new_char_window_open = False
        # Change value back after SQL insert
        character_data['Class'] = char_class_name
        new_char_window.destroy()

    def close_new_char_window():
        global new_char_window_open
        new_char_window_open = False
        new_char_window.destroy()

    create_button = Button(new_char_window, text="Create Character", command=create_new_character_button)
    create_button.grid(row=len(labels), columnspan=2, pady=10)
    new_char_window.protocol("WM_DELETE_WINDOW", close_new_char_window)

def insert_new_character(character_data):
    iids = my_tree.get_children()
    integers = [int(iid) for iid in iids]
    if integers:
        max_counter = max(integers)
        max_counter += 1
    else:
        max_counter = 0
    print('newchartest')
    print(character_data)
    characters_array.append(character_data)
    my_tree.insert(parent='', index='end', iid=max_counter, text="", values=(
            character_data['Name'], character_data['Class'], character_data['Account'], character_data['Password'],
            character_data['EmuAccount'], character_data['EmuPassword'], character_data['Server'], character_data['Location']))

def create_menus():
    menu_bar = Menu(root)
    root.config(menu = menu_bar)
    # File
    file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New Character", command=create_new_character_window)
    file_menu.add_command(label="Set EQ dir", command=eq_directory)
    file_menu.add_command(label="Get All Camp Locations", command=lambda: mymodules.get_camp_location(my_tree, inputSearch, characters_array,selected_class, eq_dir, name='All'))
    file_menu.add_command(label="Exit", command=lambda: mymodules.exit_app(root))
    # Inventory
    inventory_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Inventory", menu=inventory_menu)
    inventory_menu.add_command(label="Open Inventory Reader", command=lambda: inventory.inventory_window('All', inventory_window_open=False, inventory_array=inventory_array, characters_array=characters_array, root=root))
    inventory_menu.add_command(label="Parse All Inventory Files", command=lambda: create_inventory('All', eq_dir))
    inventory_menu.add_command(label="Delete Entire Inventory DB", command=lambda: delete_inventory_db('All'))
    # Spells
    spells_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Spells", menu=spells_menu)
    spells_menu.add_command(label="Create Missing Spells DB", command=lambda: spells.create_all_spells_dbs(characters_array, eq_dir, 'All'))
    spells_menu.add_command(label="Missing Spells Window", command=lambda: spells.missing_spells_window(characters_array, root, 'All', missing_spells_window_open = None, missing_spells_array=[]))
    spells_menu.add_command(label="Delete Entire Spells DB", command=lambda: spells.delete_spells_db(eq_dir, 'All'))
    
def create_columns():
    my_tree.column('#0', width=0, stretch=NO)
    my_tree.column('Name', anchor=W)
    my_tree.column('Class')
    my_tree.column('Account')
    my_tree.column('Password')
    my_tree.column('EmuAccount')
    my_tree.column('EmuPassword')
    my_tree.column('Server')
    my_tree.column('Location')

def create_headings():
    my_tree.heading("#0", text="")
    my_tree.heading("Name", text="Name", command=lambda: mymodules.sort_column("Name", False, my_tree))
    my_tree.heading("Class", text="Class", command=lambda: mymodules.sort_column("Class", False, my_tree))
    my_tree.heading("Account", text="Account", command=lambda: mymodules.sort_column("Account", False, my_tree))
    my_tree.heading("Password", text="Password", command=lambda: mymodules.sort_column("Password", False, my_tree))
    my_tree.heading("EmuAccount", text="EmuAccount", command=lambda: mymodules.sort_column("EmuAccount", False, my_tree))
    my_tree.heading("EmuPassword", text="EmuPassword", command=lambda: mymodules.sort_column("EmuPassword", False, my_tree))
    my_tree.heading("Server", text="Server", command=lambda: mymodules.sort_column("Server", False))
    my_tree.heading("Location", text="Location", command=lambda: mymodules.sort_column("Location", False, my_tree))

inputSearch.bind("<KeyRelease>", lambda event: mymodules.query_characters_array(characters_array, event, selected_class.get(), my_tree, inputSearch))
selected_class.trace("w", selected_class_changed)

if __name__ == '__main__':
    mymodules.create_tables()
    create_columns()
    create_headings()
    create_menus()
    mymodules.fetch_eq_dir()
    mymodules.fetch_all_characters(characters_array, my_tree)
    mymodules.sort_column("Name", False, my_tree)
    # mymodules.delete_all_characters()
    # spells.create_missing_spells_db()
    # spells.get_all_spell_tables()
    # spells.create_character_spellbooks(characters_array, 'All', eq_dir)
    # spells.test_fetch_spell('', '')
    
    
    root.mainloop()









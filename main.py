from tkinter import *
from tkinter import ttk
import sqlite3
from sqlite3 import Error
from tkinter import Menu
import json

def fetch_eq_dir():
    global eq_dir
    conn = create_connection('./stables.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM eqDir""")
    try:
        eq_dir = c.fetchall()[0][0]
    except Exception as e:
        print('no eq DIR set yet')
    print(eq_dir)

def row_right_click(e):
    item = my_tree.identify_row(e.y)
    if item:
        my_tree.selection_set(item)
        right_click_menu.post(e.x_root, e.y_root)
        name = my_tree.item(item, "values")[0]
        right_click_menu.entryconfig("Edit", command=lambda n=name: menu_item_right_click("Edit", n))
        right_click_menu.entryconfig("Delete", command=lambda n=name: menu_item_right_click("Delete", n))
        right_click_menu.entryconfig("Open Inventory", command=lambda n=name: menu_item_right_click("Open Inventory", n))
        right_click_menu.entryconfig("Parse Inventory File", command=lambda n=name: menu_item_right_click("Parse Inventory File", n))
        print(name)

def menu_item_right_click(option, name):
    if option == 'Edit':
        edit_character_window(name)
        pass
    elif option == 'Delete':
        delete_character(name)
        pass
    elif option == 'Open Inventory':
        inventory_window(name)
        pass
    elif option == 'Parse Inventory File':
        create_inventory(name, eq_dir)
        print('parse inventory char right click')
        pass

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
new_char_window_open = False
edit_char_window_open = False
inventory_window_open = False
eq_dir_window_open = False
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
        conn = create_connection('./stables.db')
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
    query_characters_array(None, selected_class.get())

def inventory_window(name):
    global inventory_window_open
    global inventory_array

    if inventory_window_open:
        return
    inventory_window_open = True

    def fill_table_with_inventory_array():
        inv_tree.delete(*inv_tree.get_children())
        counter = 0
        for item in inventory_array:
            inv_tree.insert(parent='', index='end', iid = counter, text="", values=(item[0], item[2], item[1], item[3], item[4]))
            counter += 1

    def query_char_inventory(name, item_name):
        global inventory_array
        inventory_array = []
        conn = create_connection('./stables.db')
        c = conn.cursor()
        selected_char.set(name)
        print(name)
        print(item_name)
        if name == 'All':
            print('all test')
            c.execute("""SELECT * FROM inventory WHERE itemName LIKE ?""", ('%' + item_name + '%',))
        else:
            print('else test')
            c.execute("""SELECT * FROM inventory WHERE charName = ?""", (name,))
        
        char_inventory = c.fetchall()
        print(char_inventory)
        for item in char_inventory:
            inventory_array.append(item)

        fill_table_with_inventory_array()
        conn.commit()
        conn.close()

    def selected_inventory_changed(*args):
        global inventory_array
        inventory_array = []
        name = selected_char.get()
        query_char_inventory(name, '')
    
    def delete_inv_tree():
        for item in inv_tree.get_children():
            inv_tree.delete(item)
            print('row deleted from tree')

    char_list = [char['Name'] for char in characters_array]
    char_list.append('ALL')
    char_list.sort()
    inv_window = Toplevel(root)
    inv_window.title("Inventory Reader")
    inv_window.grid_rowconfigure(1, weight=1)
    inv_window.grid_columnconfigure(0, weight=1)
    inv_tree = ttk.Treeview(inv_window)
    inv_tree['columns'] = ('Char Name', 'Item Name', 'Location', 'Item ID', 'Count')
    inv_tree.grid(row=1, column=0, columnspan=8, padx=10, pady=10, sticky="nsew")
    inv_search = Entry(inv_window, width=100, bd=5, font = ('Arial Bold', 15))
    inv_search.grid(row=0, column=0, columnspan=7, padx=5, pady=5)
    inv_search.bind("<Return>", lambda event: query_char_inventory(name, inv_search.get()))
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
    inv_tree.heading("#0", text='')
    inv_tree.heading("Char Name", text='Char Name')
    inv_tree.heading("Item Name", text='Item Name')
    inv_tree.heading("Location", text='Location')
    inv_tree.heading("Item ID", text='Item ID')
    inv_tree.heading("Count", text='Count')
    # Select Char Frame
    select_char_frame = LabelFrame(inv_window, text="Select Character")
    select_char_frame.grid(row=0, column=0, padx=5, pady=5, sticky="W")
    select_char_label = Label(select_char_frame, text="SELECT CHAR:", anchor="w")
    select_char_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    selected_char = StringVar()
    select_char_pulldown = ttk.Combobox(select_char_frame, textvariable=selected_char, values=char_list, state="readonly")
    select_char_pulldown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    selected_char.set('ALL')
    
    query_char_inventory(name, '')    
            
    def close_inventory_window():
        global inventory_window_open
        global inventory_array
        inventory_window_open = False
        inventory_array = []
        inv_window.destroy()

    inv_window.protocol("WM_DELETE_WINDOW", close_inventory_window)
    select_char_pulldown.bind("<<ComboboxSelected>>", lambda event: selected_inventory_changed())
    
def show_please_wait_window():
    please_wait_window = Toplevel(root)
    please_wait_window.title("Please Wait...")
    label = Label(please_wait_window, text="Parsing/writing, please wait...", padx=20, pady=20)
    label.pack()

    log_text = Text(please_wait_window, wrap=WORD, width=50, height=10)
    log_text.pack()

    return please_wait_window, log_text

# Parses inventory file(s) and uploads to SQLite:
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
    conn = create_connection('./stables.db')
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
    conn = create_connection('./stables.db')
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
        conn = create_connection("./stables.db")
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

def fill_table_with_characters_array():
    for item in my_tree.get_children():
        my_tree.delete(item)
    counter = 0
    # iterate over 'characters_array' and fill table
    for character in characters_array:
        my_tree.insert(parent='', index='end', iid = counter, text="", values=(character['Name'], character['Class'], character['Account'], character['Password'], character['EmuAccount'], character['EmuPassword'], character['Server'], character['Location']))
        counter += 1
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
    
        conn = create_connection('./stables.db')
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
        query_characters_array('e', selected_class.get())
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
        conn = create_connection('./stables.db')
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

def exit_app():
    root.quit()

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def fetch_row_test():
    database = "./stables.db"
    conn = create_connection(database)
    c = conn.cursor()
    c.execute("SELECT * FROM characters WHERE charName = 'test'")
    row = c.fetchall()
    print(row)

def fetch_all_characters():
    database = "./stables.db"
    conn = create_connection(database)
    c = conn.cursor()
    c.execute("SELECT * FROM characters")
    rows = c.fetchall()
    # Add Data
    for row in rows:
        class_id_mapping = {
        1: 'Bard',
        2: 'Cleric',
        3: 'Druid',
        4: 'Enchanter',
        5: 'Mage',
        6: 'Monk',
        7: 'Necromancer',
        8: 'Paladin',
        9: 'Ranger',
        10: 'Rogue',
        11: 'Shadow Knight',
        12: 'Shaman',
        13: 'Warrior',
        14: 'Wizard'
        }
        
        row_object = {
            'Name': row[1],
            'Class': class_id_mapping.get(row[2], None),
            'Account': row[3],
            'Password': row[4],
            'EmuAccount': row[5],
            'EmuPassword': row[6],
            'Server': row[7],
            'Location': row[8]
        }

        characters_array.append(row_object)
    # filtered_characters = copy.deepcopy(characters_array)
    fill_table_with_characters_array()
    conn.close()

def create_tables():
    database = r"./stables.db"

    sql_create_characters_table = """ Create TABLE IF NOT EXISTS characters (
                                    charID integer PRIMARY KEY AUTOINCREMENT,
                                    charName text NOT NULL,
                                    classID integer,
                                    account text,
                                    password text,
                                    emuAccount text,
                                    emuPassword text,
                                    server text,
                                    location text
    );"""

    sql_create_characterClasses_table = """ Create TABLE IF NOT EXISTS characterClasses (
                                 classID integer PRIMARY KEY,
                                 charClass text
    );"""

    sql_create_eqDir_table = """ Create TABLE IF NOT EXISTS eqDir (
                                 eqDir text PRIMARY KEY
    );"""

    sql_create_classSpells_table = """ Create TABLE IF NOT EXISTS classSpells (
                                       charClass text,
                                       spellLevel integer,
                                       spellName text
    );"""

    sql_create_spellbooks_table = """ Create TABLE IF NOT EXISTS spellbooks (
                                       charName text,
                                       spellLevel integer,
                                       spellName text
    );"""

    sql_create_inventory_table = """ Create TABLE IF NOT EXISTS inventory (
                                       charName text,
                                       itemLocation text,
                                       itemName text,
                                       itemId integer,
                                       itemCount integer,
                                       itemSlots integer
    );"""

    conn = create_connection(database)
    # c = conn.cursor()
    if conn is not None:
        create_table(conn, sql_create_characters_table)
        create_table(conn, sql_create_characterClasses_table)
        create_table(conn, sql_create_eqDir_table)
        create_table(conn, sql_create_classSpells_table)
        create_table(conn, sql_create_spellbooks_table)
        create_table(conn, sql_create_inventory_table)
    conn.close()

def create_menus():
    menu_bar = Menu(root)
    root.config(menu = menu_bar)
    # Create a file menu
    file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    # Add items to the File menu
    file_menu.add_command(label="New Character", command=create_new_character_window)
    file_menu.add_command(label="Set EQ dir", command=eq_directory)
    file_menu.add_command(label="Exit", command=exit_app)
    # Create an Edit menu (just for demonstration)
    inventory_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Inventory", menu=inventory_menu)
    inventory_menu.add_command(label="Open Inventory Reader", command=lambda: inventory_window('All'))
    inventory_menu.add_command(label="Parse All Inventory Files", command=lambda: create_inventory('All', 'c:/r99'))
    inventory_menu.add_command(label="Delete Entire Inventory DB", command=lambda: delete_inventory_db('All'))
    
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
    my_tree.heading("Name", text="Name", command=lambda: sort_column("Name", False))
    my_tree.heading("Class", text="Class")
    my_tree.heading("Account", text="Account")
    my_tree.heading("Password", text="Password")
    my_tree.heading("EmuAccount", text="EmuAccount")
    my_tree.heading("EmuPassword", text="EmuPassword")
    my_tree.heading("Server", text="Server")
    my_tree.heading("Location", text="Location")

def import_json_db():
        json_db = None
        conn = create_connection("./stables.db")
        c = conn.cursor()
        with open("db.json", "r") as json_file:
            json_db = json.load(json_file)
        
        for character in json_db:
            # Map character class names to class IDs
            class_name = character['charclass']
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
            location = character.get('location', None)
            class_id = class_id_mapping.get(class_name, None)
            if class_id is not None:
                c.execute("""
                    INSERT INTO characters (charName, classID, emuAccount, emuPassword, account, password, server, location)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    character['name'],
                    class_id,
                    character['emuaccount'],
                    character['emupassword'],
                    character['account'],
                    character['password'],
                    character['server'],
                location
                ))

                conn.commit()
        conn.close()

def delete_all_characters():
    database = "./stables.db"
    conn = create_connection(database)
    c = conn.cursor()
    
    try:
        c.execute("DELETE FROM characters")
        conn.commit()
        print("All rows deleted from the 'characters' table.")
    except Error as e:
        print(e)
    finally:
        conn.close()

def query_characters_array(event, selected_class):
    search_input_text = inputSearch.get().lower()
    if selected_class == 'All':
        filtered_characters = [char for char in characters_array if search_input_text in char['Name'].lower()]
    else:
         filtered_characters = [char for char in characters_array if char['Class'] == selected_class and search_input_text in char['Name'].lower()]
    
    for item in my_tree.get_children():
        my_tree.delete(item)

    counter = 0
    for char in filtered_characters:
        my_tree.insert(parent='', index='end', iid=counter, text="", values=(
            char['Name'], char['Class'], char['Account'], char['Password'],
            char['EmuAccount'], char['EmuPassword'], char['Server'], char['Location']))
        counter += 1
    sort_column("Name", False)
    return

def custom_sort(col, reverse):
    data = [(my_tree.set(item, col) ,item)for item in my_tree.get_children('')]
    data.sort(reverse=reverse)
    for index, (val, item) in enumerate(data):
        my_tree.move(item, '', index)
    my_tree.heading(col, command=lambda: sort_column(col, not reverse))

def sort_column(col, reverse):
    my_tree.heading(col, command=lambda: custom_sort(col, reverse))
    custom_sort(col, reverse)

inputSearch.bind("<KeyRelease>", lambda event: query_characters_array(event, selected_class.get()))
selected_class.trace("w", selected_class_changed)
# Not sure why this condition is needed, or what it even does:
if __name__ == '__main__':
    create_tables()
    fetch_all_characters()
    fetch_row_test()
    create_columns()
    create_headings()
    create_menus()
    sort_column("Name", False)
    # delete_inventory_db('All')
    # import_json_db()
    fetch_eq_dir()
    root.mainloop()









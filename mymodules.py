from tkinter import *
from tkinter import ttk
import sqlite3
from sqlite3 import Error
from tkinter import Menu
import json
import os
from tkinter import scrolledtext
import re
import threading

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def fetch_eq_dir():
    conn = create_connection('./stables.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM eqDir""")
    try:
        return c.fetchall()[0][0]
    except Exception as e:
        return 'c:/r99'
    
def query_characters_array(characters_array, event, selected_class, tree, inputSearch):
        search_input_text = inputSearch.get().lower()
        if selected_class == 'All':
            filtered_characters = [char for char in characters_array if search_input_text in char['Name'].lower()]
        else:
            filtered_characters = [char for char in characters_array if char['Class'] == selected_class and search_input_text in char['Name'].lower()]
        
        for item in tree.get_children():
            tree.delete(item)

        counter = 0
        for char in filtered_characters:
            tree.insert(parent='', index='end', iid=counter, text="", values=(
                char['Name'], char['Class'], char['Account'], char['Password'],
                char['EmuAccount'], char['EmuPassword'], char['Server'], char['Location']))
            counter += 1
        sort_column("Name", False, tree)
        return
# pass in characters_array
# Query_characters_array() and selected_class:
def get_camp_location(tree, inputSearch, characters_array, selected_class, eq_dir, name='All'):
    # Define the regex pattern for matching zone information
    regex = r"^.{27}There (?:is|are) \d+ player(?:s?) in (?!EverQuest)(\D+).$"
    char_names = []
    zone_char_pairs = []
    lines_parsed_per_char = []
    if name == 'All':
        char_names = [character['Name'] for character in characters_array]
    else:
        char_names = [character['Name'] for character in characters_array if character['Name'] == name]

    popup = Toplevel()
    popup.title('Parsing Progress')
    text_widget = scrolledtext.ScrolledText(popup, wrap=WORD)
    text_widget.pack(fill=BOTH, expand=True)
    text_widget.insert(1.0, 'Parsing in progress, please wait until completion...\n')
    text_widget.update()
    counter = 0

    for char_name in char_names:
        if char_name == 'All':
            continue
        log_file_path = f'{eq_dir}/Logs/eqlog_{char_name}_P1999PVP.txt'
        found_regex = False
        try:
            # Open the log file in binary mode
            with open(log_file_path, 'rb') as log_file:
                # Seek to the end of the file
                log_file.seek(0, os.SEEK_END)
                # Read file in reversed order
                while log_file.tell() > 0:
                    log_file.seek(-1, os.SEEK_CUR)
                    char = log_file.read(1).decode('utf-8')
                    if char == '\n':
                        #match = re.match(regex, line)
                        counter += 1
                        log_file.seek(-2, os.SEEK_CUR)
                    line = ''
                    while char != '\n' and log_file.tell() > 0:
                        line = char + line
                        log_file.seek(-2, os.SEEK_CUR)
                        char = log_file.read(1).decode('utf-8')
                        if log_file.tell() <= 0:
                            break 
                        match = re.match(regex, line)
                        if match:
                            lines_parsed_per_char.append([char_name, counter])
                            counter = 0
                            zone_name = match.group(1)
                            text_widget.insert(1.0, f'Character "{char_name}" is camped out in: {zone_name}\n')
                            text_widget.update()
                            zone_char_pairs.append([zone_name, char_name])
                            found_regex = True
                            # Now we need to update the object locally
                            character_to_edit = None
                            for character in characters_array:
                                if character['Name'] == char_name:
                                    character_to_edit = character
                                    break
                            if character_to_edit is None:
                                text_widget.insert(1.0, f"Character with name '{char_name}' not found\n")
                                text_widget.update()
                            character_to_edit['Location'] = zone_name
                            break  # Stop parsing the current log file after finding a match
                    if found_regex:
                        break
                    if counter == 10000:
                        break
        except FileNotFoundError as e:
            text_widget.insert(END, f'File not found: {e}\n')
            text_widget.update()
        except PermissionError as e:
            text_widget.insert(END, f'Permission error: {e}\n')
            text_widget.update()
        except Exception as e:
            text_widget.insert(END, f'An error occurred: {e}\n')
            text_widget.update()

    conn = create_connection('./stables.db')
    c = conn.cursor()
    for zone_name, char_name in zone_char_pairs:
        text_widget.insert(1.0, f'Updating: {zone_name}, {char_name}\n')
        text_widget.update()
        c.execute("UPDATE characters SET location = ? WHERE charName = ?", (zone_name, char_name))
    conn.commit()
    conn.close()
    # Why is this in here?
    # query_characters_array(characters_array, 'e', selected_class.get(), tree, inputSearch)
    text_widget.insert(1.0, 'Parsing complete!\n')
    text_widget.update()
    # print(lines_parsed_per_char)

def custom_sort(col, reverse, tree):
    data = [(tree.set(item, col) ,item)for item in tree.get_children('')]
    data.sort(reverse=reverse)
    for index, (val, item) in enumerate(data):
        tree.move(item, '', index)
    tree.heading(col, command=lambda: sort_column(col, not reverse, tree))

def sort_column(col, reverse, tree):
    tree.heading(col, command=lambda: custom_sort(col, reverse, tree))
    custom_sort(col, reverse, tree)

# def custom_sort(col, reverse, tree):
#     # Create a list of item tags and sort it based on the column values
#     item_tags = list(tree.get_children())
#     item_tags.sort(key=lambda item: tree.set(item, col), reverse=reverse)

#     # Rearrange items in the Treeview based on the sorted tags
#     for index, tag in enumerate(item_tags):
#         tree.move(tag, '', index)

# def sort_column(col, reverse, tree):
#     custom_sort(col, reverse, tree)
#     # Update the sorting function for the column header click
#     header = tree.heading(col)
#     header['command'] = lambda: sort_column(col, not reverse, tree)

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

def import_json_db():
        json_db = None
        conn = create_connection("./stables.db")
        c = conn.cursor()
        with open("db.json", "r") as json_file:
            json_db = json.load(json_file)
        
        for character in json_db:
            # Map character class names to class IDs
            class_name = character['charClass']
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
                    character['charName'],
                    class_id,
                    character['emuAccount'],
                    character['emuPassword'],
                    character['account'],
                    character['password'],
                    character['server'],
                location
                ))

                conn.commit()
        conn.close()

def fill_table_with_characters_array(characters_array, tree):
    for item in tree.get_children():
        tree.delete(item)
    counter = 0
    # iterate over 'characters_array' and fill table
    for character in characters_array:
        tree.insert(parent='', index='end', iid = counter, text="", values=(character['Name'], character['Class'], character['Account'], character['Password'], character['EmuAccount'], character['EmuPassword'], character['Server'], character['Location']))
        counter += 1
    return

def fetch_all_characters(characters_array, tree):
    conn = create_connection("./stables.db")
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
    fill_table_with_characters_array(characters_array, tree)
    conn.close()

def exit_app(root):
    root.quit()

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_tables():
    
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

    sql_create_missingspells_table = """ Create TABLE IF NOT EXISTS missingSpells (
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

    conn = create_connection("./stables.db")
    # c = conn.cursor()
    if conn is not None:
        create_table(conn, sql_create_characters_table)
        create_table(conn, sql_create_characterClasses_table)
        create_table(conn, sql_create_eqDir_table)
        create_table(conn, sql_create_classSpells_table)
        create_table(conn, sql_create_spellbooks_table)
        create_table(conn, sql_create_inventory_table)
        create_table(conn, sql_create_missingspells_table)
        
    conn.close()


    




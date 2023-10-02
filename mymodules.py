from tkinter import *
from tkinter import ttk
import sqlite3
from sqlite3 import Error
from tkinter import Menu
import json
import os
from tkinter import scrolledtext
import re



def fetch_eq_dir():
    conn = create_connection('./stables.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM eqDir""")
    try:
        return c.fetchall()[0][0]
    except Exception as e:
        return 'c:/r99'
    
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

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
    tree.heading(col, command=lambda: sort_column(col, not reverse))

def sort_column(col, reverse, tree):
    tree.heading(col, command=lambda: custom_sort(col, reverse))
    custom_sort(col, reverse, tree)








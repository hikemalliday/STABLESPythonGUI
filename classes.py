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

class main_data:
    def __init__(self):
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
    missing_spells_array = []
    new_char_window_open = False
    edit_char_window_open = False
    inventory_window_open = False
    eq_dir_window_open = False
    missing_spells_window_open = False
    eq_dir = 'c:/r99'

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
# main_window
class MainWindow:
    def __init__(self, data_instance, file_menu_instance):
        self.data = data_instance
        self.file_menu_instance = file_menu_instance
        self.setup_main_window()
        pass

    # Note: changing 'my_tree' to 'char_tree'
    def setup_main_window(self):

        self.root = Tk()
        self.title('S T A B L E S')
        # Char search
        self.inputSearch = Entry(self.root, width=100, bd=5, font = ('Arial Bold', 15))
        self.inputSearch.grid(row=0, column=0, columnspan=7, padx=5, pady=5)
        # Char table/tree
        self.char_tree = ttk.Treeview(self.root)
        self.char_tree['columns'] = ('Name', 'Class', 'Account', 'Password', 'EmuAccount', 'EmuPassword', 'Server', 'Location')
        self.char_tree.bind("<Button-3>", self.row_right_click)
        self.char_tree.grid(row=1, column=0, columnspan=8, padx=10, pady=10, sticky="nsew")
        # Scroll bar
        self.tree_scrollbar = Scrollbar(self.root, orient="vertical", command=self.char_tree.yview)
        self.tree_scrollbar.grid(row=1, column=8, sticky="ns")
        self.char_tree.configure(yscrollcommand=self.tree_scrollbar.set)
        # SELECT CLASS frame
        self.select_class_frame = LabelFrame(self.root, text="Select Class")
        self.select_class_frame.grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.select_class_label = Label(self.select_class_frame, text="CLASS:", anchor="w")
        self.select_class_label.grid(row=0, column=0, padx=(5, 0), pady=5, sticky="w")
        self.selected_class = StringVar()
        self.selected_class.set(self.data.class_options[0])
        self.select_class_pulldown = OptionMenu(self.select_class_frame, self.selected_class, self.data.class_options)
        self.select_class_pulldown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Dependencies: 'root'
        self.right_click_menu = Menu(self.root, tearoff=0)
        self.right_click_menu.add_command(label = "Edit")
        self.right_click_menu.add_command(label = "Delete")
        self.right_click_menu.add_command(label = "Open Inventory")
        self.right_click_menu.add_command(label = "Parse Inventory File")
        self.right_click_menu.add_command(label = "Copy UI")
        self.right_click_menu.add_command(label = "Get Camp Location")
        self.right_click_menu.add_command(label = "Missing Spells")

        self.create_menus()
        self.create_columns()
        self.create_headings()

    def create_menus(self):
        menu_bar = Menu(self.main_window_instance.root)
        self.main_window_instance.root.config(menu = menu_bar)
        # File
        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Character", command=self.file_menu_instance.create_new_character_window)
        file_menu.add_command(label="Set EQ dir", command=self.file_menu_instance.eq_directory)
        file_menu.add_command(label="Get All Camp Locations", command=lambda: mymodules.get_camp_location(self.char_tree, self.inputSearch, self.data.characters_array, self.selected_class, self.data.eq_dir, name='All'))
        file_menu.add_command(label="Exit", command=lambda: mymodules.exit_app(self.main_window.instance.root))
        # Inventory
        inventory_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Inventory", menu=inventory_menu)
        inventory_menu.add_command(label="Open Inventory Reader", command=lambda: inventory.inventory_window('All', inventory_window_open=False, inventory_array=self.data.inventory_array, characters_array=self.data.characters_array, root=self.main_window_instance.root))
        inventory_menu.add_command(label="Parse All Inventory Files", command=lambda: self.file_menu_instance.create_inventory('All', self.data.eq_dir))
        inventory_menu.add_command(label="Delete Entire Inventory DB", command=lambda: delete_inventory_db('All'))
        # Spells
        spells_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Spells", menu=spells_menu)
        spells_menu.add_command(label="Create Missing Spells DB", command=lambda: spells.create_all_spells_dbs(self.data.characters_array, self.data.eq_dir, 'All'))
        spells_menu.add_command(label="Missing Spells Window", command=lambda: spells.missing_spells_window(self.data.characters_array, self.main_window_instance.root, 'All', missing_spells_window_open = None, missing_spells_array=[]))
        spells_menu.add_command(label="Delete Entire Spells DB", command=lambda: spells.delete_spells_db(self.data.eq_dir, 'All'))
 
    def create_columns(self):
        self.my_tree.column('#0', width=0, stretch=NO)
        self.my_tree.column('Name', anchor=W)
        self.my_tree.column('Class')
        self.my_tree.column('Account')
        self.my_tree.column('Password')
        self.my_tree.column('EmuAccount')
        self.my_tree.column('EmuPassword')
        self.my_tree.column('Server')
        self.my_tree.column('Location')

    def create_headings(self):
        self.my_tree.heading("#0", text="")
        self.my_tree.heading("Name", text="Name", command=lambda: mymodules.sort_column("Name", False, self.char_tree))
        self.my_tree.heading("Class", text="Class", command=lambda: mymodules.sort_column("Class", False, self.char_tree))
        self.my_tree.heading("Account", text="Account", command=lambda: mymodules.sort_column("Account", False, self.char_tree))
        self.my_tree.heading("Password", text="Password", command=lambda: mymodules.sort_column("Password", False, self.char_tree))
        self.my_tree.heading("EmuAccount", text="EmuAccount", command=lambda: mymodules.sort_column("EmuAccount", False, self.char_tree))
        self.my_tree.heading("EmuPassword", text="EmuPassword", command=lambda: mymodules.sort_column("EmuPassword", False, self.char_tree))
        self.my_tree.heading("Server", text="Server", command=lambda: mymodules.sort_column("Server", False))
        self.my_tree.heading("Location", text="Location", command=lambda: mymodules.sort_column("Location", False, self.char_tree))


    def selected_class_changed(self, *args):
        mymodules.query_characters_array(self.data.characters_array, None, self.data.selected_class.get(), self.char_tree, self.inputSearch)
# Break up into other classes
class RightClickMethods:
    def __init__(self, data_instance, main_window_instance):
        self.data = data_instance
        self.main_window_instance = main_window_instance

    # Dependencies: 'char_tree', 
    def row_right_click(self, e):
        item = self.char_tree.identify_row(e.y)
        if item:
            self.char_tree.selection_set(item)
            self.right_click_menu.post(e.x_root, e.y_root)
            name = self.char_tree.item(item, "values")[0]
            char_class = self.char_tree.item(item, "values")[1]
            self.right_click_menu.entryconfig("Edit", command=lambda: self.menu_item_right_click("Edit", name, '', ''))
            self.right_click_menu.entryconfig("Delete", command=lambda: self.menu_item_right_click("Delete", name, '', ''))
            self.right_click_menu.entryconfig("Open Inventory", command=lambda: self.menu_item_right_click("Open Inventory", name, '', ''))
            self.right_click_menu.entryconfig("Parse Inventory File", command=lambda: self.menu_item_right_click("Parse Inventory File", name, '', self.data.eq_dir))
            self.right_click_menu.entryconfig("Copy UI", command=lambda c=char_class: self.menu_item_right_click("Copy UI", name, char_class, self.data.eq_dir))
            self.right_click_menu.entryconfig("Get Camp Location", command=lambda : self.menu_item_right_click("Get Camp Location", name, '', self.data.eq_dir))
            self.right_click_menu.entryconfig("Missing Spells", command=lambda : self.menu_item_right_click("Missing Spells", name, char_class, self.data.eq_dir))

    def menu_item_right_click(self, option, name, char_class):
        if option == 'Edit':
            self.edit_character_window(name)
            
        elif option == 'Delete':
            self.delete_character(name)
            
        elif option == 'Open Inventory':
            inventory.inventory_window(name, inventory_window_open=False, inventory_array=self.data.inventory_array, characters_array=self.data.characters_array, root=self.main_window_instance.root)
            
        elif option == 'Parse Inventory File':
            self.create_inventory(name)
            
        elif option == 'Copy UI':
            self.copy_ui(char_class, name)
        
        elif option == 'Get Camp Location':
            mymodules.get_camp_location(self.main_window_instance.my_tree, self.main_window_instance.inputSearch, self.data.characters_array, self.main_window_instance.selected_class, name)

        elif option == 'Missing Spells':
            spells.missing_spells_window(self.data.characters_array, self.main_window_instance.root, name)


    def copy_ui(self, char_class, name):
        print('char_class', char_class)
        print('name', name)
    
        try:
            with open(f'./classUIs/UI_{char_class}_P1999PVP.ini', 'r') as file:
                ui_file = file.read()
                print('test ui 1')
            with open(f'{self.data.eq_dir}/UI_{name}_P1999PVP.ini', 'w') as file:
                file.write(ui_file)
                print('test ui 2')
            with open(f'./classUIs/{char_class}_P1999PVP.ini', 'r') as file:
                ui_file2 = file.read()
                print('test ui 3')
            with open(f'{self.data.eq_dir}/{name}_P1999PVP.ini', 'w') as file:
                file.write(ui_file2)
                print('test ui 4')
            print('UI Copy successful?')
        except FileNotFoundError as e:
            print(f'File not found: {e}')
        except PermissionError as e:
            print(f'Permission error: {e}')
        except Exception as e:
            print(f'An error occurred: {e}')
# Edit and Create are bundles into the create char and edit char methods
class CharacterMethods:
    def __innit__(self, data_instance, file_menu_instance, main_window_instance):
        self.data = data_instance
        self.file_menu_instance = file_menu_instance
        self.main_window_instance = main_window_instance
        pass

    def create_new_character_window(self):
        
        if self.data.new_char_window_open:
            return
        self.data.new_char_window_open = True

        self.new_char_window = Toplevel(self.main_window_instance.root)
        self.new_char_window.title("New Character")
        self.labels = ['Name', 'Class', 'Account', 'Password', 'EmuAccount', 'EmuPassword', 'Server', 'Location']
        self.entry_widgets = {}

        for label_text in self.labels:
            label = Label(self.new_char_window, text=label_text)
            label.grid(row=self.labels.index(label_text), column=0, padx=10, pady=5, sticky="w")

            self.entry_widgets[label_text] = Entry(self.new_char_window, width=30)
            self.entry_widgets[label_text].grid(row=self.labels.index(label_text), column=1, padx=10, pady=5, sticky="w")

        def create_new_character_button(self):
            
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
            character_data = {label: self.entry_widgets[label].get() for label in self.labels}
            if character_data['Class'] == 'Magician':
                character_data['Class'] = 'Mage'
            if character_data['Class'] == 'Shadowknight':
                character_data['Class'] = 'Shadow Knight'
            self.insert_new_character(character_data)
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
            self.data.new_char_window_open = False
            # Change value back after SQL insert
            character_data['Class'] = char_class_name
            self.new_char_window.destroy()

        def close_new_char_window(self):
            self.data.new_char_window_open = False
            self.new_char_window.destroy()

        create_button = Button(self.new_char_window, text="Create Character", command=create_new_character_button)
        create_button.grid(row=len(self.labels), columnspan=2, pady=10)
        self.new_char_window.protocol("WM_DELETE_WINDOW", close_new_char_window)
    # Is this is the right scope? We used to have it indented to the right
    def insert_new_character(self, character_data):
        iids = self.main_window_instance.char_tree.get_children()
        integers = [int(iid) for iid in iids]
        if integers:
            max_counter = max(integers)
            max_counter += 1
        else:
            max_counter = 0
        print('newchartest')
        print(character_data)
        self.data.characters_array.append(character_data)
        self.main_window_instance.char_tree.insert(parent='', index='end', iid=max_counter, text="", values=(
                character_data['Name'], character_data['Class'], character_data['Account'], character_data['Password'],
                character_data['EmuAccount'], character_data['EmuPassword'], character_data['Server'], character_data['Location']))
        
    def edit_character_window(self, name):
        
        old_name = name
        if self.data.edit_char_window_open:
            return
        self.data.edit_char_window_open = True

        edit_char_window = Toplevel(self.main_window_instance.root)
        edit_char_window.title("Edit Character")
        labels = ['Name', 'Class', 'Account', 'Password', 'EmuAccount', 'EmuPassword', 'Server', 'Location']
        entry_widgets = {}

        character_to_edit = None
        for character in self.data.characters_array:
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

        def edit_character_button(self, character):
            
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

            self.data.edit_char_window_open = False
            # Change value back after SQL insert
            character_data['Class'] = char_class_name
            mymodules.query_characters_array(self.data.characters_array, 'e', self.data.selected_class.get(), self.main_window_instance.my_tree, self.main_window_instance.inputSearch)
            edit_char_window.destroy()

        def close_edit_char_window():
            global edit_char_window_open
            edit_char_window_open = False
            edit_char_window.destroy()
        
        def query_characters_array(self, event):
            search_input_text = self.main_window_instance.inputSearch.get().lower()
            if self.main_window_instance.selected_class == 'All':
                filtered_characters = [char for char in self.data.characters_array if search_input_text in char['Name'].lower()]
            else:
                filtered_characters = [char for char in self.data.characters_array if char['Class'] == self.main_window_instance.selected_class and search_input_text in char['Name'].lower()]
            
            for item in self.main_window_instance.tree.get_children():
                self.main_window_instance.tree.delete(item)

            counter = 0
            for char in filtered_characters:
                self.main_window_instance.tree.insert(parent='', index='end', iid=counter, text="", values=(
                    char['Name'], char['Class'], char['Account'], char['Password'],
                    char['EmuAccount'], char['EmuPassword'], char['Server'], char['Location']))
                counter += 1
            sort_column("Name", False, self.main_window_instance.tree)
            return
        
        create_button = Button(edit_char_window, text="Edit Character", command=lambda: edit_character_button(character))
        create_button.grid(row=len(labels), columnspan=2, pady=10)
        edit_char_window.protocol("WM_DELETE_WINDOW", close_edit_char_window)

    def get_camp_location(self, name='All'):
        # Define the regex pattern for matching zone information
        regex = r"^.{27}There (?:is|are) \d+ player(?:s?) in (?!EverQuest)(\D+).$"
        char_names = []
        zone_char_pairs = []
        lines_parsed_per_char = []
        if name == 'All':
            char_names = [character['Name'] for character in self.data.characters_array]
        else:
            char_names = [character['Name'] for character in self.data.characters_array if character['Name'] == name]

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
            log_file_path = f'{self.data.eq_dir}/Logs/eqlog_{char_name}_P1999PVP.txt'
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
                                for character in self.data.characters_array:
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

    def delete_all_characters(self):
        database = "./stables.db"
        conn = self.create_connection(database)
        c = conn.cursor()
        
        try:
            c.execute("DELETE FROM characters")
            conn.commit()
            print("All rows deleted from the 'characters' table.")
        except Error as e:
            print(e)
        finally:
            conn.close()

    def fetch_all_characters(self):
        conn = self.create_connection("./stables.db")
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

            self.data.characters_array.append(row_object)
        # filtered_characters = copy.deepcopy(characters_array)
        self.fill_table_with_characters_array(self)
        conn.close()
        # print(lines_parsed_per_char)
    def fill_table_with_characters_array(self):
        for item in self.main_window_instance.char_tree.get_children():
            self.main_window_instance.char_tree.delete(item)
        counter = 0
        # iterate over 'characters_array' and fill table
        for character in self.data.characters_array:
            self.main_window_instance.char_tree.insert(parent='', index='end', iid = counter, text="", values=(character['Name'], character['Class'], character['Account'], character['Password'], character['EmuAccount'], character['EmuPassword'], character['Server'], character['Location']))
            counter += 1
        return
# Can pulldown menu inner functions be taken down a scope?
# Move char window to Characters()
class FileMenuMethods:
    def __init__(self, data_instance, main_window_instance):
        self.data = data_instance
        self.main_window_instance = main_window_instance

    def eq_directory(self):
        if self.data.eq_dir_window_open:
            return
        self.data.eq_dir_window_open = True
        self.eq_dir_window = Toplevel(self.data.root)
        self.eq_dir_window.title("Set EQ Directory")
        self.eq_dir_window.grid_rowconfigure(1, weight=1)
        self.eq_dir_window.grid_columnconfigure(0, weight=1)
        self.eq_dir_frame = LabelFrame(self.eq_dir_window, text="Please Enter EQ Directory")
        self.eq_dir_frame.grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.eq_dir_input = Entry(self.eq_dir_frame, width=50, bd=5, font=('Ariel', 15))
        self.eq_dir_input.insert(0, self.data.eq_dir)
        self.eq_dir_input.grid(row=0, column=0, padx=5, pady=5)
        
    def set_eq_dir(self):
        conn = mymodules.create_connection('./stables.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM eqDir")
        row_count = c.fetchone()[0]

        if row_count == 0:
            c.execute("""INSERT INTO eqDir (eqDir) VALUES (?)""", (self.eq_dir_input.get(),))
        else:
            c.execute("""UPDATE eqDir SET eqDir = ?""", (self.eq_dir_input.get(),))

        self.data.eq_dir = self.eq_dir_input.get()
        conn.commit()
        conn.close()
            
    def close_eq_dir_window(self):
        self.data.eq_dir_window_open = False
        self.set_eq_dir()
        print(self.data.eq_dir)
        self.eq_dir_window.destroy()

        ok_button = Button(self.eq_dir_window, text="OK", command=lambda: self.close_eq_dir_window())
        ok_button.grid(row=1, columnspan=2, pady=10)
        self.eq_dir_window.protocol("WM_DELETE_WINDOW", self.close_eq_dir_window)
        self.eq_dir_input.bind("<Return>", lambda event: self.close_eq_dir_window())

class InventoryWindow:
    def __innit__(self, data_instance, main_window_instance):
        self.data = data_instance
        self.main_window_instance = main_window_instance
        setup_inventory_window()
    # Could refactor some of this to INNIT, some of it to 'create_inventory_window()' etc. Will come back to this...
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

class InventoryMethods:
    def __init__(self, data_instance, main_window_instance):
        self.data = data_instance
        self.main_window_instance = main_window_instance

    def create_inventory(self, name):
        self.delete_inventory_db(name)
        please_wait_window, log_text = self.show_please_wait_window()
        self.main_window_instance.root.update()
        char_names = []
        # Get list of char_names
        if name == 'All':
            char_names = [char['Name'] for char in self.data.characters_array]
        else:
            char_names = [char['Name'] for char in self.data.characters_array if char['Name'] == name]
        char_names.sort()
        # Parse the eq_dir for the files
        conn = mymodules.create_connection('./stables.db')
        c = conn.cursor()
        count = 0
        try:
            for char in char_names:
                char_inventory_array = []
                file_paths = [f'{self.data.eq_dir}/{char}', f'{self.data.eq_dir}/{char}.txt']
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
                                        line[1] = 'Piece of a medallion (Burnished Wooden Stave)'
                                    if line[2] == '19959':
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
        
    def delete_inventory_db(self, name):
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

    def delete_character(self, name):
        try:
            # perform query to delete item
            conn = mymodules.create_connection("./stables.db")
            c = conn.cursor()
            c.execute("""DELETE FROM Characters WHERE charName = ? """, (name,))
            conn.commit()
            conn.close()
            characters_array = [char for char in characters_array if char['Name'] != name]
            selected_item = self.main_window_instance.my_tree.selection()  # Get the selected item(s)
            for item in selected_item:
                self.main_window_instance.my_tree.delete(item)  # Delete the selected item(s)
        except Error as e:
            print('Char Delete Query Failed!')
            print(e)
        return
    
    def show_please_wait_window(self):
        self.please_wait_window = Toplevel(self.main_window_instance.root)
        self.please_wait_window.title("Please Wait...")
        self.label = Label(self.please_wait_window, text="Parsing/writing, please wait...", padx=20, pady=20)
        self.label.pack()

        log_text = Text(self.please_wait_window, wrap=WORD, width=50, height=10)
        log_text.pack()

        return self.please_wait_window, log_text
    
class SpellsMethods:
    def __innit__(self, data_instance, main_window_instance):
        self.data = data_instance
        self.main_window_instance = main_window_instance

    def delete_spells_db(eq_dir, name):
        conn = mymodules.create_connection('./stables.db')
        c = conn.cursor()
        c.execute("""DELETE FROM classSpells""")
        c.execute("""DELETE FROM spellbooks""")
        c.execute("""DELETE FROM missingSpells""")
        conn.commit()
        conn.close()
        print('Entire Spells DB Deleted.')

    def query_missing_spells():
        conn = mymodules.create_connection('./stables.db')
        c = conn.cursor()
        c.execute("""SELECT * FROM missingSpells WHERE charName = 'Grixus'""")
        res = c.fetchall()
        print('res')
        print(res)
    
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

class SpellsWindow:
    def __innit__(self, data_instance, main_window_instance):
        self.data = data_instance
        self.main_window_instance = main_window_instance
        create_spells_window()

    def missing_spells_window(self, name='All'):

        if self.data.missing_spells_window_open:
            return
        self.data.missing_spells_window_open = True
        self.data.missing_spells_array = []

        def fill_table_with_missing_spells_array(self):
            
            self.missing_spells_tree.delete(*self.missing_spells_tree.get_children())
            counter = 0
            for spell in self.data.missing_spells_array:
                self.missing_spells_tree.insert(parent='', index='end', iid=counter, values=(spell[0], spell[2], spell[1]))
                counter += 1

        # Why do we need 'missing_spells_array'?
        def query_missing_spells(self, char_name):
            
            self.data.missing_spells_array = []
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
                self.spells_window.destroy()
                messagebox.showinfo("No SpellBook Found", "No 'missing spells' book found.")
                return   
            
            fill_table_with_missing_spells_array(missing_spells)
            
        def delete_missing_spells_tree(self):
            for item in self.missing_spells_tree.get_children():
                self.missing_spells_tree.delete(item)
                print('row deleted from tree')

        def fetch_missing_spells(self, name):
            conn = mymodules.create_connection('./stables.db')
            c = conn.cursor()
            if name == 'All':
                c.execute("""SELECT * FROM missingSpells""")
                self.data.missing_spells_array = c.fetchall()
            else:
                c.execute("""SELECT * FROM missingSpells WHERE charName = ? """, (name,))
                self.data.missing_spells_array = c.fetchall()
            print(self.data.missing_spells_array)

        # Get char names
        char_list = fetch_missing_spells_char_names()

        self.spells_window = Toplevel(self.main_window_instance.root)
        self.spells_window.title("Missing Spells")
        # Config row and col heights:
        self.spells_window.grid_rowconfigure(1, weight=1)
        self.spells_window.grid_columnconfigure(0, weight=1)
        # Create scrollbar for Treeview
        self.spells_window_scrollbar = Scrollbar(self.spells_window, orient="vertical")
        self.spells_window_scrollbar.grid(row=0, column=1, sticky="ns")
        # Create the Treeview widget
        self.missing_spells_tree = ttk.Treeview(self.spells_window)
        self.missing_spells_tree['columns'] = ('Char Name', 'Spell Name', 'Level')
        self.missing_spells_tree.grid(row=0, column=0, sticky="nsew")
        # Config Scrollbar
        self.spells_window_scrollbar.configure(command=self.missing_spells_tree.yview)
        self.missing_spells_tree.configure(yscrollcommand=self.spells_window_scrollbar.set)

        self.spells_window.rowconfigure(0, weight=1)
        self.spells_window.columnconfigure(0, weight=1)
        # Cols
        self.missing_spells_tree.column('#0', width=0, stretch=NO)
        self.missing_spells_tree.column('Char Name')
        self.missing_spells_tree.column('Spell Name')
        self.missing_spells_tree.column('Level')
        # Headings
        self.missing_spells_tree.heading('Char Name', text='Char Name')
        self.missing_spells_tree.heading('Spell Name', text='Spell Name')
        self.missing_spells_tree.heading('Level', text='Level')
        # Select Char Frame
        select_char_frame = LabelFrame(self.spells_window, text="Select Character")
        select_char_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        select_char_label = Label(select_char_frame, text="SELECT CHAR:", anchor="w")
        select_char_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        selected_char = StringVar()
        select_char_pulldown = ttk.Combobox(select_char_frame, textvariable=selected_char, values=char_list, state="readonly")
        select_char_pulldown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        selected_char.set('ALL')

        def selected_character_changed(self, *args):
            
            self.data.missing_spells_array = []
            name = selected_char.get()
            query_missing_spells(name, '')

        def close_spells_window(self):
            
            self.data.missing_spells_window_open = False
            self.data.missing_spells_array = []
            self.spells_window.destroy()

        self.spells_window.protocol("WM_DELETE_WINDOW", lambda event=None: close_spells_window(self.missing_spells_window_open, self.data.missing_spells_array))
        self.select_char_pulldown.bind("<<ComboboxSelected>>", lambda event, array=self.data.missing_spells_array: selected_character_changed(self.data.missing_spells_array))

    
        query_missing_spells(name, self.data.missing_spells_array)
        

        def create_all_spells_dbs(self, name):
            delete_all_spell_tables()
            create_character_spellbooks(self.data.characters_array, 'All', self.data.eq_dir)
            create_class_spells_db()
            create_missing_spells_db(self.data.characters_array, self.data.eq_dir, name)

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

class MiscMethods:
    def __innit__(self, data_instance, main_window_instance, inventory_window_instance, spells_window_instance)
        self.data = data_instance
        self.main_window_instance = main_window_instance
        self.inventory_window_instance = inventory_window_instance
        self.spells_window_instance = spells_window_instance

    def custom_sort(self, col, reverse, tree):
        data = [(tree.set(item, col) ,item)for item in tree.get_children('')]
        data.sort(reverse=reverse)
        for index, (val, item) in enumerate(data):
            tree.move(item, '', index)
        tree.heading(col, command=lambda: self.sort_column(col, not reverse, tree))

    def sort_column(self, col, reverse, tree):
        tree.heading(col, command=lambda: self.custom_sort(col, reverse, tree))
        self.custom_sort(col, reverse, tree)

    def import_json_db(self):
        json_db = None
        conn = self.create_connection("./stables.db")
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

    def exit_app(root):
        root.quit()

    def create_table(self, conn, create_table_sql):
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

        conn = self.create_connection("./stables.db")
        # c = conn.cursor()
        if conn is not None:
            self.create_table(conn, sql_create_characters_table)
            self.create_table(conn, sql_create_characterClasses_table)
            self.create_table(conn, sql_create_eqDir_table)
            self.create_table(conn, sql_create_classSpells_table)
            self.create_table(conn, sql_create_spellbooks_table)
            self.create_table(conn, sql_create_inventory_table)
            self.create_table(conn, sql_create_missingspells_table)
            
        conn.close()
    
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn
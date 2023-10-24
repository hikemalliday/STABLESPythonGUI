from tkinter import *
from tkinter import ttk
import sqlite3
from sqlite3 import Error
from tkinter import Menu
import json
import os
from tkinter import scrolledtext
import re

from tkinter import messagebox

import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import pygtail
from PIL import ImageGrab


class PlaceHolderMethods:
    def row_right_click(self, e):
        print('test1')
        pass
    def create_new_character_window(self):
        print('test2')
        pass
    def eq_directory(self):
        print('test3')
        pass
    def create_inventory(self, none):
        print('test4')
        pass
    def delete_inventory_db(self, none):
        print('test5')
        pass
    def get_camp_location(self, one, two, three, four):
        print('test6')
        pass
    def exit_app(self, none):
        print('test7')
        pass
    def inventory_window(self, none):
        print('test8')
        pass
    def create_all_spells_dbs(self, none):
        print('test9')
        pass
    def missing_spells_window(self, none):
        print('test10')
        pass
    def delete_spells_db(self, none):
        print('test11')
        pass
    def sort_column(self, one, two, three):
        print('test12')
        pass
    def yellow_text_window(self, none):
        print('test12')
        pass
    def parse_yellow_text(self, none):
        print('parse_yellow_text placeholder')
        pass
    def delete_yellow_text_db(self, none):
        pass
    def monitor_log_folder(self):
        pass
    def create_connection(self, none):
        pass
class InitialFetch:
    def __init__(self, data_instance, misc_methods_instance, character_methods_instance):
        self.data = data_instance
        self.misc_methods_instance = misc_methods_instance
        self.character_methods_instance = character_methods_instance
        self.misc_methods_instance = misc_methods_instance
        self.misc_methods_instance.create_tables()
        self.misc_methods_instance.fetch_eq_dir()
        self.character_methods_instance.fetch_all_characters()
        
class MainData:
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
    yellow_text_array = []
    log_file_mod_times = {}
    log_folder_path = ''
    new_char_window_open = False
    edit_char_window_open = False
    inventory_window_open = False
    eq_dir_window_open = False
    yellow_text_window_open = False
    missing_spells_window_open = False
    modified_file_found = False
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
    def __init__(self, data_instance=None, file_menu_instance=None, right_click_methods_instance=None, inventory_methods_instance=None, character_methods_instance=None, misc_methods_instance=None, spells_methods_instance=None, inventory_window_instance=None, spells_window_instance=None, yellow_text_window_instance=None, yellow_text_methods_instance=None, yellow_text_watcher_instance=None, log_file_handler_instance=None):
        self.data = data_instance
        self.file_menu_instance = file_menu_instance
        self.right_click_methods_instance = right_click_methods_instance
        self.inventory_methods_instance = inventory_methods_instance
        self.character_methods_instance = character_methods_instance
        self.misc_methods_instance = misc_methods_instance
        self.spells_methods_instance = spells_methods_instance
        self.inventory_window_instance = inventory_window_instance
        self.spells_window_instance = spells_window_instance
        self.yellow_text_window_instance = yellow_text_window_instance
        self.yellow_text_methods_instance = yellow_text_methods_instance
        self.yellow_text_watcher_instance = yellow_text_watcher_instance
        self.log_file_handler_instance = log_file_handler_instance
        
    def setup_main_window(self):
       
        self.root = Tk()
        self.root.title('S T A B L E S')
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
        self.select_class_pulldown = OptionMenu(self.select_class_frame, self.selected_class, *self.data.class_options)
        self.select_class_pulldown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.right_click_menu = Menu(self.root, tearoff=0)
        self.right_click_menu.add_command(label = "Edit")
        self.right_click_menu.add_command(label = "Delete")
        self.right_click_menu.add_command(label = "Open Inventory")
        self.right_click_menu.add_command(label = "Parse Inventory File")
        self.right_click_menu.add_command(label = "Copy UI")
        self.right_click_menu.add_command(label = "Get Camp Location")
        self.right_click_menu.add_command(label = "Missing Spells")
        self.right_click_menu.add_command(label = "Open Yellow Text")
        
        
        self.create_menus()
        self.create_columns()
        self.create_headings()

        self.inputSearch.bind("<KeyRelease>", lambda event: self.character_methods_instance.query_characters_array(event))
        self.selected_class.trace("w", self.selected_class_changed)

    def create_menus(self):
        menu_bar = Menu(self.root)
        self.root.config(menu = menu_bar)
        # File
        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Character", command=lambda: self.character_methods_instance.create_new_character_window())
        file_menu.add_command(label="Set EQ dir", command=self.file_menu_instance.eq_directory)
        file_menu.add_command(label="Get All Camp Locations", command=lambda: self.character_methods_instance.get_camp_location(name='All'))
        file_menu.add_command(label="Exit", command=lambda: self.misc_methods_instance.exit_app(self.root))
        # Inventory
        inventory_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Inventory", menu=inventory_menu)
        inventory_menu.add_command(label="Open Inventory Reader", command=lambda: self.inventory_window_instance.inventory_window('All'))
        inventory_menu.add_command(label="Parse All Inventory Files", command=lambda: self.inventory_methods_instance.create_inventory('All'))
        inventory_menu.add_command(label="Delete Inventory DB", command=lambda: self.inventory_methods_instance.delete_inventory_db('All'))
        # Spells
        spells_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Spells", menu=spells_menu)
        spells_menu.add_command(label="Missing Spells Window", command=lambda: self.spells_window_instance.missing_spells_window('All'))
        spells_menu.add_command(label="Create Missing Spells DB", command=lambda: self.spells_methods_instance.create_all_spells_dbs('All'))
        spells_menu.add_command(label="Delete Spells DB", command=lambda: self.spells_methods_instance.delete_spells_db())
        # Yellow Text
        yellow_text_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Yellow Text", menu=yellow_text_menu)
        yellow_text_menu.add_command(label="Yellow Text Window", command=lambda: self.yellow_text_window_instance.yellow_text_window('All'))
        yellow_text_menu.add_command(label="Create Yellow Text DB", command=lambda: self.yellow_text_methods_instance.parse_yellow_text('All'))
        yellow_text_menu.add_command(label="Delete Yellow Text DB", command=lambda: self.yellow_text_methods_instance.delete_yellow_text_db('All'))
        yellow_text_menu.add_command(label="Monitor Log Files for Yellow Text Screenshots", command=lambda: self.yellow_text_watcher_instance.run())
        yellow_text_menu.add_command(label="Stop Monitor for Yellow Text", command=lambda: self.yellow_text_watcher_instance.stop_global())
    
    def create_columns(self):
        self.char_tree.column('#0', width=0, stretch=NO)
        self.char_tree.column('Name', anchor=W)
        self.char_tree.column('Class')
        self.char_tree.column('Account')
        self.char_tree.column('Password')
        self.char_tree.column('EmuAccount')
        self.char_tree.column('EmuPassword')
        self.char_tree.column('Server')
        self.char_tree.column('Location')

    def create_headings(self):
        self.char_tree.heading("#0", text="")
        self.char_tree.heading("Name", text="Name", command=lambda: self.misc_methods_instance.sort_column("Name", False, self.char_tree))
        self.char_tree.heading("Class", text="Class", command=lambda: self.misc_methods_instance.sort_column("Class", False, self.char_tree))
        self.char_tree.heading("Account", text="Account", command=lambda: self.misc_methods_instance.sort_column("Account", False, self.char_tree))
        self.char_tree.heading("Password", text="Password", command=lambda: self.misc_methods_instance.sort_column("Password", False, self.char_tree))
        self.char_tree.heading("EmuAccount", text="EmuAccount", command=lambda: self.misc_methods_instance.sort_column("EmuAccount", False, self.char_tree))
        self.char_tree.heading("EmuPassword", text="EmuPassword", command=lambda: self.misc_methods_instance.sort_column("EmuPassword", False, self.char_tree))
        self.char_tree.heading("Server", text="Server", command=lambda: self.misc_methods_instance.sort_column("Server", False))
        self.char_tree.heading("Location", text="Location", command=lambda: self.misc_methods_instance.sort_column("Location", False, self.char_tree))

    def row_right_click(self, e):
        
        item = self.char_tree.identify_row(e.y)
        if item:
            self.char_tree.selection_set(item)
            self.right_click_menu.post(e.x_root, e.y_root)
            name = self.char_tree.item(item, "values")[0]
            char_class = self.char_tree.item(item, "values")[1]
            self.right_click_menu.entryconfig("Edit", command=lambda: self.menu_item_right_click("Edit", name))
            self.right_click_menu.entryconfig("Delete", command=lambda: self.menu_item_right_click("Delete", name))
            self.right_click_menu.entryconfig("Open Inventory", command=lambda: self.menu_item_right_click("Open Inventory", name, ''))
            self.right_click_menu.entryconfig("Parse Inventory File", command=lambda: self.menu_item_right_click("Parse Inventory File", name, ''))
            self.right_click_menu.entryconfig("Copy UI", command=lambda c=char_class: self.menu_item_right_click("Copy UI", name, char_class))
            self.right_click_menu.entryconfig("Get Camp Location", command=lambda : self.menu_item_right_click("Get Camp Location", name, ''))
            self.right_click_menu.entryconfig("Missing Spells", command=lambda : self.menu_item_right_click("Missing Spells", name, char_class))
            self.right_click_menu.entryconfig("Open Yellow Text", command=lambda : self.menu_item_right_click("Open Yellow Text", name))
            
            
    def menu_item_right_click(self, option, name = 'All', char_class = ''):
        if option == 'Edit':
            self.character_methods_instance.edit_character_window(name)
            
        elif option == 'Delete':
            self.character_methods_instance.delete_character(name)
            
        elif option == 'Open Inventory':
            
            self.inventory_window_instance.inventory_window(name)
            
        elif option == 'Parse Inventory File':
            self.inventory_methods_instance.create_inventory(name)
            
        elif option == 'Copy UI':
            self.right_click_methods_instance.copy_ui(char_class, name)
        
        elif option == 'Get Camp Location':
            self.character_methods_instance.get_camp_location(name)

        elif option == 'Missing Spells':
            self.spells_window_instance.missing_spells_window(name)

        elif option == 'Open Yellow Text':
            self.yellow_text_window_instance.yellow_text_window(name)

        elif option == 'Parse Yellow Text':
            self.yellow_text_methods_instance.parse_yellow_text(name)

    def selected_class_changed(self, *args):
        self.character_methods_instance.query_characters_array(self.selected_class.get())
# Break up into other classes
class RightClickMethods:
    def __init__(self, data_instance, main_window_instance = [], inventory_methods_instance = [], spells_methods_instance = [], character_method_instance = []):
        self.data = data_instance
        self.main_window_instance = main_window_instance
        self.inventory_methods_instance = inventory_methods_instance
        self.spells_methods_instance = spells_methods_instance
        self.character_method_instance = character_method_instance

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

class CharacterMethods:
    def __init__(self, data_instance, file_menu_instance, main_window_instance, misc_methods_instance):
        self.data = data_instance
        self.file_menu_instance = file_menu_instance
        self.main_window_instance = main_window_instance
        self.misc_methods_instance = misc_methods_instance
        pass
        # Depends on: main_window.root,
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

        create_button = Button(self.new_char_window, text="Create Character", command=self.create_new_character_button)
        create_button.grid(row=len(self.labels), columnspan=2, pady=10)
        self.new_char_window.protocol("WM_DELETE_WINDOW", self.close_new_char_window)

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
        conn = self.misc_methods_instance.create_connection('./stables.db')
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
        
    # Is this is the right scope? We used to have it indented to the right
    def insert_new_character(self, character_data):
        iids = self.main_window_instance.char_tree.get_children()
        integers = [int(iid) for iid in iids]
        if integers:
            max_counter = max(integers)
            max_counter += 1
        else:
            max_counter = 0
        
        self.data.characters_array.append(character_data)
        self.main_window_instance.char_tree.insert(parent='', index='end', iid=max_counter, text="", values=(
                character_data['Name'], character_data['Class'], character_data['Account'], character_data['Password'],
                character_data['EmuAccount'], character_data['EmuPassword'], character_data['Server'], character_data['Location']))
        
    def edit_character_window(self, name):
        
        self.old_name = name
        if self.data.edit_char_window_open:
            return
        self.data.edit_char_window_open = True

        self.edit_char_window = Toplevel(self.main_window_instance.root)
        self.edit_char_window.title("Edit Character")
        self.labels = ['Name', 'Class', 'Account', 'Password', 'EmuAccount', 'EmuPassword', 'Server', 'Location']
        self.entry_widgets = {}

        character_to_edit = None
        for character in self.data.characters_array:
            if character['Name'] == name:
                character_to_edit = character
                break
        if character_to_edit is None:
            print(f"Character with name '{name}' not found.")
            return

        for label_text in self.labels:
            label = Label(self.edit_char_window, text=label_text)
            label.grid(row=self.labels.index(label_text), column=0, padx=10, pady=5, sticky="w")

            self.entry_widgets[label_text] = Entry(self.edit_char_window, width=30)
            
            if character_to_edit.get(label_text, '') == None:
                character_to_edit[label_text] = 'None'
            self.entry_widgets[label_text].insert(0, character_to_edit.get(label_text, ''))
            self.entry_widgets[label_text].grid(row=self.labels.index(label_text), column=1, padx=10, pady=5, sticky="w")
        
        create_button = Button(self.edit_char_window, text="Edit Character", command=lambda: self.edit_character_button(character))
        create_button.grid(row=len(self.labels), columnspan=2, pady=10)
        self.edit_char_window.protocol("WM_DELETE_WINDOW", self.close_edit_char_window)

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
        character_data = {label: self.entry_widgets[label].get() for label in self.labels}
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
    
        conn = self.misc_methods_instance.create_connection('./stables.db')
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
                    self.old_name,
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
        self.query_characters_array('e')
        self.edit_char_window.destroy()

    def delete_character(self, name):
        try:
            # perform query to delete item
            conn = self.misc_methods_instance.create_connection("./stables.db")
            c = conn.cursor()
            c.execute("""DELETE FROM Characters WHERE charName = ? """, (name,))
            conn.commit()
            conn.close()
            self.data.characters_array = [char for char in self.data.characters_array if char['Name'] != name]
            selected_item = self.main_window_instance.char_tree.selection()  # Get the selected item(s)
            for item in selected_item:
                self.main_window_instance.char_tree.delete(item)  # Delete the selected item(s)
        except Error as e:
            print('Char Delete Query Failed!')
            print(e)
        return

    def close_edit_char_window(self):
        
        self.data.edit_char_window_open = False
        self.edit_char_window.destroy()
        
    def query_characters_array(self, event):
       
        search_input_text = self.main_window_instance.inputSearch.get().lower()
        
        if self.main_window_instance.selected_class.get() == 'All':
            
            filtered_characters = [char for char in self.data.characters_array if search_input_text in char['Name'].lower()]
        else:
            filtered_characters = [char for char in self.data.characters_array if char['Class'] == self.main_window_instance.selected_class.get() and search_input_text in char['Name'].lower()]
        
        for item in self.main_window_instance.char_tree.get_children():
            self.main_window_instance.char_tree.delete(item)
        
        counter = 0
        for char in filtered_characters:
            
            self.main_window_instance.char_tree.insert(parent='', index='end', iid=counter, text="", values=(
                char['Name'], char['Class'], char['Account'], char['Password'],
                char['EmuAccount'], char['EmuPassword'], char['Server'], char['Location']))
            counter += 1
        self.misc_methods_instance.sort_column("Name", False, self.main_window_instance.char_tree)
        return
        
    

    def get_camp_location(self, name='All'):
        # Define the regex pattern for matching zone information
        # regex = r"^.{27}There (?:is|are) \d+ player(?:s?) in (?!EverQuest)(\D+).$"
        regex = r"\[.*\] You have entered (.*?\w+)\."
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

        conn = self.misc_methods_instance.create_connection('./stables.db')
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
        conn = self.misc_methods_instance.create_connection("./stables.db")
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
        self.fill_table_with_characters_array()
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
# Move char window to Characters()
class FileMenuMethods:
    def __init__(self, data_instance, main_window_instance, misc_methods_instance):
        self.data = data_instance
        self.main_window_instance = main_window_instance
        self.misc_methods_instance = misc_methods_instance

    def eq_directory(self):
        if self.data.eq_dir_window_open:
            return
        self.data.eq_dir_window_open = True
        self.eq_dir_window = Toplevel(self.main_window_instance.root)
        self.eq_dir_window.title("Set EQ Directory")
        self.eq_dir_window.grid_rowconfigure(1, weight=1)
        self.eq_dir_window.grid_columnconfigure(0, weight=1)
        self.eq_dir_frame = LabelFrame(self.eq_dir_window, text="Please Enter EQ Directory")
        self.eq_dir_frame.grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.eq_dir_input = Entry(self.eq_dir_frame, width=50, bd=5, font=('Ariel', 15))
        self.eq_dir_input.insert(0, self.data.eq_dir)
        self.eq_dir_input.grid(row=0, column=0, padx=5, pady=5)

        ok_button = Button(self.eq_dir_window, text="OK", command=lambda: self.close_eq_dir_window())
        ok_button.grid(row=1, columnspan=2, pady=10)
        self.eq_dir_window.protocol("WM_DELETE_WINDOW", self.close_eq_dir_window)
        self.eq_dir_input.bind("<Return>", lambda event: self.close_eq_dir_window())
        
    def set_eq_dir(self):
        conn = self.misc_methods_instance.create_connection('./stables.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM eqDir")
        row_count = c.fetchone()[0]

        if row_count == 0:
            
            c.execute("""INSERT INTO eqDir (eqDir) VALUES (?)""", (self.eq_dir_input.get(),))
        else:
            
            c.execute("""UPDATE eqDir SET eqDir = ?""", (self.eq_dir_input.get(),))

        c.execute("""SELECT * FROM eqDir""")
        res = c.fetchall()
        
        self.data.eq_dir = self.eq_dir_input.get()
        
        conn.commit()
        conn.close()
        
    def close_eq_dir_window(self):
        self.data.eq_dir_window_open = False
        self.set_eq_dir()
        print(self.data.eq_dir)
        self.eq_dir_window.destroy()

class InventoryWindow:
    def __init__(self, data_instance, main_window_instance, misc_methods_instance):
        self.data = data_instance
        self.main_window_instance = main_window_instance
        self.misc_methods_instance = misc_methods_instance
        
    def setup_inventory_window(self):
        self.char_list = self.fetch_inventory_char_names()
        self.inv_window = Toplevel(self.main_window_instance.root)
        self.inv_window.title("Inventory Reader")
        self.inv_window.grid_rowconfigure(1, weight=1)
        self.inv_window.grid_columnconfigure(0, weight=1)

        self.inv_tree = ttk.Treeview(self.inv_window)
        self.inv_tree['columns'] = ('Char Name', 'Item Name', 'Location', 'Item ID', 'Count')
        self.inv_tree.grid(row=1, column=0, columnspan=8, padx=10, pady=10, sticky="nsew")
        self.inv_search = Entry(self.inv_window, width=100, bd=5, font = ('Arial Bold', 15))
        self.inv_search.grid(row=0, column=0, columnspan=7, padx=5, pady=5)
        self.inv_search.bind("<Return>", lambda event: self.query_char_inventory(self.selected_char.get(), self.inv_search.get()))
        self.inv_tree_scrollbar = Scrollbar(self.inv_window, orient="vertical", command=self.inv_tree.yview)
        self.inv_tree_scrollbar.grid(row=1, column=1, sticky="ns")
        self.inv_tree.configure(yscrollcommand=self.inv_tree_scrollbar.set)
        # Cols
        self.inv_tree.column('#0', width=0, stretch=NO)
        self.inv_tree.column('Char Name')
        self.inv_tree.column('Item Name')
        self.inv_tree.column('Location')
        self.inv_tree.column('Item ID')
        self.inv_tree.column('Count')
        # Headings
        self.inv_tree.heading("#0", text='', )
        self.inv_tree.heading("Char Name", text='Char Name', command=lambda: self.misc_methods_instance.sort_column("Char Name", False, self.inv_tree))
        self.inv_tree.heading("Item Name", text='Item Name', command=lambda: self.misc_methods_instance.sort_column("Item Name", False, self.inv_tree))
        self.inv_tree.heading("Location", text='Location', command=lambda: self.misc_methods_instance.sort_column("Location", False, self.inv_tree))
        self.inv_tree.heading("Item ID", text='Item ID', command=lambda: self.misc_methods_instance.sort_column("Item ID", False, self.inv_tree))
        self.inv_tree.heading("Count", text='Count', command=lambda: self.misc_methods_instance.sort_column("Count", False, self.inv_tree))
        # Select Char Frame
        self.select_char_frame = LabelFrame(self.inv_window, text="Select Character")
        self.select_char_frame.grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.select_char_label = Label(self.select_char_frame, text="SELECT CHAR:", anchor="w")
        self.select_char_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.selected_char = StringVar()
        self.select_char_pulldown = ttk.Combobox(self.select_char_frame, textvariable=self.selected_char, values=self.char_list, state="readonly")
        self.select_char_pulldown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.selected_char.set('ALL')

        self.inv_window.protocol("WM_DELETE_WINDOW", lambda event=None: self.close_inventory_window())
        self.select_char_pulldown.bind("<<ComboboxSelected>>", lambda event, *, tree=self.inv_tree, inventory_array=self.data.inventory_array, characters_array=self.data.characters_array: self.selected_inventory_changed())
        pass
    # Could refactor some of this to INNIT, some of it to 'create_inventory_window()' etc. Will come back to this...
    def inventory_window(self, name):
        if self.data.inventory_window_open:
            return
        self.data.inventory_window_open = True
        self.setup_inventory_window()
        if self.query_char_inventory(name, '') == False:
            self.close_inventory_window()
            return messagebox.showinfo("No Inventory Found", "No inventory was found for the selected character.")

    def fill_table_with_inventory_array(self, inventory_array):
        self.inv_tree.delete(*self.inv_tree.get_children())
        counter = 0
        for item in inventory_array:
            self.inv_tree.insert(parent='', index='end', iid = counter, text="", values=(item[0], item[2], item[1], item[3], item[4]))
            counter += 1

    def query_char_inventory(self, name, item_name = ''):
        # if item_name is None:
        #     item_name = ''
        inventory_array = []
        conn = self.misc_methods_instance.create_connection('./stables.db')
        c = conn.cursor()
        self.selected_char.set(name)
        
        if name == 'All':
            c.execute("""SELECT * FROM inventory WHERE itemName LIKE ?""", ('%' + item_name + '%',))
        else:
            c.execute("""SELECT * FROM inventory WHERE charName = ? AND itemName LIKE ?""", (name, '%' + item_name + '%'))
        
        char_inventory = c.fetchall()
        
        for item in char_inventory:
            inventory_array.append(item)
        conn.commit()
        conn.close()
        # If char doesnt have inventory, return False
        if len(inventory_array) == 0 and len(self.inv_tree.get_children()) == 0:
            if self.inv_window is not None and self.inv_window.winfo_exists():
                return False
        self.fill_table_with_inventory_array(inventory_array)
             
    def selected_inventory_changed(self):
        inventory_array = []
        name = self.selected_char.get()
        self.query_char_inventory(name, '')
        
        # This boolean tells us if the chose char's inventory is length of 0. If so, returns false and closes the window.
              
    def close_inventory_window(self):
        self.data.inventory_window_open = False
        self.data.inventory_array = []
        self.inv_window.destroy()
    
    def fetch_inventory_char_names(self):
        res = []
        conn = self.misc_methods_instance.create_connection('./stables.db')
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
    def __init__(self, data_instance, main_window_instance, misc_methods_instance):
        self.data = data_instance
        self.main_window_instance = main_window_instance
        self.misc_methods_instance = misc_methods_instance

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
        conn = self.misc_methods_instance.create_connection('./stables.db')
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
        conn = self.misc_methods_instance.create_connection('./stables.db')
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

    def show_please_wait_window(self):
        self.please_wait_window = Toplevel(self.main_window_instance.root)
        self.please_wait_window.title("Please Wait...")
        self.label = Label(self.please_wait_window, text="Parsing/writing, please wait...", padx=20, pady=20)
        self.label.pack()

        log_text = Text(self.please_wait_window, wrap=WORD, width=50, height=10)
        log_text.pack()

        return self.please_wait_window, log_text
    
class SpellsMethods:
    def __init__(self, data_instance, main_window_instance, misc_methods_instance, spells_window_instance):
        self.data = data_instance
        self.main_window_instance = main_window_instance
        self.misc_methods_instance = misc_methods_instance
        self.spells_window_instance = spells_window_instance

    def delete_spells_db(self):
        conn = self.misc_methods_instance.create_connection('./stables.db')
        c = conn.cursor()
        c.execute("""DELETE FROM classSpells""")
        c.execute("""DELETE FROM spellbooks""")
        c.execute("""DELETE FROM missingSpells""")
        conn.commit()
        conn.close()
        print('Entire Spells DB Deleted.')

    def query_missing_spells(self):
        conn = self.misc_methods_instance.create_connection('./stables.db')
        c = conn.cursor()
        c.execute("""SELECT * FROM missingSpells WHERE charName = 'Grixus'""")
        res = c.fetchall()
        print('res')
        print(res)
    
    def create_class_spells_db(self):
        class_spells = []
        for filename in os.listdir('./classSpells'):
                char_class = filename[:-4]
                with open(f'./classSpells/{filename}', 'r') as file:
                    for line in file:
                        line = line.strip().replace('\n', '').replace('\t', '').split(',')
                        line.insert(0, char_class)
                        class_spells.append(line)                
        # [charClass, spellLevel, spellName]
        conn = self.misc_methods_instance.create_connection('./stables.db')
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

    def create_character_spellbooks(self, name='All'):
        char_names = []
        spellbooks_list = []
        spellbooks_object = {}
        
        conn = self.misc_methods_instance.create_connection('./stables.db')
        c = conn.cursor()
        
        if name == 'All':
            char_names = [char['Name'] for char in self.data.characters_array]
            c.execute("""DELETE FROM spellbooks""")
            
        else:
            char_names = [name]
            c.execute("""DELETE FROM spellbooks WHERE charName = ?""", (name,))
        
        for char_name in char_names:
            try:
                with open(f'{self.data.eq_dir}/{char_name}spells', 'r') as spellbook: 
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
    
    def get_class_spells(self, char_class):
        # need to return an object that contains key: char_class, val: 2d list
        conn = self.misc_methods_instance.create_connection('./stables.db')
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
    
    def get_all_spell_tables(self):
        conn = self.misc_methods_instance.create_connection('./stables.db')
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

    def delete_all_spell_tables(self):
        conn = self.misc_methods_instance.create_connection('./stables.db')
        c = conn.cursor()
        c.execute("""DELETE FROM classSpells""")
        print('deleted db.classSpells')
        c.execute("""DELETE FROM spellbooks""")
        print('deleted db.spellbooks')
        c.execute("""DELETE FROM missingSpells""")
        print('deleted db.missingSpells')
        conn.commit()
        conn.close()

    def create_missing_spells_db(self, name='All'):
            
            characters_classes = []
            class_spells = {}
            missing_spells = []
            
            conn = self.misc_methods_instance.create_connection('./stables.db')
            c = conn.cursor()

            if name == 'All':
                characters_classes = {char['Name']: char['Class'] for char in self.data.characters_array}
                class_spells = self.get_class_spells('All')
                c.execute("""DELETE FROM missingSpells""")
            
            else:
                characters_classes = {char['Name']: char['Class'] for char in self.data.characters_array if char['Name'] == name}
                class_spells = self.get_class_spells(characters_classes[name])
                c.execute("""DELETE FROM missingSpells WHERE charName = ? """, (name,))
            conn.commit()
            conn.close()
            
            character_spellbooks = self.create_character_spellbooks(name)
            
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
            
            conn = self.misc_methods_instance.create_connection('./stables.db')
            c = conn.cursor()
            try:
                c.executemany("""INSERT INTO missingspells VALUES (?, ?, ?)""", (missing_spells))
            except Exception as e:
                print(e)
            conn.commit()
            conn.close()
            
            return missing_spells

    def fetch_missing_spells_char_names(self):
        res = []
        conn = self.misc_methods_instance.create_connection('./stables.db')
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

    def create_all_spells_dbs(self, name):
        self.delete_all_spell_tables()
        self.create_character_spellbooks('All')
        self.create_class_spells_db()
        self.create_missing_spells_db(name)

    def fetch_missing_spells(self, name):
        conn = self.misc_methods_instance.create_connection('./stables.db')
        c = conn.cursor()
        if name == 'All':
            c.execute("""SELECT * FROM missingSpells""")
            self.data.missing_spells_array = c.fetchall()
        else:
            c.execute("""SELECT * FROM missingSpells WHERE charName = ? """, (name,))
            self.data.missing_spells_array = c.fetchall()
        print(self.data.missing_spells_array)

    def query_missing_spells(self, char_name):
        
        self.data.missing_spells_array = []
        conn = self.misc_methods_instance.create_connection('./stables.db')
        c = conn.cursor()
        
        self.spells_window_instance.selected_char.set(char_name)
        if char_name == 'All':
            c.execute("""SELECT * FROM missingSpells""")
        else:
            c.execute("""SELECT * FROM missingSpells WHERE charName = ? """, (char_name,))

        self.data.missing_spells_array = c.fetchall()
        conn.commit()
        conn.close()
        
        if len(self.data.missing_spells_array) == 0:
            self.spells_window_instance.spells_window.destroy()
            messagebox.showinfo("No SpellBook Found", "No 'missing spells' book found.")
            return   
        
        self.spells_window_instance.fill_table_with_missing_spells_array()

    def selected_character_changed(self, *args):
        
        self.data.missing_spells_array = []
        name = self.spells_window_instance.selected_char.get()
        self.query_missing_spells(name)

class SpellsWindow:
    def __init__(self, data_instance, main_window_instance, spells_methods_instance, misc_methods_instance):
        self.data = data_instance
        self.main_window_instance = main_window_instance
        self.spells_methods_instance = spells_methods_instance
        self.misc_methods_instance = misc_methods_instance
            
    def missing_spells_window(self, name='All'):
        if self.data.missing_spells_window_open == True:
            return
        self.create_spells_window(name)
        self.data.missing_spells_window_open = True
        self.data.missing_spells_array = []

    def fill_table_with_missing_spells_array(self):
        self.missing_spells_tree.delete(*self.missing_spells_tree.get_children())
        counter = 0
        for spell in self.data.missing_spells_array:
            self.missing_spells_tree.insert(parent='', index='end', iid=counter, values=(spell[0], spell[2], spell[1]))
            counter += 1

    def delete_missing_spells_tree(self):
        for item in self.missing_spells_tree.get_children():
            self.missing_spells_tree.delete(item)
            print('row deleted from tree')

    def create_spells_window(self, name):
        # Get char names
        char_list = self.spells_methods_instance.fetch_missing_spells_char_names()

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
        self.select_char_frame = LabelFrame(self.spells_window, text="Select Character")
        self.select_char_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.select_char_label = Label(self.select_char_frame, text="SELECT CHAR:", anchor="w")
        self.select_char_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.selected_char = StringVar()
        self.select_char_pulldown = ttk.Combobox(self.select_char_frame, textvariable=self.selected_char, values=char_list, state="readonly")
        self.select_char_pulldown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.selected_char.set('ALL')

        self.spells_window.protocol("WM_DELETE_WINDOW", lambda event=None: self.close_spells_window())
        self.select_char_pulldown.bind("<<ComboboxSelected>>", lambda event, array=self.data.missing_spells_array: self.spells_methods_instance.selected_character_changed())

        self.spells_methods_instance.query_missing_spells(name)

    def close_spells_window(self):
        
        self.data.missing_spells_window_open = False
        self.data.missing_spells_array = []
        self.spells_window.destroy()

class YellowTextWindow:
    def __init__(self, data_instance, main_window_instance, file_menu_instance, right_click_methods_instance, misc_methods_instance):
        self.data = data_instance
        self.main_window_instance = main_window_instance
        self.file_menu_instance = file_menu_instance
        self.right_click_methods_instance = right_click_methods_instance
        self.misc_methods_instance = misc_methods_instance

    def setup_yellow_text_window(self):
        self.char_list = self.fetch_yellow_text_char_names()
        self.yellow_txt_win = Toplevel(self.main_window_instance.root)
        self.yellow_txt_win.title("Yellow Text")
        self.yellow_txt_win.grid_rowconfigure(1, weight=1)
        self.yellow_txt_win.grid_columnconfigure(0, weight=1)

        self.yellow_txt_tree = ttk.Treeview(self.yellow_txt_win)
        self.yellow_txt_tree['columns'] = ('Name', 'Opponent', 'Zone', 'Date')
        self.yellow_txt_tree.grid(row=1, column=0, columnspan=8, padx=10, pady=10, sticky="nsew")
        self.yt_search = Entry(self.yellow_txt_win, width=100, bd=5, font = ('Arial Bold', 15))
        self.yt_search.grid(row=0, column=0, columnspan=7, padx=5, pady=5)
        self.yt_search.bind("<Return>", lambda event: self.query_yellow_text_array(self.yt_search.get()))
        self.yellow_txt_tree_scrollbar = Scrollbar(self.yellow_txt_win, orient="vertical", command=self.yellow_txt_tree.yview)
        self.yellow_txt_tree_scrollbar.grid(row=1, column=1, sticky="ns")
        self.yellow_txt_tree.configure(yscrollcommand=self.yellow_txt_tree_scrollbar.set)
        # Cols
        self.yellow_txt_tree.column('#0', width=0, stretch=NO)
        self.yellow_txt_tree.column('Name')
        self.yellow_txt_tree.column('Opponent')
        self.yellow_txt_tree.column('Zone')
        self.yellow_txt_tree.column('Date')
        
        # Headings
        self.yellow_txt_tree.heading("#0", text='', )
        self.yellow_txt_tree.heading("Name", text='Name', command=lambda: self.misc_methods_instance.sort_column("Name", False, self.yellow_txt_tree))
        self.yellow_txt_tree.heading("Opponent", text='Opponent', command=lambda: self.misc_methods_instance.sort_column("Opponent", False, self.yellow_txt_tree))
        self.yellow_txt_tree.heading("Zone", text='Zone', command=lambda: self.misc_methods_instance.sort_column("Zone", False, self.yellow_txt_tree))
        self.yellow_txt_tree.heading("Date", text='Date', command=lambda: self.misc_methods_instance.sort_column("Date", False, self.yellow_txt_tree))
        
        # Select Char Frame
        self.select_char_frame = LabelFrame(self.yellow_txt_win, text="Select Character")
        self.select_char_frame.grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.select_char_label = Label(self.select_char_frame, text="SELECT CHAR:", anchor="w")
        self.select_char_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.selected_char = StringVar()
        self.select_char_pulldown = ttk.Combobox(self.select_char_frame, textvariable=self.selected_char, values=self.char_list, state="readonly")
        self.select_char_pulldown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.selected_char.set('ALL')

        self.yellow_txt_win.protocol("WM_DELETE_WINDOW", lambda event=None: self.close_yellow_text_window())
        self.select_char_pulldown.bind("<<ComboboxSelected>>", lambda event, *, tree=self.yellow_txt_tree, yellow_text_array=self.data.yellow_text_array, characters_array=self.data.characters_array: self.selected_character_changed())
        
    def yellow_text_window(self, name):
        if self.data.yellow_text_window_open == True:
            return
        self.data.yellow_text_window_open = True
        self.setup_yellow_text_window()
        if self.query_yellow_text(name) == False:
            self.close_yellow_text_window()
            return messagebox.showinfo("No Yellow Text Found", "No Yellow Text was found for the selected character.")
        pass

    def close_yellow_text_window(self):
        self.data.yellow_text_window_open = False
        self.yellow_txt_win.destroy()
        pass

    def query_yellow_text(self, name='All'):

        results = []
        conn = self.misc_methods_instance.create_connection('./stables.db')
        c = conn.cursor()
        self.selected_char.set(name)
        
        if name == 'All':
            c.execute("""SELECT * FROM yellowText""")
        else:
            c.execute("""SELECT * FROM yellowText WHERE charName = ? """, (name,))
        # look into how inventories are handlded, see if we are consistent here. Making a copy and storing it in 'data' allows us to avoid calling db querys when we want to query the yellow text db
        yellow_text = c.fetchall()
        self.data.yellow_text_array = yellow_text.copy()
        
        for item in yellow_text:
            results.append(item)
        conn.commit()
        conn.close()
        # If char doesnt have inventory, return False
        if len(results) == 0 and len(self.yellow_txt_tree.get_children()) == 0:
            if self.yellow_txt_win is not None and self.yellow_txt_win.winfo_exists():
                return False
        self.fill_table_with_yellow_text_array(results)
        
    def fill_table_with_yellow_text_array(self, yellow_text_array):
        self.yellow_txt_tree.delete(*self.yellow_txt_tree.get_children())
        counter = 0
        for item in yellow_text_array:
            self.yellow_txt_tree.insert(parent='', index='end', iid = counter, text="", values=(item[1], item[2], item[3], item[0]))
            counter += 1
        pass

    def fetch_yellow_text_char_names(self):
        res = []
        conn = self.misc_methods_instance.create_connection('./stables.db')
        c = conn.cursor()
        try:
            c.execute("""SELECT DISTINCT charName FROM yellowText""")
            char_names = c.fetchall()
            conn.commit()
            conn.close()
            for name in char_names:
                res.append(name[0])
            res.append('All')
            res.sort()
        except Exception as e:
            print(e)
            return
        return res

    def query_yellow_text_array(self, name):
        if name == 'All':
            yellow_text = self.data.yellow_text_array
        else:
            yellow_text = [yt for yt in self.data.yellow_text_array if name.lower() in yt[1].lower()]

        self.fill_table_with_yellow_text_array(yellow_text)
        
    def selected_character_changed(self, *args):
        
        name = self.selected_char.get()
        self.query_yellow_text_array(name)

class YellowTextMethods:
    def __init__(self, data_instance, main_window_instance, file_menu_instance, right_click_methods_instance, misc_methods_instance, yellow_text_window_instance):
        self.data = data_instance
        self.main_window_instance = main_window_instance
        self.file_menu_instance = file_menu_instance
        self.right_click_methods_instance = right_click_methods_instance
        self.misc_methods_instance = misc_methods_instance
        self.yellow_text_window_instance = yellow_text_window_instance

    def parse_yellow_text(self, name):
        counter = 0
        yellow_texts = []
        
        regex = r"\[(.*?)\] \[.*\] (\w+) <.*?> has been defeated by (\w+) <.*?> in ([^!]+)"
        yellow_texts = []
        char_names = []
        
        if name == 'All':
            self.delete_yellow_text_db('All')
            char_names = [char['Name'] for char in self.data.characters_array]
        else:
            self.delete_yellow_text_db(name)
            char_names = [char['Name'] for char in self.data.characters_array if char['Name'] == name]
        char_names.sort()

        popup = Toplevel()
        popup.title('Parsing Progress')
        text_widget = scrolledtext.ScrolledText(popup, wrap=WORD)
        text_widget.pack(fill=BOTH, expand=True)
        text_widget.insert(1.0, 'Parsing in progress, please wait until completion...\n')
        text_widget.update()

        for char_name in char_names:
            if char_name == 'All':
                continue
            log_file_path = f'{self.data.eq_dir}/Logs/eqlog_{char_name}_P1999PVP.txt'
            
            try:
                with open(log_file_path, 'r') as file:
                    lines = file.readlines()               
                    for line in lines:
                        match = re.match(regex, line)
                        if match:
                            counter += 1
                            date = match.group(1)
                            winner = match.group(2)
                            opponent = match.group(3)
                            zone = match.group(4)
                            text_widget.insert(1.0, f'YT Found: {line}\n')
                            text_widget.update()
                            yellow_texts.append([date, winner, opponent, zone])
            except Exception as e:
                print('test yt parse failed: ')
                print(e)
            
        conn = self.misc_methods_instance.create_connection('./stables.db')
        c = conn.cursor()
        for yellow_text in yellow_texts:
            text_widget.insert(1.0, f'Inserting YT:{yellow_text[1]} has defeated {yellow_text[2]} in {yellow_text[3]}\n')
            text_widget.update()
            try:
                c.execute("""INSERT INTO yellowText VALUES (?, ?, ?, ?)""", (yellow_text[0], yellow_text[2], yellow_text[1], yellow_text[3]))
            except Exception as e:
                print(e)
                print('INSERT failed')
        conn.commit()
        conn.close()

        text_widget.insert(1.0, 'Parsing complete!\n')
        text_widget.update()

    def delete_yellow_text_db(self, name):
        conn = self.misc_methods_instance.create_connection('./stables.db')
        c = conn.cursor()
        try:
            if name == 'All':
                c.execute("""DELETE FROM yellowText""")
            else:
                c.execute("""DELETE FROM yellowText WHERE charName = ?""", (name,))
            conn.commit()
            conn.close()
        except Exception as e:
            print('delete yt db error')
            print(e)
            return
        print('Yellow Text db deleted!')

    def check_if_yellow_text_exists(self, yellow_text):
        try:
            conn = self.misc_methods_instance.create_connection('./stables.db')
            c = conn.cursor()
            c.execute("""SELECT * from yellowText WHERE date = ? AND charName = ? AND opponent = ?""", (yellow_text[0], yellow_text[1], yellow_text[2]))
            res = c.fetchall()
            conn.commit()
            conn.close()
            if len(res):
                return True
        except Exception as e:
            print(e)
            print('check_if_yellow_text_exists() error')

    def show_please_wait_window(self):
        self.please_wait_window = Toplevel(self.main_window_instance.root)
        self.please_wait_window.title("Please Wait...")
        self.label = Label(self.please_wait_window, text="Parsing/writing, please wait...", padx=20, pady=20)
        self.label.pack()

        log_text = Text(self.please_wait_window, wrap=WORD, width=50, height=10)
        log_text.pack()

        return self.please_wait_window, log_text

class LogFileHandler(FileSystemEventHandler):
    def __init__(self, log_file_path=''):
        FileSystemEventHandler.__init__(self)  # Call the parent class's __init__ method
        self.log_file_path = log_file_path
        self.last_position = 0

    def on_modified(self, event):
        if not event.is_directory and event.src_path == self.log_file_path:
            # Log file has been modified, handle the changes here
            with open(self.log_file_path, 'r') as log_file:
                log_file.seek(self.last_position)  # Move to the last read position
                new_lines = log_file.readlines()
                # Update the last read position
                self.last_position = log_file.tell()
                # Process the newly added lines here
                for line in new_lines:
                    print(f'New Line in "{self.log_file_path}": {line}')

class YellowTextWatcher:
    def __init__(self, data_instance, main_window, log_file_path = '', log_folder_path = ''):
        self.data = data_instance
        self.main_window = main_window
        self.event_handler = LogFileHandler(log_file_path)
        self.log_file_path = log_file_path
        self.log_folder_path = log_folder_path
        self.observer = Observer()
        self.stopped = False

    def run(self):
        print('starting loop...')
        self.stopped = False
        self.data.log_file_being_monitored = True
        thread = threading.Thread(target=self.run_forever)
        thread.daemon = True
        thread.start()
    
    def run_forever(self):
         print('run forever test')
         self.main_window.root.title('Yellow Text Screenshot Sniffer Running...')
         while not self.stopped:
            log_file_path = self.monitor_log_folder()
            
            if log_file_path:
                self.run2(log_file_path)
         print('log folder parse aborted...')
         self.main_window.root.title('S T A B L E S')
    
    def run2(self, log_file_path):
        self.stopped = False
        regex = r"\[(.*?)\] \[.*\] (\w+) <.*?> has been defeated by (\w+) <.*?> in (.+)$"
        try:
            with open(log_file_path, 'r') as log_file:
                log_file.seek(0, 2)
                while not self.stopped:
                    for line in pygtail.Pygtail(log_file_path, read_from_end=True):
                        # Process the newly added line here
                        if re.search(regex, line):
                            print('YT Found! Creating image...')
                            self.take_screenshot_and_save()
                        print(f'New Line in "{log_file_path}": {line.strip()}')
                    time.sleep(0.1)  # Sleep briefly to avoid busy-waiting
        except KeyboardInterrupt:
            self.stop()
        # Loop is ended, reset booleans and mod_times:
        print('ending loop')
        self.stopped = True
        self.data.log_file_mod_times[log_file_path] = os.path.getmtime(log_file_path)
        self.main_window.root.title('S T A B L E S')

    def stop_global(self):
        self.stopped = True
    
    def stop(self):
        self.stopped = True
        self.observer.stop()
        self.observer.join()

    def monitor_log_folder(self):
        log_folder_path = f'{self.data.eq_dir}/logs/'
        for root, _, files in os.walk(log_folder_path):
            if self.stopped == True:
                break
            for file in files:
                if self.stopped == True:
                    break
                if file.endswith('offset') or file == 'dbg' or file.endswith('offset.txt') or file == 'dbg.txt':
                    continue
                log_file_path = os.path.join(root, file)
                last_modification_time = os.path.getmtime(log_file_path)

                if log_file_path not in self.data.log_file_mod_times:
                    self.data.log_file_mod_times[log_file_path] = last_modification_time

                elif last_modification_time > self.data.log_file_mod_times[log_file_path]:
                    self.data.log_file_mod_times[log_file_path] = last_modification_time
                    print(f'{log_file_path} has been modified')
                    self.data.modified_file_found = True
                    return log_file_path
        
                
    def take_screenshot_and_save(self):
        counter = 0
        file_name = 'killshot'
        while True:
            if counter == 0:
                screenshot_path = f'./killshots/{file_name}.jpg'
            else:
                screenshot_path = f'./killshots/{file_name}_{counter}.jpg'
            
            if not os.path.exists(screenshot_path):
                # Take a screenshot of the entire screen
                screenshot = ImageGrab.grab()
                # Save the screenshot as a JPEG file
                screenshot.save(screenshot_path)
                break
            else:
                counter += 1

class MiscMethods:
    def __init__(self, data_instance):
        self.data = data_instance
        
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

    def create_tables(self):
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

        sql_create_yellowtext_table = """ Create TABLE IF NOT EXISTS yellowText (
                                        date text,
                                        charName text,
                                        opponent text,
                                        location text

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
            self.create_table(conn, sql_create_yellowtext_table)
        conn.close()
    
    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn
    
    def fetch_eq_dir(self):
        conn = self.create_connection('./stables.db')
        c = conn.cursor()
        c.execute("""SELECT * FROM eqDir""")
        
        try:
            self.data.eq_dir = c.fetchall()[0][0]
            return
          
        except Exception as e:
            print('returning exception / c:/r99')
            self.data.eq_dir = 'c:/r99' 
            return 
        

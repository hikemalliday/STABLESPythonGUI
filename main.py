from tkinter import *

import classes


place_holder_methods = classes.PlaceHolderMethods()
main_data = classes.MainData()
main_window = classes.MainWindow(main_data, file_menu_instance=place_holder_methods, right_click_methods_instance=place_holder_methods, inventory_methods_instance=place_holder_methods, character_methods_instance=place_holder_methods, spells_methods_instance=place_holder_methods, inventory_window_instance=[], spells_window_instance=place_holder_methods, yellow_text_window_instance=place_holder_methods, yellow_text_methods_instance=place_holder_methods, yellow_text_watcher_instance=place_holder_methods, log_file_handler_instance=place_holder_methods)                

right_click_methods = classes.RightClickMethods(main_data, main_window)
main_window.right_click_methods_instance = right_click_methods

inventory_methods = classes.InventoryMethods(main_data, main_window, misc_methods_instance=place_holder_methods)
main_window.inventory_methods_instance = inventory_methods
right_click_methods.inventory_methods_instance = inventory_methods

spells_methods = classes.SpellsMethods(main_data, main_window, place_holder_methods, place_holder_methods)
right_click_methods.spells_methods_instance = spells_methods
main_window.spells_methods_instance = spells_methods

file_menu_methods = classes.FileMenuMethods(main_data, main_window, misc_methods_instance=place_holder_methods)
main_window.file_menu_instance = file_menu_methods


misc_methods = classes.MiscMethods(main_data)
spells_methods.misc_methods_instance = misc_methods
main_window.misc_methods_instance = misc_methods
file_menu_methods.misc_methods_instance = misc_methods
inventory_methods.misc_methods_instance = misc_methods

character_methods = classes.CharacterMethods(main_data, file_menu_methods, main_window, misc_methods)
right_click_methods.character_method_instance = character_methods

spells_window = classes.SpellsWindow(main_data, main_window, spells_methods, misc_methods)
spells_methods.spells_window_instance = spells_window
main_window.spells_window_instance = spells_window

inventory_window = classes.InventoryWindow(main_data, main_window, misc_methods)
main_window.inventory_window_instance = inventory_window
main_window.character_methods_instance = character_methods

yellow_text_window = classes.YellowTextWindow(main_data, main_window, file_menu_methods, right_click_methods, misc_methods)
main_window.yellow_text_window_instance = yellow_text_window

yellow_text_methods = classes.YellowTextMethods(main_data, main_window, file_menu_methods, right_click_methods, misc_methods, yellow_text_window)
main_window.yellow_text_methods_instance = yellow_text_methods

main_window.setup_main_window()

intitial_fetch = classes.InitialFetch(main_data, misc_methods, character_methods)
log_file_handler = classes.LogFileHandler(main_data.eq_dir)

yellow_text_watcher = classes.YellowTextWatcher(main_data, main_window, main_data.eq_dir)
main_window.yellow_text_watcher_instance = yellow_text_watcher
main_window.log_file_handler_instance = log_file_handler

main_window.root.mainloop()









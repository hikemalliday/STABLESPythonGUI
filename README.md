# STABLESPythonGUI

#### The STABLES app is a desktop app for Project1999. It is a log parsing app that reads / writes to a local SQLite database.

For installation instructions, please head to the wiki

Features:

- **Parse inventory files:**

Parse your character's /output inventory files and write them into a local DB (SQLite). You can then search the DB by item name and / or character name.

- **Parse spellbook files:**

Parse your character's spellbooks to see which spells are 'missing' from your spellbook. The 'missing spells' are written into the local DB.

- **Parse campout locations:**

Parse your character's log files to see where they are camped out at. This updates the 'location' column for a character.

- **Parse for Yellow Text (PvP kills):**

Parses all of your log files and writes the Yellow Text's into the local DB.

- **Monitor logs for Yellow Texts (PvP kills) in real time:**

Monitors the log file of the character you are playing. 

When a Yellow Text happens, the app will printscreen and dump a JPEG file in the local folder '/killshots'.
The image shown below was taken with this feature. Notice the dead enemy is midair still falling to the ground:
![Killshot JPEG example](https://cdn.discordapp.com/attachments/1058479766644199567/1161750968975773827/image.png?ex=65396fe7&is=6526fae7&hm=76ebb4b3ec718318d4fa53c224e0199e2c4c32056ff577ae078ec530250fd387&)

# Dev Notes:
EDIT: 7/21

This app was my first attempt at a desktop GUI app. I def learned a lot making it, but def fell into feature creep with this one. Lately I prefer to build desktop GUI apps with electron, but as with any hobby project, I learned a lot.

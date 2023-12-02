# STABLESPythonGUI

#### The STABLES app is a desktop app for Project1999. It is a log parsing app that reads / writes to a local SQLite database.

For installation instructions, please head to the wiki

Features:

- **Parse inventory files:**

Parse your character's /output inventory files and write them into a local DB (SQLite). You can then search the DB by item name and / or character name.
![Inventory Example](https://cdn.discordapp.com/attachments/1162507378340679751/1162507573832994886/image.png?ex=653c308b&is=6529bb8b&hm=8d580a9944739366df6a9988eb62d8007e661ffe315252b626a81f1f87fe6677&)

- **Parse spellbook files:**

Parse your character's spellbooks to see which spells are 'missing' from your spellbook. The 'missing spells' are written into the local DB.
![Missing Spells Example](https://cdn.discordapp.com/attachments/1162507378340679751/1162508991541289010/image.png?ex=653c31dd&is=6529bcdd&hm=d28753304d1e3ed7f3e2ec4a73931640e10cdd81f4a7182e3f93c0d3027efb67&)

- **Parse campout locations:**

Parse your character's log files to see where they are camped out at. This updates the 'location' column for a character.
![Campout Location Example](https://cdn.discordapp.com/attachments/1162507378340679751/1162509466709799002/image.png?ex=653c324f&is=6529bd4f&hm=0d2a62085f8d52877faf292d705d3414134c3206979b6accaeca67e58d863074&)

- **Parse for Yellow Text (PvP kills):**

Parses all of your log files and writes the Yellow Text's into the local DB.
![Yellow Text Table Example](https://cdn.discordapp.com/attachments/1162507378340679751/1162509733429780531/image.png?ex=653c328e&is=6529bd8e&hm=3c685b7fde0e385d31d18773ef7955f7f807742a71158a1f21cde362974210ec&)

- **Monitor logs for Yellow Texts (PvP kills) in real time:**

Monitors the log file of the character you are playing. 

When a Yellow Text happens, the app will printscreen and dump a JPEG file in the local folder '/killshots'.
This image was taken with this feature. Notice the dead enemy is midair still falling to the ground:
![Killshot JPEG example](https://cdn.discordapp.com/attachments/1058479766644199567/1161750968975773827/image.png?ex=65396fe7&is=6526fae7&hm=76ebb4b3ec718318d4fa53c224e0199e2c4c32056ff577ae078ec530250fd387&)

# Dev Notes:
I initially created the app without classes. I reached about two thousand lines of code, and the complexity started to increase. At this point a senior dev friend of mine suggested to use OOP to attempt to lessen complexity. So, I did a massive refactor and used classes. This is my second attempt at OOP (the first being a python based Checkers game). While it is certainly much easier for me to work on the program post refactor, I discovered that it is flawed. I implemented dependency injection, and I soon discovered that my program is ridden with 'circular dependency'. My solution was to create 'placeholder methods'. I needed mock methods to exist, so that the program would launch without crashing. This buys time for the dependency injections to resolve. Overall I am pleased with this program, as it provides a lot of value for me and my guildmates. 

The PvP kill screenshot feature is my first time ever using multithreading. I needed to use multithreading, so that the feature could be activated (it actively scans folders and files, and watches for killshots to happen in game) without locking up the app. This feature is one of the things I am most proud of that I have created. The feature first monitors the folder containing all the log files, then when it finds out which file is being modified in real time, it starts monitoring that file. Then, using REGEX, we wait for a pvp kill to happen. A screenshot of the monitor is then taken and saved into a folder.

I will likely re-write this program under the guidance of a senior dev friend of mine, in an attempt to really make it more profressional, as well as with a more modern looking UI. The library I used for the GUI (PyTkinter) is very easy to create with, but it looks like something straight out of 1997.

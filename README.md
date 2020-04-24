# List for organizing students by score

1 - To compile this application, go to **[PyInstaller](https://pypi.org/project/PyInstaller/)** and install it.

2 - In the command console, access the project directory where the index.py file is located. Type the following command:
`pyinstaller --windowed --onefile --icon=./favicon.ico index.py`

3 - Copy the `database.db` file found in this directory.

4 - Access the `dist` folder that has been created. Inside is the executable `index` file (the extension depends on the operating system you use). Paste the previously copied `database.db` file.

5 - Execute 'index'.

Autor - Fixing: when the program is first opened, load the data from the database correctly.
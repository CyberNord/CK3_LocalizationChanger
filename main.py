from pathlib import Path
import os

# ---------------------------------------------------
FOLDER = "db\\german\\"
PATTERN = "english"
REPLACE_WITH = "german"
# ---------------------------------------------------


INPUT_DIR = Path.cwd() / FOLDER

file: Path
for file in list(INPUT_DIR.rglob("*.yml*")):

    filepath = os.path.dirname(os.path.abspath(file))
    filename = file.name.split('/')[0]
    newfileName = filename.replace(PATTERN, REPLACE_WITH)

    # replace text in file
    with open(file, 'r') as f_r:
        file_data = f_r.read()
        file_data = file_data.replace(PATTERN, REPLACE_WITH)
    with open(file, 'w') as f_r:
        f_r.write(file_data)

    # rename File
    old_file = os.path.join(filepath, filename)
    new_file = os.path.join(filepath, newfileName)
    os.rename(old_file, new_file)





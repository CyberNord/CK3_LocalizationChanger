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
    with open(file, 'r', encoding="utf-8") as f_r:
        file_data = f_r.readlines()
        file_data[0] = file_data[0].replace(PATTERN, REPLACE_WITH)
    with open(file, 'w', encoding="utf-8") as f_r:
        f_r.writelines(file_data)

    # rename File
    old_file = os.path.join(filepath, filename)
    new_file = os.path.join(filepath, newfileName)
    os.rename(old_file, new_file)





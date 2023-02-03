import time
from pathlib import Path
import os
import re
from googletrans import Translator

# ---------------------------------------------------
FOLDER = "db\\english\\"
PATTERN = "english"
REPLACE_WITH = "german"
do_translation = True  # translation will take time as API demands timeouts..
translator = Translator()
RE_PATTERN = re.compile(r'\[[^"\]]*]|\$[^$]+\$|#[^$]+#|\\n')
REPLACER = '{@}'
# ---------------------------------------------------

INPUT_DIR = Path.cwd() / FOLDER
totalCount = 0

file: Path
for file in list(INPUT_DIR.rglob("*.yml*")):

    filepath = os.path.dirname(os.path.abspath(file))
    filename = file.name.split('/')[0]
    newfileName = filename.replace(PATTERN, REPLACE_WITH)

    # replace text in file
    with open(file, 'r', encoding="utf-8") as f_r:
        print("current File: " + file.name)
        file_data = f_r.readlines()
        file_data[0] = file_data[0].replace(PATTERN, REPLACE_WITH)

        if do_translation:
            #  basic Translator in work
            for i, lines in enumerate(file_data[1:]):
                matches = re.findall('"([^"]*)"', lines)
                print(matches)
                if len(matches) == 1 and matches is not None:
                    tokens = re.findall(RE_PATTERN, matches[0])
                    print(tokens)

                    match = matches[0]
                    matches[0] = re.sub(RE_PATTERN, REPLACER, matches[0])
                    print(matches)

                    # timeout is needed otherwise api will block usage
                    print("Timeout API.")
                    for j in range(2, 0, -1):
                        print(j, end="...")
                        time.sleep(1)
                    print("resuming")

                    # translate
                    try:
                        translation = translator.translate(matches[0], dest='de', src='en')
                        padded_translation = translation.text
                    except TypeError:
                        translation = matches[0]
                        padded_translation = matches[0]
                        print('Error Skiped in: ' + matches[0])
                    totalCount += 1

                    print(padded_translation)
                    for t in tokens:
                        padded_translation = padded_translation.replace(REPLACER, t, 1)

                    print(padded_translation)
                    file_data[i + 1] = lines.replace(match, padded_translation, 1)
                    print(file_data[i + 1])
                    print("#" + str(totalCount))
                print()

    old_file = os.path.join(filepath, filename)
    newfileName = filename.replace(PATTERN, REPLACE_WITH, 1)
    new_filepath = filepath.replace(PATTERN, REPLACE_WITH, 1)
    new_file = os.path.join(new_filepath, newfileName)

    new_path = Path(new_file)
    if not os.path.exists(new_filepath):
        os.makedirs(new_filepath)

    with open(new_path, 'w', encoding="utf-8-sig") as f_r:
        f_r.writelines(file_data)

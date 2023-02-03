import time
import argparse
from pathlib import Path
import os
import re
from googletrans import Translator

# ---------------------------------------------------
PATTERN = "english"
REPLACE_WITH = "german"
translator = Translator()
RE_PATTERN = re.compile(r'\[[^"\]]*]|\$[^$]+\$|#[^$]+#|\\n')
REPLACER = '{@}'
# ---------------------------------------------------

def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l1", type=str, default="en")
    parser.add_argument("-l2", type=str, default="de")
    parser.add_argument("-trans", type=int, default=1)
    parser.add_argument("path")

    args = parser.parse_args()
    fromlanguage = args.l1
    tolanguage = args.l2
    if args.trans == 1:
        do_translation = True
    else:
        do_translation = False
    target_dir = Path(args.path)

    if not target_dir.exists():
        print("The target directory doesn't exist")
        raise SystemExit(1)
    init(target_dir, do_translation,fromlanguage,tolanguage)


def init(target_dir, do_translation, fromlanguage, tolanguage):
    INPUT_DIR = target_dir
    print("INPUT_DIR " + INPUT_DIR.__str__())

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
                translate(file_data, totalCount, fromlanguage, tolanguage)

            tofile(filepath, filename, file_data)


def tofile(filepath, filename, file_data):
    old_file = os.path.join(filepath, filename)
    newfileName = filename.replace(PATTERN, REPLACE_WITH, 1)
    new_filepath = filepath.replace(PATTERN, REPLACE_WITH, 1)
    new_file = os.path.join(new_filepath, newfileName)

    new_path = Path(new_file)
    if not os.path.exists(new_filepath):
        os.makedirs(new_filepath)

    with open(new_path, 'w', encoding="utf-8-sig") as f_r:
        f_r.writelines(file_data)


def translate(file_data, totalCount, fromlanguage, tolanguage):
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
                translation = translator.translate(matches[0], dest=tolanguage, src=fromlanguage)
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


if __name__ == "__main__":
    parseargs()

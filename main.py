import datetime
import time
import argparse
from pathlib import Path
import os
import re
from googletrans import Translator

# ---------------------------------------------------
DEBUG = False
INFO = False
translator = Translator()
RE_PATTERN = re.compile(r'\[[^"\]]*]|\$[^$]+\$|#[^$]+#|\\n')
REPLACER = '{@}'
LINE_STR = '-----------------------------------------'
# ---------------------------------------------------

def get_loc_code(from_l: bool, pars_arg: str):
    locale_codes = {
        'en': 'english',
        'de': 'german',
        'fr': 'french',
        'es': 'spanish',
        'ru': 'russian',
        'zh-cn': 'simp_chinese',
        'ko': 'korean'
    }
    locale = locale_codes.get(pars_arg)
    if not locale:
        locale = 'english' if from_l else 'german'
    return locale


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l1", type=str, default="en")
    parser.add_argument("-l2", type=str, default="de")
    parser.add_argument("-trans", type=int, default=1)
    parser.add_argument("path")

    args = parser.parse_args()
    from_language = args.l1
    to_language = args.l2
    from_naming = get_loc_code(True, from_language)
    to_naming = get_loc_code(False, to_language)

    if args.trans == 1:
        do_translation = True
    else:
        do_translation = False
    target_dir = Path(args.path)

    if not target_dir.exists():
        print("The target directory doesn't exist")
        raise SystemExit(1)
    log_message(
        LINE_STR + "\nNew Translation " + from_language + " --> " + to_language + "\n" + LINE_STR,
        False)
    init(target_dir, do_translation, from_language, to_language, from_naming, to_naming)


def log_message(message, sign_t=True):
    log_file = "error_log.txt"
    if not os.path.exists(log_file):
        open(log_file, "w").close()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as file:
        if sign_t:
            file.write("[{}] {}\n".format(timestamp, message))
        else:
            file.write("{}\n".format(message))


def init(target_dir, do_translation, from_language, to_language, from_naming, to_naming):
    INPUT_DIR = target_dir
    print("INPUT_DIR " + INPUT_DIR.__str__())

    totalCount = 0

    file: Path
    for file in list(INPUT_DIR.rglob("*.yml*")):
        filepath = os.path.dirname(os.path.abspath(file))
        filename = file.name.split('/')[0]
        newfileName = filename.replace(from_naming, to_naming)

        # replace text in file
        with open(file, 'r', encoding="utf-8") as f_r:
            print(LINE_STR)
            print("current File: " + file.name)
            log_message("\n" + file.name, False)

            file_data = f_r.readlines()
            file_data[0] = file_data[0].replace(from_naming, to_naming)
            if do_translation:
                translate(file_data, totalCount, from_language, to_language)
            tofile(filepath, filename, file_data, from_naming, to_naming)


def tofile(filepath, filename, file_data, from_naming, to_naming):
    old_file = os.path.join(filepath, filename)
    newfileName = filename.replace(from_naming, to_naming, 1)
    new_filepath = filepath.replace(from_naming, to_naming, 1)
    new_file = os.path.join(new_filepath, newfileName)

    new_path = Path(new_file)
    if not os.path.exists(new_filepath):
        os.makedirs(new_filepath)

    with open(new_path, 'w', encoding="utf-8") as f_r:
        f_r.writelines(file_data)


def translate(file_data, totalCount, from_language, to_language):
    #  basic Translator in work
    for i, lines in enumerate(file_data[1:]):
        matches = re.findall('"([^"]*)"', lines)
        if len(matches) == 1 and matches[0] != '' and matches is not None:
            tokens = re.findall(RE_PATTERN, matches[0])

            match = matches[0]
            matches[0] = re.sub(RE_PATTERN, REPLACER, matches[0])

            # timeout is needed otherwise api will block usage
            if DEBUG:
                print("Timeout API.")
                for j in range(2, 0, -1):
                    print(j, end="...")
                    time.sleep(1)
                print("resuming")
            else:
                time.sleep(2)
            # translate
            try:
                translation = translator.translate(matches[0], dest=to_language, src=from_language)
                padded_translation = translation.text
            except TypeError:
                translation = matches[0]
                padded_translation = matches[0]
                print('Error (TypeError) Skipped in: ' + matches[0])
                log_message("Translator TypeError in line #" + totalCount + " : " + matches[0])
            except TimeoutError:
                translation = matches[0]
                padded_translation = matches[0]
                print('Error (TimeOut) Skipped in: ' + matches[0])
                log_message("Translator TimeOut in line #" + totalCount + " : " + matches[0])
            except:
                # no optimal solution
                translation = matches[0]
                padded_translation = matches[0]
                print('Unknown Exception - Skipped in' + matches[0])
                log_message("Unknown Exception in line #" + totalCount + " : " + matches[0])
            totalCount += 1

            if DEBUG:
                print(padded_translation)

            for t in tokens:
                padded_translation = padded_translation.replace(REPLACER, t, 1)

            if DEBUG:
                print(padded_translation)

            file_data[i + 1] = lines.replace("\"" + match + "\"", "\"" + padded_translation + "\"", 1)
            if INFO:
                print(match + " <- " + padded_translation)
            print("line no. #" + str(totalCount), end="")
        print()


if __name__ == "__main__":
    parseargs()

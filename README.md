
# ck3-Translator

This Project allows the user to automatically translate ck3 (Crusader Kings 3) localisation files to other languages supported by the game and the translator API.

## Authors

- [@CyberNord](https://github.com/CyberNord)
- [@Martin220799](https://github.com/Martin220799)    (Powershell Controls) 


## Installation

#### Requirements
Before Starting make sure the following libraries are installed. 

- [Python 3.1](https://www.python.org/download/releases/3.1/)
- [googletrans 4.0.0rc1](https://libraries.io/pypi/googletrans)
- [PyYAML](https://pypi.org/project/PyYAML/)

While higher versions of Python may work, its important to use the googletrans version 4.0.0rc1 (or higher) older versions will cause the the Program to throw an error.

#### First Steps
Download the project folder from github and unpack it in a Location of your desire. Start a command prompt (e.g. PowerShell) in the path where the main.py is located. 
The default setting is translating from english to german and it will look like that. 

```bash
  python main.py D:\the\path\to\english\loc\folder
```

### Usage
Below you can see the general Syntax 

```bash
python main.py [-h] [-l1 L1] [-l2 L2] [-trans TRANS] path
```

The following parts are mandatory
 - **python main.py**&nbsp;&nbsp;&nbsp;&nbsp;call of the programm
 - **path**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;path to the folder to be translated
 
Optional information
- **[-h]**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; no function for now
- **[-l1 L1]**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;given input language (default = en)
- **[-l2 L2]**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;desired output language (default = de)
- **[-trans TRANS]**&nbsp;&nbsp;(default = 1) If this value is set to 0 there will be no translation. The Programm wil only convert the files to the disired output language so that it is supported by the game (e.g. results in english text in german localisation)

#### More examples

this will translate from english (default) to french
```bash
python main.py -l2 fr D:\the\path\to\english\loc\folder
```
this will translate from french to german (default)
```bash
python main.py -l1 fr D:\the\path\to\english\loc\folder
```

this will just alter the first line and filename so that the localisation is detected by the game
```bash
python main.py -trans 0 D:\the\path\to\english\loc\folder
```
#### Supported languages 
The list is limited by the possible localisation of CK3.
- 'en' english
- 'de' german
- 'fr' french
- 'es' spanish
- 'zh-cn' simplified chinese
- 'ko' korean

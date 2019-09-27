import os
import sys
import json
DIR = os.path.dirname(__file__)
PYMEL = os.path.join(DIR, "pymel")
HTML = os.path.join(DIR, "html.json")

html_dict = {}
with open(HTML,'r') as f:
    html_dict = json.load(f, encoding="utf-8")

exclude_file = [
    '__init__.py',
    "all.py",
    "allapi.py",
    "runtime.py",
    "ipymel.py",
    "conditions.py",
    "trees.py",
    "testing.py",
    "shell.py",
    "scanf.py",
    "picklezip.py",
    "objectParser.py",
    "nameparse.py",
]
exclude_dir = ['internal', 'external','ply','mel2py']

def readFile(path):
    path = path.replace("\\","/")
    moudle,ext = os.path.splitext(path)
    _, module = moudle.split(DIR)
    module = module[1:].replace("/",".")
    # pymel_module,func = module.rsplit(".",1)
    # print(html_dict[module])
    if html_dict.has_key(module):
        html_dict[module]
        
    else:
        if module == "pymel.util.namedtuple":
            pass
        elif module == "pymel.util.path":
            pass
    
    # with open(path,'r') as f:
    #     content = f.read()
    

def main():

    for root, dirs, files in os.walk(PYMEL):
        _,folder = os.path.split(root)
        if folder in exclude_dir:
            continue

        for py in files:
            if not py.endswith(".py") or py in exclude_file:
                continue
            
            readFile(os.path.join(root, py))



if __name__ == "__main__":
    main()

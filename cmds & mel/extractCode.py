# coding:utf-8
from html2text import HTML2Text
from pathlib import Path
import re
import os
import json


parser = HTML2Text()
parser.wrap_links = False
parser.skip_internal_links = True
parser.inline_links = True
parser.ignore_anchors = True
parser.ignore_images = True
parser.ignore_emphasis = True
parser.ignore_table = True


def getParamData(snippet):
    name = snippet.split("|")[0]
    param_longName = name.split("(")[0][1:]
    param_shortName = re.search(r"\((.*?)\)", name).group(1)
    
    snippet2 = snippet.split("|")[1].replace("\n", " ")
    param_type = re.search(r"`(.*)`", snippet2).group(1)
    
    reg = r"\|  \|  (.*)---\|"
    param_instruction = re.search(reg, snippet.replace("\n", " ")).group(1).strip()

    return{
        # "source": snippet,
        "longName": param_longName,
        "shortName": param_shortName,
        "type": param_type,
        "instruction": param_instruction
    }


def extractCommandData(DIR,extract="python",exclude_list=[],long_space=15,short_space=5):
    command_info = {}
    DIR = Path(DIR)

    output_file = ""
    for i, html in enumerate(DIR.iterdir()):

        command = html.resolve().stem
        ext = html.resolve().suffix

        # NOTE 删除无关页面
        if command in exclude_list or ext != ".html":
            print ("delete -> ",html)
            os.remove(html)
            continue

        print(i, command)

        output_file += f"def {command}(*args, **keywords):\n"
        output_file += "    \"\"\"\n"
        
        
        command_info[command] = {}
        command_info[command]["link"] = r"http://help.autodesk.com/cloudhelp/2019/ENU/Maya-Tech-Docs/CommandsPython/" + html.name
        with open(html, 'r', encoding='utf-8') as f:
            try:
                upper, lower = f.read().split('<h2><a name="hReturn">Return value')
            except:
                print(f"'{command}',")
                continue

            # NOTE 提取说明
            reg = r'<p id="synopsis">(?:.|\n)*?</p>'
            instruction = re.split(reg, upper)[-1]
            instruction = parser.handle(instruction).strip()
            command_info[command]["instruction"] = instruction
            mode_list = ["query","edit"]
            if "NOT queryable" in instruction:
                mode_list.remove("query")
            if "NOT editable" in instruction:
                mode_list.remove("edit")
            command_info[command]["mode"] = mode_list


            for line in instruction.split("\n"):
                output_file += f"    {line}\n"

            # NOTE 提取返回值

            command_info[command]["param"] = []

            # NOTE 提取参数
            snippets = lower.split('<tr bgcolor="#EEEEEE">')
            for j, snippet in enumerate(snippets):

                # NOTE 提取 Return 信息
                if j == 0:
                    return_list = parser.handle(snippet).split("##")[0]
                    return_list = return_list.replace("\n---|---", "")
                    return_value = " ".join(return_list.split("|")).strip()

                    command_info[command]["return"] = return_value
                    output_file += "\n    Return Value:\n"
                    for line in return_value.split("\n"):
                        output_file += f"     {line}\n"

                    output_file += "\n    Flags:\n"
                # NOTE 提取参数属性
                elif j == len(snippets)-1:
                    snippet, example = parser.handle(snippet).split("* * *")
                    data = getParamData(snippet)
                    command_info[command]["param"].append(data)
                    output_file += f"        {data['longName']:<{long_space}}"
                    output_file += f" : {data['shortName']:<{short_space}}"
                    output_file += f" [{data['type']}]\n"
                    output_file += f"          {data['instruction']}\n\n"
                else:

                    mode_list = []
                    if 'alt="query" title="query"' in snippet:
                        mode_list.append('query')
                    if 'alt="edit" title="edit"' in snippet:
                        mode_list.append('edit')

                    snippet = parser.handle(snippet)
                    data = getParamData(snippet)
                    data['mode'] = mode_list
                    command_info[command]["param"].append(data)
                    output_file += f"        {data['longName']:<{long_space}}"
                    output_file += f" : {data['shortName']:<{short_space}}"
                    output_file += f" [{data['type']}]\n"
                    output_file += f"          {data['instruction']}\n\n"
            else:
                # NOTE 提取 Example
                if extract == "python":
                    example = example.split("Python examples")[-1].strip()
                elif extract == "mel":
                    example = "    " + example.split("MEL examples")[-1].strip()

                command_info[command]["example"] = example

                output_file += "    Python Example:\n\n" if extract == "python" else "    MEL Example:\n\n"
                for line in example.split("\n"):
                    line = line.replace('"""', '\\"\\"\\"')
                    if "# //" in line:
                        continue
                    output_file += f"    {line}\n"

        output_file += "    \"\"\"\n\n"

    FILE = Path(__file__)
    
    # output_py = FILE.parent / f"{extract}.py"
    # with open(output_py,'w',encoding="utf-8") as f:
    #     f.write(output_file)
    
    output_json = FILE.parent / f"{extract}.json"
    with open(output_json,'w',encoding="utf-8") as f:
        json.dump(command_info, f, indent=4)
        


if __name__ == "__main__":
    exclude_list = [
        # NOTE not command
        'cat_Animation',
        'cat_Effects',
        'cat_General',
        'cat_Language',
        'cat_Modeling',
        'cat_Rendering',
        'cat_System',
        'cat_Windows',
        'CommandsPython_index',
        'Commands_index',
        'frame_search',
        'index',
        'index_all',
        'index_overview',
        'index_substring',
        'letter_A',
        'letter_B',
        'letter_C',
        'letter_D',
        'letter_E',
        'letter_F',
        'letter_G',
        'letter_H',
        'letter_I',
        'letter_J',
        'letter_K',
        'letter_L',
        'letter_M',
        'letter_N',
        'letter_O',
        'letter_P',
        'letter_Q',
        'letter_R',
        'letter_S',
        'letter_T',
        'letter_U',
        'letter_V',
        'letter_W',
        'letter_X',
        'nav_Animation',
        'nav_Effects',
        'nav_General',
        'nav_Language',
        'nav_Modeling',
        'nav_Rendering',
        'nav_System',
        'nav_Windows',
        'show',
        'blank',
        
    ]
    obselete_list =[
        'dynControl',
        'displayStats',
        'reference',
        'webBrowserPrefs',
        'userCtx',
        'selectedNodes',
    ]

    FILE = Path(__file__)
    PY_DIR = FILE.parent / "CommandsPython"
    MEL_DIR = FILE.parent / "Commands"
    extractCommandData(MEL_DIR, "mel", exclude_list=exclude_list + obselete_list)

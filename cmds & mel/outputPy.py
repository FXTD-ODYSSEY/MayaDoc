# coding:utf-8
import json
import os
from bs4 import BeautifulSoup
DIR = os.path.dirname(__file__)
JSON_PATH = os.path.join(DIR,"python.json")
HTML_PATH = os.path.join(DIR,"cat")
OUTPUT_PATH = os.path.join(DIR,"cmds")

# NOTE 读取 json 数据
def loadJsonData():
    with open(JSON_PATH,'r') as f:
        cmds_dict = json.load(f)
    return cmds_dict

def loadHTMLData():
    cat_dict = {}
    cat_list = [
        'Animation',
        'Effects',
        'General',
        'Language',
        'Modeling',
        'Rendering',
        'System',
        'Windows',
    ]

    for cat in cat_list:
        path = os.path.join(HTML_PATH,"cat_%s.html"%cat)
        with open(path,'r') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        attr_list = []
        for table in soup.findAll("table"):
            for attr in table.findAll("a"):
                attr_list.append(attr.text)

        cat_dict[cat] = attr_list

    return cat_dict  

def main():
    cmds_dict = loadJsonData()
    cat_dict = loadHTMLData()

    long_space=15
    short_space=5
    init_file = ""
    for name in cat_dict:
        output_file = ""
        init_file += f"from maya.cmds.{name} import *\n"
        for func in cat_dict[name]:
            # NOTE 跳过 Obselete 命令
            if func not in cmds_dict:
                continue
            
            # NOTE 函数名称
            output_file += f"def {func}("

            for mode in cmds_dict[func]["mode"]:
                if mode == "query":
                    output_file += "q=1,"
                elif mode == "edit":
                    output_file += "e=1,"

            for data in cmds_dict[func]["param"]:
                param = data['shortName']
                if param == "e" or param == "q" or not data['shortName']:
                    param = data['longName']
                    
                output_file += param
                output_file += f"=\"{data['type']}\"," if data['type'] != "boolean" else f"=1,"


            # NOTE 去除多出的逗号
            if len(cmds_dict[func]["param"]+cmds_dict[func]["mode"]) >= 1:
                output_file = output_file[:-1]
            output_file += "):\n    \"\"\"\n"
            output_file += f"{cmds_dict[func]['link']}\n\n"

            # NOTE 函数说明
            output_file += "\n\n-----------------------------------------\n\n"
            for line in cmds_dict[func]["instruction"].split("\n"):
                output_file += f"{line}\n"
            
            # NOTE 函数返回值
            output_file += "\n\n-----------------------------------------\n\n"
            output_file += "\nReturn Value:\n\n"
            for line in cmds_dict[func]["return"].split("\n"):
                output_file += f"{line}\n"
            
            # NOTE 函数参数说明
            if cmds_dict[func]["param"]:
                output_file += "\n\n-----------------------------------------\n\n"
                output_file += "\nFlags:\n\n"

            for data in cmds_dict[func]["param"]:
                output_file += "-----------------------------------------\n\n"
                output_file += f"{data['shortName']:<{short_space}}"
                output_file += f" : {data['longName']:<{long_space}}"
                output_file += f" [{data['type']}]"
                if "mode" in data:
                    output_file += f" {data['mode']}\n"
                else:
                    output_file += "\n"
                output_file += f"    {data['instruction']}\n\n"

            # output_file += "    Python Example:\n\n"

            # # NOTE 函数使用例子
            # for i, line in enumerate(cmds_dict[func]["example"].split("\n")):
            #     if i == 0:
            #         line = "    %s" % line
            #     line = line.replace('"""', '\\"\\"\\"')
            #     if "# //" in line:
            #         continue
            #     output_file += f"    {line}\n"

            output_file += "    \"\"\"\n\n"

        # NOTE 输出 模块 文件
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)
        output = os.path.join(OUTPUT_PATH,"%s.py"%name)
        with open(output,'w',encoding="utf-8") as f:
            f.write(output_file)

    # NOTE 输出 __init__.py  文件
    output = os.path.join(OUTPUT_PATH, "__init__.py" )
    with open(output, 'w', encoding="utf-8") as f:
        f.write(init_file)



if __name__ == "__main__":
    main()
    from maya import cmds
    
    cmds.about(api=1,bd=1)
    cmds.polyCube(q=1)
    cmds.spaceLoca

    from maya import OpenMaya

    OpenMaya.MSelectionList()

    import pymel.core as pm
    pm.PyNode()
    pm.space
    
    

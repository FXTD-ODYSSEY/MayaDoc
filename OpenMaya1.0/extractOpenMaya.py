# coding:utf-8
from html2text import HTML2Text
import re
import json
import os
from collections import OrderedDict
from maya import OpenMaya
from maya import OpenMayaAnim
from maya import OpenMayaFX
from maya import OpenMayaMPx
from maya import OpenMayaRender
from maya import OpenMayaUI

parser = HTML2Text()
parser.wrap_links = False
parser.skip_internal_links = True
parser.inline_links = True
parser.ignore_anchors = True
parser.ignore_images = True
parser.ignore_emphasis = True
parser.ignore_table = True

# ! ----------------------------------------

DIR = os.path.dirname(__file__)
WEB = os.path.join(
    r"D:\Users\Administrator\Desktop\MayaDoc\maya-2019-developer-help_enu_offline", "cpp_ref")
FOLDER = os.path.join(DIR, "cpp_ref")


def get_dict():
    html_set = set()
    html_dict = {}
    for i, html in enumerate(os.listdir(FOLDER)):
        path = os.path.join(FOLDER, html).replace("\\", "/")
        with open(path, 'r') as f:
            data = f.read()
        func = re.search(r"<h1>(.*?)</h1>", data).group(1).split(" ")[0]
        html_set.add(func)
        html_dict[func] = os.path.join(FOLDER, html).replace("\\", "/")

    OpenMaya_set = set()
    OpenMaya_set.update(set(dir(OpenMaya)))
    OpenMaya_set.update(set(dir(OpenMayaAnim)))
    OpenMaya_set.update(set(dir(OpenMayaFX)))
    OpenMaya_set.update(set(dir(OpenMayaMPx)))
    OpenMaya_set.update(set(dir(OpenMayaRender)))
    OpenMaya_set.update(set(dir(OpenMayaUI)))

    func_set = html_set.intersection(OpenMaya_set)

    # # NOTE 可以获取到所有 OpenMaya 不支持的页面
    # for i,func in enumerate(html_set - func_set):
    #     print i,html_dict[func]
    #     os.remove(html_dict[func])

    # # NOTE OpenMaya有但是在 HTML 上没有的
    # for i,func in enumerate(OpenMaya_set - func_set):
    #     if "_" not in func:
    #         if func in dir(OpenMaya):
    #             print i,"OpenMaya",func
    #         elif func in dir(OpenMayaAnim):
    #             print i,"OpenMayaAnim",func
    #         elif func in dir(OpenMayaFX):
    #             print i,"OpenMayaFX",func
    #         elif func in dir(OpenMayaMPx):
    #             print i,"OpenMayaMPx",func
    #         elif func in dir(OpenMayaRender):
    #             print i,"OpenMayaRender",func
    #         elif func in dir(OpenMayaUI):
    #             print i,"OpenMayaUI",func

    # NOTE 提取相关函数的方法名
    func_dict = {}
    func_dict["OpenMaya"] = {}
    func_dict["OpenMayaAnim"] = {}
    func_dict["OpenMayaFX"] = {}
    func_dict["OpenMayaMPx"] = {}
    func_dict["OpenMayaRender"] = {}
    func_dict["OpenMayaUI"] = {}
    for i, func in enumerate(func_set):
        if func in dir(OpenMaya):
            func_dict["OpenMaya"][func] = [method for method in dir(
                eval("OpenMaya.%s" % func)) if not method.startswith("__")]
        elif func in dir(OpenMayaAnim):
            func_dict["OpenMayaAnim"][func] = [method for method in dir(
                eval("OpenMayaAnim.%s" % func)) if not method.startswith("__")]
        elif func in dir(OpenMayaFX):
            func_dict["OpenMayaFX"][func] = [method for method in dir(
                eval("OpenMayaFX.%s" % func)) if not method.startswith("__")]
        elif func in dir(OpenMayaMPx):
            func_dict["OpenMayaMPx"][func] = [method for method in dir(
                eval("OpenMayaMPx.%s" % func)) if not method.startswith("__")]
        elif func in dir(OpenMayaRender):
            func_dict["OpenMayaRender"][func] = [method for method in dir(
                eval("OpenMayaRender.%s" % func)) if not method.startswith("__")]
        elif func in dir(OpenMayaUI):
            func_dict["OpenMayaUI"][func] = [method for method in dir(
                eval("OpenMayaUI.%s" % func)) if not method.startswith("__")]

    # # NOTE 输出json文件
    # json_path = os.path.join(DIR,"output2.json")
    # with open(json_path,'w') as f:
    #     json.dump(func_dict,f,indent=4)

    # # NOTE 将网页转成 Markdown
    # OUTPUT_FOLDER = os.path.join(DIR, "cpp_ref_md")
    # if not os.path.exists(OUTPUT_FOLDER):
    #     os.mkdir(OUTPUT_FOLDER)

    # for func in func_dict["OpenMaya"]:
    #     path = html_dict[func]
    #     with open(path, 'r') as f:
    #         html = f.read()
    #     md_file = os.path.split(path)[1].replace(".html",".md")
    #     path = os.path.join(OUTPUT_FOLDER, md_file)
    #     with open(path,'w') as f:
    #         f.write(parser.handle(html).strip().encode("utf-8"))
    return func_dict, html_dict


def itemParser(content):
    header, doc = content.split('<div class="memdoc">')

    # NOTE 提取 description
    description = parser.handle(doc.split("<dl")[0]).strip()

    # NOTE 提取 header
    header = parser.handle(header).replace("|", "").replace("---", "")
    header = header.encode("utf8").strip()
    name = re.search(r'((?:.|\n)*?)\(', header).group(1).strip()
    func_name = name.split(" ")[-1]

    header_split = header.replace("(*)", "").split(func_name)
    
    return_type = header_split[0]
    keyword = func_name.join(header_split[1:])
    
    # NOTE 根据 header 提取参数类型和默认值
    keyword = re.findall("\(((?:.|\n)*)\)", keyword)[-1]
    keywords = {}
    for line in keyword.split(","):
        line = line.strip()
        if not line:
            continue
        
        if "\xc2\xa0" in line:
            param_type, _, param_name = line.partition("\xc2\xa0")
            param_name = param_name.replace("\xc2\xa0", "").strip()
        else:
            param_type,_,param_name = line.rpartition(" ")

        if "=" in param_name:
            name, val = param_name.split("=")
            name = name.strip().split("[")[0].replace("*","")
            keywords[name] = [param_type.strip(), val.strip()]
        else:
            name = param_name.strip().split("[")[0].replace("*", "")
            keywords[name] = [param_type.strip()]
    
    # NOTE 提取 params
    params = ""
    for param in re.findall(r'<dl class="params">((?:.|\n)*?)</dl>', doc):
        for line in re.findall(r'<tr>((?:.|\n)*?)</tr>', param):
            line = parser.handle(line).replace("|", "")
            line = line.replace("---", "").strip()
            line += " "
            
            # NOTE MPxModelEditorCommand 的 modelView 方法不合规范
            if "]" not in line and func_name == "modelView":
                line = "[out] %s" % line

            regx = r'(\[(?:in|out|in,out)\]) (.*?) '
            _,inout, name, instruction = re.split(regx, line)

            if len(keywords[name]) == 2:
                param_type,default = keywords[name]
                params += "%-5s %-20s %-15s %-10s %s\n" % (inout,param_type, name, "{default:%s}"%default, instruction)
            else:
                param_type = keywords[name][0]
                params += "%-5s %-20s %-15s %s\n" % (inout,param_type, name, instruction)

    # NOTE 提取 returns
    return_type = "[%s]" % return_type.replace("OPENMAYA_MAJOR_NAMESPACE_OPEN ","").strip()
    returns = "%-10s " % return_type if return_type != "[]" else ""
    for return_val in re.findall(r'<dl class="section return">((?:.|\n)*?)</dl>', doc):
        return_val = parser.handle(return_val).replace("|", "")
        return_val = return_val.replace("---", "")
        return_val = return_val.replace("Returns", "")
        returns   += return_val.strip()

    return func_name, description, params, returns


def main():

    func_dict, html_dict = get_dict()

    OpenMaya_dict = {}
    for i,module in enumerate(func_dict):
        # if i < 5: continue
        OpenMaya_dict[module] = {}
        for j, func in enumerate(func_dict[module]):
            # if j < 150:continue
            print i,j,func
            OpenMaya_dict[module][func] = {}
            path = html_dict[func]
            with open(path, 'r') as f:
                html = f.read()

            # NOTE 获取线上访问网址
            WEB = r"http://help.autodesk.com/view/MAYAUL/2019/ENU/?guid=Maya_SDK_MERGED_cpp_ref_"
            html_file = WEB + os.path.split(path)[-1].replace(".","_")

            for content in re.split(r'<h2 class="groupheader">', html):
                # NOTE 有两个HTML含有非法字符
                if "Class Description" in content:
                    content = parser.handle(content)
                    instruction = content.split("Class Description")[-1]
                    instruction = instruction.split("Examples:")[0].strip()
                    instruction = instruction.split("Inheritance diagram")[0].strip()
                    OpenMaya_dict[module][func]["instruction"] = instruction
                # NOTE 方法提取处理
                elif "Member Function Documentation" in content:
                    OpenMaya_dict[module][func]["method"] = {}
                    anchor_list = re.findall('<a class="anchor" id="(.*?)"></a>',content)
                    item_list = content.split('<div class="memitem">')[1:]
                    for anchor,method in zip(anchor_list,item_list):
                        name, description, params, returns = itemParser(method)
                        OpenMaya_dict[module][func]["method"][name] = {
                            "link": "%s#%s" % (html_file, anchor),
                            "anchor": anchor,
                            "description": description,
                            "param": params,
                            "return": returns,
                        }
                # NOTE 构造函数
                elif "Constructor &amp; Destructor Documentation" in content:
                    OpenMaya_dict[module][func]["constructor"] = []
                    anchor_list = re.findall('<a class="anchor" id="(.*?)"></a>',content)
                    item_list = content.split('<div class="memitem">')[1:]
                    for anchor, constructor in zip(anchor_list, item_list):
                        _, description, params, returns = itemParser(constructor)
                        OpenMaya_dict[module][func]["constructor"].append({
                            "link": "%s#%s" % (html_file, anchor),
                            "anchor": anchor,
                            "description": description,
                            "param": params,
                            "return": returns,
                        })


    output = os.path.join(DIR, "OpenMaya1.0.json")
    with open(output, 'w') as f:
        json.dump(OpenMaya_dict, f,indent=4, encoding="utf-8")
    # print OpenMaya_dict["OpenMayaAnim"]["MFnClip"]["constructor"][0]["header"]


if __name__ == "__main__":
    main()

# coding=utf-8
import os
import sys
import json
DIR = os.path.dirname(__file__)
PYMEL = os.path.join(DIR, "pymel")
HTML = os.path.join(DIR, "PyMel_html", "generated")


pymel_module = ["pymel.core.datatypes",
"pymel.core.nodetypes",
"pymel.core.uitypes",
# "pymel.core.runtime",
"pymel.core",
"pymel.util",
"pymel.versions",
"pymel.mayautils",
"pymel.tools",
"pymel.api"]

# html_dict = {}
# for module in pymel_module:
#     html_dict[module] = []

html_dict = {"": [], "functions": {}, "classes": {}}
module_list = []
for root, dirs, files in os.walk(HTML):
    for html in files:
        if html.endswith(".html"):
            # NOTE 去掉 .html 后缀
            html = html[:-5]
            for module in pymel_module:
                if module in html and module != html:
                    module,_,func = html.rpartition(".")
                    # if not html_dict.has_key(module):
                    #     html_dict[module] = {"functions": [], "classes":[]}
                    TYPE = root.split(HTML)[-1][1:].replace("\\","/").split("/")[0]
                    # NOTE  如果 TYPE 为空，说明属于模块
                    if TYPE == '':
                        module_list.append(html)
                        break

                    if not html_dict[TYPE].has_key(module):
                        html_dict[TYPE][module] = []
                    

                    html_dict[TYPE][module].append(html)

                    break


for module in module_list:
    if module not in html_dict["functions"] and module not in html_dict["classes"]:
        html_dict[""].append(module)

path = os.path.join(DIR,"html3.json")
with open(path,'w') as f:
    json.dump(html_dict,f,indent=4)


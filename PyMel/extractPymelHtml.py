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

html_dict = {}
for root, dirs, files in os.walk(HTML):
    for html in files:
        if html.endswith(".html"):
            html = html[:-5]
            for module in pymel_module:
                if module in html and module != html:
                    module,_,func = html.rpartition(".")
                    if not html_dict.has_key(module):
                        html_dict[module] = []
                    html_dict[module].append(func)
                    break

path = os.path.join(DIR,"html.json")
with open(path,'w') as f:
    json.dump(html_dict,f,indent=4)


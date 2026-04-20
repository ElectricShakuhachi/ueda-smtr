from typing import TypedDict, List

class YamlData(TypedDict):
    name: str
    content: str

class Yamls(TypedDict):
    yamls: List[YamlData]

#{
#   "yamls" : [
#       {
#           "name" : "filename",
#           "content" : "yaml-content here"
#       },
#       {
#           "name" : "filename",
#           "content" : "yaml-content here"
#       }
#   ]
#}
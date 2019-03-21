from flask import json
from jsondiff import diff

def json_equal(a, b):
    for a_key in a:
        for b_key in b:
            if (a_key == b_key) & (a.get(a_key) != b.get(b_key)):
                return False

a = {'a': 1, 'b': 2, 'c': [5, 1]}
b = {'a': 1, 'b': 2, 'c': [5, 3]}

a_str = str(a)
b_str = str(b)

a_str = a_str.replace("\'","\"")
b_str = b_str.replace("\'","\"")

a_json = json.loads(a_str)
b_json = json.loads(b_str)
print (json_equal(a,b))
print (diff(a,b))
print (a, b)


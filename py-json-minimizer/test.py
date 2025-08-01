from json_minimizer import json_minimizable, JSONRestorer

schema = {
    "name": str,
    "age": int,
    "courses": [str],
    "advisor": {
        "name": str,
        "email": str
    }
}

@json_minimizable
def test():
    d = {
        "name": "muktadir",
        "age": 29,
        "courses": ["Algorithms", "Discrete"],
        "advisor": {
            "name": "Guanpeng Li",
            "email": "guanpeng-li@uiowa.edu"
        }
    }
    return d

minimized = test()
print(minimized)

restored = JSONRestorer(schema).restore(minimized)
print(restored)
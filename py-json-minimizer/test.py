from json_minimizer import json_minimizable, JSONRestorer

schema = {
    "name": str,
    "age": int,
    "courses": [{
        "name": str,
        "sh": int
    }],
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
        "courses": [
            {
                "name": "Algorithms",
                "sh": 3,
            },
            {
                "name": "Functional Programming",
                "sh": 3
            }
        ],
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
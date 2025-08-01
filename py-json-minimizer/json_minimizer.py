

_directly_convertible_types = (int, float, str, bool, tuple, list)

def _is_directly_convertible(data):
    return isinstance(data, _directly_convertible_types)

class JSONMinimizer:
    def __init__(self):
        pass

    def minimize(self, data):
        if _is_directly_convertible(data):
            return data
        elif isinstance(data, dict):
            return self._minimize_dict(data)
        elif self.is_user_defined(data):
            return self._minimize_user_defined_type(data)
        else:
            raise Exception("Type not supported")

    def is_user_defined(self, obj):
        return obj.__class__.__module__ != 'builtins'

    def _minimize_dict(self, data):
        result = []
        keys = list(data.keys())
        keys.sort()
        for key in keys:
            minimized_value = self.minimize(data[key])
            result.append(minimized_value)
        return result

    def _minimize_user_defined_type(self, data):
        """
        from ChatGPT:
        Django uses Python's json module under the hood.
        json module does not know how to serialize custom objects
        unless you manually convert them to dictionaries or use a custom encoder
         TypeError: Object of type CustomResult is not JSON serializable

        Also:
         https://docs.python.org/3.3/library/json.html#encoders-and-decoders
         https://stackoverflow.com/questions/10252010/serializing-class-instance-to-json

        So, I don't have to handle this case.
        """
        raise Exception("Objects of custom classes are not supported")

class JSONRestorer:
    def __init__(self, schema):
        self.schema = schema

    #todo: add validation logic
    def restore(self, data):
        return self._restore(self.schema, data)

    def _restore(self, schema, data):
        if schema in _directly_convertible_types:
            return data
        elif isinstance(schema, list):
            return data
        elif isinstance(schema, dict):
            return self._restore_dict(schema, data)
        else:
            raise Exception("Type not supported")

    def _restore_dict(self, schema, data):
        result = {}
        keys = list(schema.keys())
        keys.sort()
        i = 0
        for key in keys:
            restored_data = self._restore(schema[key], data[i])
            result[key] = restored_data

            i += 1
        return result

def json_minimizable(func):
    def minimize(*args, **kwargs):
        data = func(*args, **kwargs)
        return JSONMinimizer().minimize(data)
    return minimize



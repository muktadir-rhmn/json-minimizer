

_directly_convertible_types = (int, float, str, bool)

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
        elif isinstance(data, list) or isinstance(data, tuple):
            return self._minimize_list_tuple(data)
        elif self._is_user_defined(data):
            return self._minimize_user_defined_type(data)
        else:
            raise Exception("Type not supported")

    def _is_user_defined(self, obj):
        return obj.__class__.__module__ != 'builtins'

    def _minimize_dict(self, data):
        minimized_data = []
        keys = list(data.keys())
        keys.sort()
        for key in keys:
            minimized_value = self.minimize(data[key])
            minimized_data.append(minimized_value)
        return minimized_data

    def _minimize_list_tuple(self, data):
        minimized_data = []
        for item in data:
            minimized_item = self.minimize(item)
            minimized_data.append(minimized_item)
        return minimized_data

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
        elif isinstance(schema, list) or isinstance(schema, tuple):
            return self._restore_list_tuple(schema, data)
        elif isinstance(schema, dict):
            return self._restore_dict(schema, data)
        else:
            raise Exception("Type not supported")

    def _restore_dict(self, schema, data):
        if not isinstance(schema, dict):
            raise Exception("Schema is supposed to be a dictionary")

        if not isinstance(data, list) and not isinstance(data, tuple):
            raise Exception("Data is supposed to be a dictionary")

        result = {}
        keys = list(schema.keys())
        keys.sort()
        i = 0
        for key in keys:
            restored_data = self._restore(schema[key], data[i])
            result[key] = restored_data

            i += 1
        return result

    def _restore_list_tuple(self, schema, data):
        if not isinstance(schema, list) and not isinstance(schema, tuple):
            raise Exception("Schema is supposed to be a list or a tuple")

        if not isinstance(data, list) and not isinstance(data, tuple):
            raise Exception("Data is supposed to be a list or tuple")
        
        if len(schema) != 1:
            raise Exception("A list is supposed to have exactly one type inside it")

        item_schema = schema[0]
        restored_data = []
        for item in data:
            restored_item = self._restore(item_schema, item)
            restored_data.append(restored_item)
        return restored_data


def json_minimizable(func):
    def minimize(*args, **kwargs):
        data = func(*args, **kwargs)
        return JSONMinimizer().minimize(data)
    return minimize



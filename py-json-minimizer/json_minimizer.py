import abc
from abc import abstractmethod

"""
Follows Strategy design pattern
"""

class Minimizer(abc.ABC):
    """
    A single source of truth for handling a type of data.
    """

    @abstractmethod
    def can_handle(self, schema_or_data):
        pass

    @abstractmethod
    def minimize(self, data):
        pass

    @abstractmethod
    def restore(self, schema, data):
        pass

class _PrimitiveMinimizer(Minimizer):
    def __init__(self, generic_minimizer):
        self._generic_minimizer = generic_minimizer
        self._directly_convertible_types = (int, float, str, bool)

    def can_handle(self, schema_or_data):
        return (schema_or_data in self._directly_convertible_types
                or isinstance(schema_or_data, self._directly_convertible_types))

    def minimize(self, data):
        return data

    def restore(self, schema, data):
        return data

class _DictMinimizer(Minimizer):
    def __init__(self, generic_minimizer):
        self._generic_minimizer = generic_minimizer

    def can_handle(self, schema_or_data):
        return isinstance(schema_or_data, dict)

    def minimize(self, data):
        minimized_data = []
        keys = list(data.keys())
        keys.sort()
        for key in keys:
            minimized_value = self._generic_minimizer.minimize(data[key])
            minimized_data.append(minimized_value)
        return minimized_data

    def restore(self, schema, data):
        if not self.can_handle(schema):
            raise Exception("Schema is supposed to be a dict")

        if not isinstance(data, list) and not isinstance(data, tuple):
            raise Exception("Data is supposed to be a dictionary")

        result = {}
        keys = list(schema.keys())
        keys.sort()
        i = 0
        for key in keys:
            restored_data = self._generic_minimizer.restore(schema[key], data[i])
            result[key] = restored_data

            i += 1
        return result

class _ListTupleMinimizer(Minimizer):
    def __init__(self, generic_minimizer):
        self._generic_minimizer = generic_minimizer

    def can_handle(self, schema_or_data):
        return isinstance(schema_or_data, list) or isinstance(schema_or_data, tuple)

    def minimize(self, data):
        minimized_data = []
        for item in data:
            minimized_item = self._generic_minimizer.minimize(item)
            minimized_data.append(minimized_item)
        return minimized_data

    def restore(self, schema, data):
        if not self.can_handle(schema):
            raise Exception("Schema is supposed to be a list or a tuple")

        if not isinstance(data, list) and not isinstance(data, tuple):
            raise Exception("Data is supposed to be a list or tuple")

        if len(schema) != 1:
            raise Exception("A list is supposed to have exactly one type inside it")

        item_schema = schema[0]
        restored_data = []
        for item in data:
            restored_item = self._generic_minimizer.restore(item_schema, item)
            restored_data.append(restored_item)
        return restored_data

class _UserDefinedTypeMinimizer(Minimizer):
    def __init__(self, generic_minimizer):
        self._generic_minimizer = generic_minimizer

    def can_handle(self, schema_or_data):
        return schema_or_data.__class__.__module__ != 'builtins'

    def minimize(self, data):
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

    def restore(self, schema, data):
        raise Exception("Objects of custom classes are not supported")

class JSONMinimizer:
    def __init__(self):
        self.minimizers = []

        self.register(_PrimitiveMinimizer(self))
        self.register(_DictMinimizer(self))
        self.register(_ListTupleMinimizer(self))
        self.register(_UserDefinedTypeMinimizer(self))

    def register(self, minimizer: Minimizer):
        self.minimizers.append(minimizer)

    def minimize(self, data):
        for minimizer in self.minimizers:
            if minimizer.can_handle(data):
                return minimizer.minimize(data)

        raise Exception("Type not supported")

    def restore(self, schema, data):
        for minimizer in self.minimizers:
            if minimizer.can_handle(schema):
                return minimizer.restore(schema, data)

        raise Exception("Type not supported")

def json_minimizable(func):
    def minimize(*args, **kwargs):
        data = func(*args, **kwargs)
        return JSONMinimizer().minimize(data)
    return minimize



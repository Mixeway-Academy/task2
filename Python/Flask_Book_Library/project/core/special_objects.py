class ReadOnce:
    def __init__(self, initial=None):
        self._value = initial
        self._is_set = initial is not None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self._is_set:
            raise AttributeError("Value is read-once and cannot be changed.")
        self._value = new_value
        self._is_set = True

    def __str__(self):
        return str("Sensitive Data: ***")
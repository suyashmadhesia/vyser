from typing import Iterable


class Iterator(Iterable):

    def __init__(self, data) -> None:
        self._data = data
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._data):
            result = self._data[self._index]
            self._index += 1
            return result
        else:
            self._index = 0
            raise StopIteration

    def any(self):
        return len(self._data) > 0

    def last_or_default(self, default_value=None):
        return self._data[-1] if self.any() else default_value

    def extend(self, data):
        self._data.extend(data)
        return self

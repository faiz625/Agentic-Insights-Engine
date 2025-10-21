# Simple in-memory placeholder for future model registry integration
class ModelStore:
    def __init__(self):
        self._store = {}

    def put(self, key, obj):
        self._store[key] = obj

    def get(self, key, default=None):
        return self._store.get(key, default)

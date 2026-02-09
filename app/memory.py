class MemoryStore:
    def __init__(self):
        self.history = []

    def add(self, text: str):
        self.history.append(text)

    def recent(self, k=5):
        return self.history[-k:]

memory = MemoryStore()

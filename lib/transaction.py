class Action:
    def __init__(self, name, number, data):
        self.name = name
        self.number = number
        self.data = data


class Transaction:
    def __init__(self):
        pass

    def read(self):
        pass

    def write(self):
        pass

    def commit(self):
        pass
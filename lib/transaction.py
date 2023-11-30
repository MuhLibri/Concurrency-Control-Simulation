class Action:
    def __init__(self, name, number, data):
        self.name = name
        self.number = number
        self.data = data


class Transaction:
    def __init__(self, number, schedule):
        self.number = number
        self.actions = []
        for action in schedule:
            
            if (len(action) == 5):
                self.actions.append(Action(action[0], action[1], action[3]))
            else:
                self.actions.append(Action(action[0], action[1], ""))

    def read(self):
        pass

    def write(self):
        pass

    def commit(self):
        pass
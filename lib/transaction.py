class Action:
    def __init__(self, name, number, data):
        self.name = name
        self.number = int(number)
        self.data = data


class Transaction:
    def __init__(self, number, schedule):
        self.number = number
        self.data = []
        self.actions = []
        for action in schedule:
            if (int(action[1]) == number):
                if (len(action) == 5):
                    self.actions.append(Action(action[0], action[1], action[3]))
                    self.data.append(action[3])
                else:
                    self.actions.append(Action(action[0], action[1], ""))

    def read(self):
        pass

    def write(self):
        pass

    def commit(self):
        pass


class Timestamp:
    def __init__(self, name, number):
        self.name = name
        self.number = number


def get_transaction_numbers(schedule):
    transaction_numbers = []
    for action in schedule:
        if (not (action.number in transaction_numbers)):
            transaction_numbers.append(action.number)

    transaction_numbers.sort()
    return transaction_numbers
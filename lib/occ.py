

class OCC:
    def __init__(self, schedule):
        self.schedule = schedule

    def __processAction(self, action):
        if (action.name == "R"):
            print(f"Transaction {action.number} read from {action.data}")
        elif (action.name == "W"):
            print(f"Transaction {action.number} write {action.data}")
        else:
            print(f"Transaction {action.number} commited")

    def __validate(self):
        pass

    def run(self):
        print("Optimistic Concurency Control Started")
        
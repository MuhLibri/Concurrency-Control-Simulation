from .transaction import Action, Timestamp


class OCC:
    def __init__(self, schedule, transaction_numbers):
        self.schedule = schedule

    def set_schedule(self, schedule):
        self.schedule = schedule

    def __processAction(self, action):
        if (action.name == "R"):
            print(f"Transaction {action.number} read {action.data}")
        elif (action.name == "W"):
            print(f"Transaction {action.number} write {action.data}")
        else:
            print(f"Transaction {action.number} commited")

    def __is_transaction_write(self, number, data):
        for s in self.schedule:
            if (s.name == "W" and s.number == number and s.data == data):
                return True
        return False

    def __get_transaction_timestamp(self, timestamps, number):
        current_timestamp = 0
        for t in timestamps:
            if (t.name == "Validation"):
                if (t.number == number):
                    return current_timestamp
                else:
                    current_timestamp += 1
        
        return -1

    def __is_valid(self, timestamps):
        current = timestamps[-1]
        prev1 = timestamps[-2]
        if (len(timestamps) == 2):
            return True
        else:
            prev2 = timestamps[-3]
            # Check timestamp before validation
            if (prev1.name == "Start" and prev1.number == current.number and prev2.name == "Finish"):
                return True
            elif (prev1.name == "Finish" and prev1.number < current.number and prev2.name == "Start" and prev2.number == current.number):
                # Check used the same resource or not
                for s in self.schedule:
                    if (s.name == "R" and s.number == current.number):
                        if (self.__is_transaction_write(current.number, s.data)):
                            print("Here1")
                            return False
                return True
            else:
                print("Here2")
                return False



    def run(self):
        print("Optimistic Concurency Control Started")
        print("-------------------------------------")
        schedule = self.schedule
        timestamps = []
        timestamps_number = []
        write_list = []
        final_schedule = []
        last_commit = -1

        while len(schedule) != 0:
            current_action = schedule.pop(0)
            if not (current_action.number in timestamps_number):
                timestamps.append(Timestamp("Start", current_action.number))
                timestamps_number.append(current_action.number)
                print(f"Started transaction {current_action.number}")

            if (current_action.name == "R"):
                print(f"Transaction {current_action.number} read {current_action.data}")
            elif (current_action.name == "W"):
                write_list.append(current_action)
            else:
                timestamps.append(Timestamp("Validation", current_action.number))
                print(f"Validating transaction {current_action.number}")
                if (self.__is_valid(timestamps)):
                    for w in write_list:
                        if (current_action.number == w.number):
                            print(f"Transaction {w.number} write {w.data}")
                    timestamps.append(Timestamp("Finish", current_action.number))
                    print(f"Finished transaction {current_action.number}")
                    print(f"Transaction {current_action.number} commited")
                else:
                    #abort
                    print(f"Transaction {current_action.number} aborted")

            final_schedule.append(current_action)
        print("-------------------------------------")
        print("Optimistic Concurency Control Finished")

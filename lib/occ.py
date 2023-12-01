from .transaction import Action, Timestamp


class OCC:
    def __init__(self, schedule, transaction_numbers):
        self.schedule = schedule
        self.transaction_numbers = transaction_numbers

    def set_schedule(self, schedule):
        self.schedule = schedule

    def __is_transaction_write(self, number, data):
        for s in self.schedule:
            if (s.name == "W" and s.number != number and s.data == data):
                return True
        return False

    def __get_all_action(self, number):
        actions = []
        for s in self.schedule:
            if (s.number == number):
                actions.append(s)

        return actions

    def __is_valid(self, timestamps, transaction_numbers):
        i = len(timestamps)-2
        validate = timestamps[-1]
        current_timestamp = timestamps[i]

        while (not (current_timestamp.name == "Start" and current_timestamp.number == validate.number)):
            if (current_timestamp.name == "Finish"):
                for s in self.schedule:
                    if (s.name == "R" and s.number == validate.number):
                        if (self.__is_transaction_write(validate.number, s.data)):
                            return False
            i -= 1
            current_timestamp = timestamps[i]

        if (transaction_numbers[0] == validate.number):
            return True
        else:
            return False

    def run(self):
        print("Optimistic Concurency Control Started")
        print("----------------------------------------------")
        schedule = self.schedule.copy()
        transaction_numbers = self.transaction_numbers.copy()
        timestamps = []
        timestamps_number = []
        write_list = []
        final_schedule = []

        while len(schedule) != 0:
            current_action = schedule.pop(0)
            if not (current_action.number in timestamps_number):
                timestamps.append(Timestamp("Start", current_action.number))
                timestamps_number.append(current_action.number)
                print(f"Started transaction {current_action.number}")

            if (current_action.name == "R"):
                print(f"[Transaction {current_action.number}] read {current_action.data}")
                final_schedule.append(f"R{current_action.number}({current_action.data})")
            elif (current_action.name == "W"):
                write_list.append(current_action)
            else:
                timestamps.append(Timestamp("Validation", current_action.number))
                print(f"Validating transaction {current_action.number}")
                if (self.__is_valid(timestamps, transaction_numbers)):
                    transaction_numbers.pop(0)
                    for w in write_list:
                        if (current_action.number == w.number):
                            print(f"[Transaction {w.number}] write {w.data}")
                            final_schedule.append(f"W{w.number}({w.data})")
                    timestamps.append(Timestamp("Finish", current_action.number))
                    print(f"Finished transaction {current_action.number}")
                    print(f"[Transaction {current_action.number}] commited")
                    final_schedule.append(f"C{current_action.number}")
                else:
                    #abort
                    print(f"Transaction {current_action.number} aborted")
                    final_schedule.append(f"A{current_action.number}")
                    if (current_action.number == transaction_numbers[0]):
                        i = 0
                    else:
                        i = 0
                        while (not (schedule[i].name == "C" and schedule[i].number == transaction_numbers[0])):
                            i += 1
                        i += 1

                    rolled_back_actions = self.__get_all_action(current_action.number)
                    for action in rolled_back_actions:
                        schedule.insert(i, action)
                        i += 1

                    timestamps_number.remove(current_action.number)
                    
        print("----------------------------------------------")
        print("Optimistic Concurency Control Finished\n")

        return final_schedule

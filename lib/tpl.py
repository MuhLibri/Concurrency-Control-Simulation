from .transaction import Action, Timestamp, Lock, LockType, can_acquire_lock, update_acquired_lock
from typing import List


class TPL: # Two Phase Locking Protocol
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
        print("Two Phase Locking Concurency Control Started")
        print("----------------------------------------------")
        schedule = self.schedule.copy()
        transaction_numbers = self.transaction_numbers.copy()
        write_list = []
        final_schedule = []

        transaction_ran = []

        transaction_blocked = []
        action_blocked = []

        lock_acquired : List[Lock] = []

        while len(schedule) != 0:
            current_action : Action = schedule.pop(0)

            print(current_action.name, '->>', len(schedule))
            print('asdasd', len(schedule), len(action_blocked))
            if (len(schedule) == 0 and len(action_blocked) != 0):
                print(action_blocked, 'sini2')
                schedule = action_blocked
                action_blocked = []

                transaction_blocked = []

                # print(schedule)

            # If transaction blocked
            if current_action.number in transaction_blocked:
                action_blocked.append(current_action)

                continue

            # New Transaction Start
            if not (current_action.number in transaction_ran):
                transaction_ran.append(current_action.number)
                print(f"Started transaction {current_action.number}")

            # Read Operation
            if (current_action.name == "R"):
                # can we acquire S lock / can we read
                if can_acquire_lock(lock_acquired, LockType['S'], current_action.number, current_action.data) :
                    # update lock acquired
                    update_acquired_lock(lock_acquired, current_action)

                    print(lock_acquired)
                    # can read
                    print(f"[Transaction {current_action.number}] read {current_action.data}")
                    final_schedule.append(f"R{current_action.number}({current_action.data})")

                    continue
                
                # put it on hold
                action_blocked.append(current_action)
                print(action_blocked, 'sini')

                # mark transaction on hold
                if not (current_action.number in transaction_blocked):
                    transaction_blocked.append(current_action.number)

                # print(f"Resource {current_action.data} is being Exclusively Locked by Transaction {current_action.number}")
                print(f"[Blocked] - [Transaction {current_action.number}] read {current_action.data}")
                print(f"Resource {current_action.data} is being Exclusively Locked")
                
            # Write Operation
            elif (current_action.name == "W"):
                # can we acquire X lock / can we write
                if can_acquire_lock(lock_acquired, LockType['X'], current_action.number, current_action.data):
                    _new_lock = update_acquired_lock(lock_acquired, current_action)

                    final_schedule.append(f"{_new_lock.type.name}L{current_action.number}({current_action.data})")

                    print(f"[Transaction {current_action.number}] write {current_action.data}")
                    final_schedule.append(f"W{current_action.number}({current_action.data})")

                    continue

                print(f"Resource {current_action.data} is being Locked by a Transaction")
                print(f"[Blocked] - [Transaction {current_action.number}] write {current_action.data}")

                if not current_action.number in transaction_blocked:
                    transaction_blocked.append(current_action.number)

                action_blocked.append(current_action)
                # write_list.append(current_action)

             # Commit Operation
            elif (current_action.name == "C"):
                print("bef", lock_acquired)
                _to_remove = []
                # remove all locks
                for i in range(len(lock_acquired)):
                    if lock_acquired[i].number == current_action.number:
                        _to_remove.append(i)

                # remove from back, carefully
                for i in _to_remove[::-1]:
                    # print(i)
                    final_schedule.append(f"UL{current_action.number}({lock_acquired[i].data})")
                    lock_acquired.pop(i)

                print("aft", lock_acquired)
            else:
                print('else')

            
                    
        print("----------------------------------------------")
        print("Two Phase Locking Concurency Control Finished\n")

        return final_schedule

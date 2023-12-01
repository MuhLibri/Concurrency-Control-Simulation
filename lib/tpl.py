from .transaction import Action, Lock, LockType, can_acquire_lock, update_acquired_lock
from typing import List


class TPL: # Two Phase Locking Protocol
    def __init__(self, schedule):
        self.schedule = schedule

    def run(self):
        print("Two Phase Locking Concurency Control Started")
        print("----------------------------------------------")
        schedule = self.schedule.copy()
        final_schedule = []

        transaction_ran = []

        transaction_blocked = []
        action_blocked = []

        lock_acquired : List[Lock] = []

        while len(schedule) > 0:
            current_action : Action = schedule.pop(0)

            if (len(schedule) == 0 and len(action_blocked) != 0):
                schedule = action_blocked
                action_blocked = []

                transaction_blocked = []

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
                    _new_lock = update_acquired_lock(lock_acquired, current_action)

                    print(f"[Transaction {current_action.number}] acquiring lock {_new_lock}")
                    final_schedule.append(f"{_new_lock.type.name}L{current_action.number}({current_action.data})")

                    # can read
                    print(f"[Transaction {current_action.number}] read {current_action.data}")
                    final_schedule.append(f"R{current_action.number}({current_action.data})")

                    continue
                
                # put it on hold
                action_blocked.append(current_action)

                # mark transaction on hold
                if not (current_action.number in transaction_blocked):
                    transaction_blocked.append(current_action.number)

                print(f"[Blocked] - [Transaction {current_action.number}] read {current_action.data}")
                print(f"Resource {current_action.data} is being Exclusively Locked")
                
            # Write Operation
            elif (current_action.name == "W"):
                # can we acquire X lock / can we write
                if can_acquire_lock(lock_acquired, LockType['X'], current_action.number, current_action.data):
                    _new_lock = update_acquired_lock(lock_acquired, current_action)

                    print(f"[Transaction {current_action.number}] acquiring lock {_new_lock}")
                    final_schedule.append(f"{_new_lock.type.name}L{current_action.number}({current_action.data})")

                    print(f"[Transaction {current_action.number}] write {current_action.data}")
                    final_schedule.append(f"W{current_action.number}({current_action.data})")

                    continue

                print(f"Resource {current_action.data} is being Locked by a Transaction")
                print(f"[Blocked] - [Transaction {current_action.number}] write {current_action.data}")

                if not current_action.number in transaction_blocked:
                    transaction_blocked.append(current_action.number)

                action_blocked.append(current_action)

             # Commit Operation
            elif (current_action.name == "C"):

                print(f"[Transaction {current_action.number}] commit {current_action.number}")
                final_schedule.append(f"C{current_action.number}")
            
                _to_remove = []
                # remove all locks
                for i in range(len(lock_acquired)):
                    if lock_acquired[i].number == current_action.number:
                        _to_remove.append(i)

                # remove from back, carefully
                for i in _to_remove[::-1]:
                    print(f"[Transaction {current_action.number}] releasing lock {lock_acquired[i]}")
                    final_schedule.append(f"UL{current_action.number}({lock_acquired[i].data})")
                    lock_acquired.pop(i)

            # if len(schedule) == 0:
            #     final_schedule.append(current_action)    
        
        print("----------------------------------------------")
        print("Two Phase Locking Concurency Control Finished\n")

        return final_schedule

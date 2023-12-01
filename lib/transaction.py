from enum import Enum
from typing import List 

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

class LockType(Enum):
    S = 1
    X = 2

class Lock:
    def __init__(self, type : LockType, number : int, data : str):
        self.type = type
        self.number = number
        self.data = data

def can_acquire_lock(acquired_list : List[Lock], type : LockType, number : int, data : str):
    if type == LockType['X']:
        for _lock in acquired_list:
            # another Transaction acquired the lock
            if _lock.data == data and _lock.number != number:
                return False
            
        return True
        
    else: # LockType['S']
        for _lock in acquired_list:
            # another Transaction acquired X Lock of it
            if _lock.data == data and _lock.number != number and _lock.type == LockType['X']:
                return False
            
        return True

def is_there_lock(acquired_list : List[Lock], type : LockType, number : int, data : str):
    for _lock in acquired_list:
        if _lock.type == type and _lock.number == number and _lock.data == data:
            return False
        
    return True

# def need_acquire_lock(acquired_list : List[Lock], action : Action):
#     if action.name == 'R':
#         if 
def update_acquired_lock(acquired_list : List[Lock], action : Action):
    if action.name == 'R':
        # can we acquire S lock
            if can_acquire_lock(acquired_list, LockType['S'], action.number, action.data) :
                # is the corresponding lock already exists
                if not (is_there_lock(acquired_list, LockType['X'], action.number, action.data) or is_there_lock(acquired_list, LockType['S'], action.number, action.data)):
                    acquired_list.append(Lock(LockType['S'], action.number, action.data))

    elif action.name == 'W':
         # can we acquire X lock
            if can_acquire_lock(acquired_list, LockType['X'], action.number, action.data) :
                # is the corresponding lock already exists
                if not (is_there_lock(acquired_list, LockType['X'], action.number, action.data)):
                    acquired_list.append(Lock(LockType['S'], action.number, action.data))
    
                        
def get_transaction_numbers(schedule):
    transaction_numbers = []
    for action in schedule:
        if (not (action.number in transaction_numbers)):
            transaction_numbers.append(action.number)

    transaction_numbers.sort()
    return transaction_numbers
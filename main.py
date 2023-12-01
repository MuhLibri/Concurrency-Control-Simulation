from lib.transaction import Action, get_transaction_numbers
from lib.occ import OCC
from lib.tpl import TPL
from lib.utils import readFile




if __name__ == "__main__":
    schedule_raw = readFile("input/tc6.txt")
    schedule = []

    print("Original Schedule:")
    print(schedule_raw)
    print()

    for action in schedule_raw:
        bracket_index = action.find("(")
        if (bracket_index != -1):
            schedule.append(Action(action[0], action[1:bracket_index], action[bracket_index+1]))
        else:
            schedule.append(Action(action[0], action[1:len(action)], ""))

    transaction_numbers = get_transaction_numbers(schedule)

    cc = OCC(schedule, transaction_numbers)
    cc = TPL(schedule, transaction_numbers)


    final_schedule = cc.run()

    print("Final Schedule:")
    print(final_schedule)
from lib.transaction import Action, get_transaction_numbers
from lib.occ import OCC
# from lib.utils import readFile




if __name__ == "__main__":
    schedule_raw = utils.readFile("input/s1.txt")
    schedule = []

    print(schedule_raw)

    # s = transaction.Transaction(1, schedule)
    # print(s.data)
    # for s in s.actions:
    #     print()
    #     print(s.name)
    #     print(s.number)
    #     print(s.data)

    # for s in schedule_raw:
    #     schedule.append(transaction.Action())

    for action in schedule_raw:
        if (len(action) == 5):
            schedule.append(Action(action[0], action[1], action[3]))
        else:
            schedule.append(Action(action[0], action[1], ""))

    transaction_numbers = get_transaction_numbers(schedule)
    print(transaction_numbers)

    a = OCC(schedule, transaction_numbers)


    a.run()
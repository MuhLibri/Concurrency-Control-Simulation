import lib.transaction as transaction
import lib.occ as occ
import lib.utils as utils




if __name__ == "__main__":
    schedule_raw = utils.readFile("input/tc6.txt")
    schedule = []

    print("Original Schedule:")
    print(schedule_raw)
    print()

    for action in schedule_raw:
        bracket_index = action.find("(")
        if (bracket_index != -1):
            schedule.append(transaction.Action(action[0], action[1:bracket_index], action[bracket_index+1]))
        else:
            schedule.append(transaction.Action(action[0], action[1:len(action)], ""))

    transaction_numbers = transaction.get_trannsaction_numbers(schedule)

    cc = occ.OCC(schedule, transaction_numbers)
    final_schedule = cc.run()

    print("Final Schedule:")
    print(final_schedule)
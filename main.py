import lib.transaction as transaction
import lib.occ as occ
import lib.utils as utils




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
            schedule.append(transaction.Action(action[0], action[1], action[3]))
        else:
            schedule.append(transaction.Action(action[0], action[1], ""))

    a = occ.OCC(schedule)

    a.run()
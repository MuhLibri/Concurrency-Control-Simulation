import lib.transaction as transaction
import lib.occ as occ
import lib.utils as utils




if __name__ == "__main__":
    schedule = utils.readFile("input/s1.txt")
    print(schedule)
    for s in schedule:
        a = transaction.Action(s[0], s[1], s[3])
        print(a.name, a.number, a.data)

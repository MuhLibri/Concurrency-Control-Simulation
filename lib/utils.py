def readFile(filePath):
    try:
        file = open(filePath, "r")
        schedule = file.read()
        schedule = schedule.split(";")
        schedule = [x.strip() for x in schedule]
        return schedule
    except:
        print("File not found, exiting...")
        exit(1)
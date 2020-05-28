import re


def time_judger(lines, ID, time_dict, WrongLog, single_time):
    your_time = float(lines[-1].split("]")[0].strip("[").strip())
    print(ID+"'s time: "+str(your_time))
    single_time[ID] = your_time
    time_dict[ID] += your_time


def process(lines, data):
    actions = []
    people = {}
    for i in range(len(lines)):
        #print(lines[i], end="")
        line = lines[i].replace("--", "-$").strip()
        new_dict = {}
        new_dict["time"] = float(line.split("]")[0].strip("[").strip())
        split_list = line.split("-")
        new_dict["action"] = split_list[0].split("]")[1]
        new_dict["floor"] = int(split_list[-2].replace("$", "-"))
        new_dict["elevator"] = split_list[-1]
        if new_dict["action"] in ["IN", "OUT"]:
            new_dict["id"] = int(split_list[-3])
            if new_dict["id"] not in people:
                people[new_dict["id"]] = {new_dict["action"]: new_dict["floor"]}
            else:
                people[new_dict["id"]][new_dict["action"]] = new_dict["floor"]
        actions.append(new_dict)

    requests = {}
    for line in data:
        if line.startswith("[0.0]"):
            continue
        if line == "END\n":
            break
        line = line.replace("--", "-$")
        split_list = line.split("-")
        id = int(split_list[0].split("]")[1])
        time = float(line[1:].split(']')[0])
        fro = int(split_list[2].replace("$", "-"))
        to = int(split_list[4].replace("$", "-"))
        requests[id] = {"from": fro, "to": to, "time": time}

    return actions, people, requests


def check_people_in_elevator(actions, WrongLog):
    passengers = {"A": [], "B": [], "C": [], "D": [], "E": []}
    for action in actions:
        elev = action["elevator"]
        if action["action"] == "IN":
            if action["id"] in passengers[elev]:
                print("In twice!")
                print("In twice!", file=WrongLog)
                return False
            passengers[elev].append(action["id"])
            if len(passengers[elev]) > 7:
                print("Too Many People in elevator {}!".format(elev))
                print("Too Many People in elevator {}!".format(elev), file=WrongLog)
                return False
        elif action["action"] == "OUT":
            if action["id"] not in passengers[elev]:
                print("Out from nowhere!")
                print("Out from nowhere!", file=WrongLog)
                return False
            passengers[elev].remove(action["id"])
    return True


def judge(data, lines, ID, time_dict, WrongLog, single_time):
    #print(data)
    time_judger(lines, ID, time_dict, WrongLog, single_time)
    actions, people, requests = process(lines, data)
    floors_range = list(range(1, 17))
    floors_range.extend([-1, -2, -3])

    for id in requests.keys():
        if id not in people.keys():
            print("Person not found!"+str(id))
            return False
        if "OUT" not in people[id].keys() or people[id]["OUT"] != requests[id]["to"]:
            print("Wrong destination!"+str(id))
            return False
        if "IN" not in people[id].keys() or people[id]["IN"] != requests[id]["from"]:
            print("Wrong start point!"+str(id))
            return False

    for action in actions:
        if action["floor"] not in floors_range:
            print("Floor out of range!")
            print("Floor out of range!", file=WrongLog)
            return False

        if "id" in action.keys() and action["id"] not in people.keys():
            print("Wrong ID!")
            print("Wrong ID!", file=WrongLog)
            return False

        #for i in range(len(floors)-1):
        #    if floors[i+1]-floors[i] > 1 or floors[i+1]-floors[i] < -1:
        #        print("Wrong floor movement!")
        #        return False

    if not check_people_in_elevator(actions, WrongLog):
        return False
    if not check_time(actions, WrongLog):
        return False

    return True


def check_time(actions, WrongLog):
    elevator_dict = {"A": [], "B": [], "C": [], "D": [], "E": []}
    for action in actions:
        elevator_dict[action["elevator"]].append(action)

    for elev in elevator_dict.keys():
        actions_elev = elevator_dict[elev]
        for i in range(len(actions_elev)-1):
            if actions_elev[i]["action"] == "ARRIVE" and actions_elev[i+1]["action"] == "ARRIVE":
                if actions_elev[i+1]["time"]-actions_elev[i]["time"] < 0.399999:
                    print("Arrive too fast!")
                    print("Arrive too fast!", file=WrongLog)
                    return False
            if actions_elev[i]["action"] == "OPEN":
                for j in range(i+1, len(actions_elev)):
                    if actions_elev[j]["action"] == "CLOSE":
                        if actions_elev[j]["time"]-actions_elev[i]["time"] < 0.399999:
                            print("Close too fast!")
                            print("Close too fast!", file=WrongLog)
                            return False
                        break
            if actions_elev[i]["action"] == "CLOSE":
                for j in range(i+1, len(actions_elev)):
                    if actions_elev[j]["action"] == "ARRIVE":
                        if actions_elev[j]["time"]-actions_elev[i]["time"] < 0.399999:
                            print("Arrive after close too fast!")
                            print("Arrive after close too fast!", file=WrongLog)
                            return False
                        break
            if (actions_elev[i+1]["floor"]-actions_elev[i]["floor"] > 1 and
                    actions_elev[i]["floor"] != -1) or \
                (actions_elev[i+1]["floor"]-actions_elev[i]["floor"] < -1 and
                 actions_elev[i+1]["floor"] != -1):
                print("Wrong floor movement!" + str(actions_elev[i+1]))
                print("Wrong floor movement!" + str(actions_elev[i+1]), file=WrongLog)
                return False

    return True
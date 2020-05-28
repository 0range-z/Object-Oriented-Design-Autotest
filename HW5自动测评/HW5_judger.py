import re
from os import popen


def calculate_base_time(data, time_dict):
    f = open("judge_data.txt", "w")
    for line in data:
        if line == "\n":
            continue
        if line == "END\n":
            break
        f.write(line)
    f.close()
    proc = popen("datacheck_win.exe -i judge_data.txt")
    ans = proc.read()
    try:
        max_time = int(ans.split(" ")[-1])
        base_time = int(ans.split(" ")[-5].strip(","))
    except:
        return 0,0
    time_dict["base"] += base_time
    time_dict["max"] += max_time
    print("max time: " + str(max_time))
    print("base time: " + str(base_time))
    return max_time, base_time


def time_judger(lines, max_time, base_time, ID, time_dict, WrongLog):

    your_time = float(lines[-1].split("]")[0].strip("[").strip())
    print(ID + "'s time: " + str(your_time))
    time_dict[ID] += your_time

    if your_time - base_time > 40:################
        print("TLE!",file=WrongLog)
        print("TLE")
        return False
    return True


def process(lines, data):
    actions = []
    string = ""
    floors = []
    people = {}
    for i in range(len(lines)):
        new_dict = {}
        new_dict["time"] = float(lines[i].split("]")[0].strip("[").strip())
        split_list = lines[i].split("-")
        new_dict["action"] = split_list[0].split("]")[1]
        new_dict["floor"] = int(split_list[-1])
        floors.append(new_dict["floor"])
        if new_dict["action"] in ["IN", "OUT"]:
            new_dict["id"] = int(split_list[-2])
            string += new_dict["action"][0].lower()
            if new_dict["id"] not in people:
                people[new_dict["id"]] = {new_dict["action"]: new_dict["floor"]}
            else:
                people[new_dict["id"]][new_dict["action"]] = new_dict["floor"]
        else:
            string += new_dict["action"][0]
        actions.append(new_dict)

    requests = {}
    for line in data:
        if line == "END\n":
            break
        split_list = line.split("-")
        id = int(split_list[0].split("]")[1])
        time = float(line[1:].split(']')[0])
        fro = int(split_list[2])
        to = int(split_list[4])
        requests[id] = {"from": fro, "to": to, "time": time}

    return actions, people, string, floors, requests


def check_people_in_elevator(actions):
    passengers = []
    for action in actions:
        if action["action"] == "IN":
            if action["id"] in passengers:
                print("In twice!")
                return False
            passengers.append(action["id"])
        elif action["action"] == "OUT":
            if action["id"] not in passengers:
                print("Out from nowhere!")
                return False
            passengers.remove(action["id"])
    return True


def check_time(actions):
    for i in range(len(actions) - 1):
        if actions[i]["action"] == "ARRIVE" and actions[i + 1]["action"] == "ARRIVE":
            if actions[i + 1]["time"] - actions[i]["time"] < 0.399999:
                print("Arrive too fast!")
                print(actions[i + 1]["time"])
                print(actions[i]["time"])
                return False
        if actions[i]["action"] == "OPEN":
            for j in range(i + 1, len(actions)):
                if actions[j]["action"] == "CLOSE":
                    if actions[j]["time"] - actions[i]["time"] < 0.399999:
                        print("Close too fast!")
                        return False
                    break
    return True


def judge(lines, data):
    actions, people, string, floors, requests = process(lines, data)
    for id in requests.keys():
        if id not in people.keys():
            print("Person not found!" + str(id))
            return False
        if "OUT" not in people[id].keys() or people[id]["OUT"] != requests[id]["to"]:
            print("Wrong destination!" + str(id))
            return False
        if "IN" not in people[id].keys() or people[id]["IN"] != requests[id]["from"]:
            print("Wrong start point!" + str(id))
            return False

    for action in actions:
        if action["floor"] not in range(1,16):
            print("Floor out of range!")
            return False

        if "id" in action.keys() and action["id"] not in people.keys():
            print("Wrong ID!")
            return False

        for i in range(len(floors) - 1):
            if floors[i+1] - floors[i] > 1 or floors[i+1] - floors[i] < -1:
                print("Wrong floor movement!")
                return False

        if not re.match("(A*(O[io]*C))*",string):
            print("Wrong action sequence!")
            return False

        if not check_people_in_elevator(actions):
            return False
        if not check_time(actions):
            return False

    return True
    # except Exception:
    # print("Error Encountered during judge")
    # return False

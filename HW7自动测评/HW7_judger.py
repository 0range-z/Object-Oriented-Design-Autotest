import re
from HW7_generator import generate, generate_coverage


def time_judger(lines, ID, time_dict, single_elevator_time, requests, people):
    elev_time = float(lines[-1].split("]")[0].strip("[").strip())
    wait_time = wait_time_calculate(requests, people)
    your_time = elev_time+wait_time
    print("{}: elevator time: {:.2f}  wait time: {:.2f} total: {:.2f}".format(ID, elev_time, wait_time, your_time))
    single_elevator_time[ID] = elev_time
    time_dict[ID] += your_time


def wait_time_calculate(requests, people):
    wait_time = 0
    for p_id in people.keys():
        for r_id in requests.keys():
            if r_id == p_id:
                wait_time += (people[p_id][-1]["time"]-requests[r_id]["time"])
    return wait_time


def process(lines, data):
    actions = []
    people = {}
    elevators = {"A": "A", "B": "B", "C": "C"}
    requests = {}

    for line in data:
        if line == "END\n":
            break
        if line.find("ADD-ELEVATOR") != -1:
            split_list = line.split("-")
            id = split_list[0].split("]")[1]
            type = split_list[-1].strip("\n")
            elevators[id] = type
        else:
            line = line.replace("--", "-$")
            split_list = line.split("-")
            id = int(split_list[0].split("]")[1])
            time = float(line[1:].split(']')[0])
            fro = int(split_list[2].replace("$", "-"))
            to = int(split_list[4].replace("$", "-"))
            requests[id] = {"from": fro, "to": to, "time": time}

    for i in range(len(lines)):
        #print(lines[i], end="")
        line = lines[i].replace("--", "-$").strip()
        new_dict = {}
        new_dict["time"] = float(line.split("]")[0].strip("[").strip())
        split_list = line.split("-")
        new_dict["action"] = split_list[0].split("]")[1]

        #print(split_list[-2].replace("$", "-"))

        new_dict["floor"] = int(split_list[-2].replace("$", "-"))
        new_dict["elevator"] = split_list[-1]
        if new_dict["action"] in ["IN", "OUT"]:
            new_dict["id"] = int(split_list[-3])
            if new_dict["id"] not in people:
                people[new_dict["id"]] = [new_dict]
            else:
                people[new_dict["id"]].append(new_dict)
        actions.append(new_dict)

    return actions, people, requests, elevators


def judge(data, lines, ID, time_dict, WrongLog, single_time):
    #print(data)
    actions, people, requests, elevators = process(lines, data)
    floors_range = list(range(1, 21))
    floors_range.extend([-1, -2, -3])

    for id in requests.keys():
        if id not in people.keys():
            print("Person not found!"+str(id))
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

    if not check_people_in_elevator(actions, WrongLog, elevators):
        return False
    if not check_time_and_floor(actions, WrongLog, elevators):
        return False
    if not check_people(people, requests, WrongLog):
        return False

    time_judger(lines, ID, time_dict, single_time, requests, people)
    return True


def check_people_in_elevator(actions, WrongLog, elevators):
    passengers = {"A": [], "B": [], "C": [], "X1": [], "X2": [], "X3": []}
    max_size = {"A": 6, "B": 8, "C": 7}
    for action in actions:
        elev = action["elevator"].strip()

        if action["action"] == "IN":
            if action["id"] in passengers[elev]:
                print("In twice!")
                print("In twice!", file=WrongLog)
                return False
            passengers[elev].append(action["id"])
            if len(passengers[elev]) > max_size[elevators[elev]]:
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


def check_time_and_floor(actions, WrongLog, elevators):
    elevator_dict = {"A": [], "B": [], "C": [], "X1": [], "X2": [], "X3": []}
    arrive_time = {"A": 0.4, "B": 0.5, "C": 0.6}
    arrive_floors = {"A": [-3, -2, -1, 1, 15, 16, 17, 18, 19, 20],
                     "B": [-2, -1, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                     "C": [1, 3, 5, 7, 9, 11, 13, 15]}

    for action in actions:
        elevator_dict[action["elevator"]].append(action)

    for elev in elevator_dict.keys():
        actions_elev = elevator_dict[elev]
        for i in range(len(actions_elev)-1):
            if actions_elev[i]["action"] == "ARRIVE" and actions_elev[i+1]["action"] == "ARRIVE":
                if actions_elev[i+1]["time"]-actions_elev[i]["time"] < arrive_time[elevators[elev]]-0.00001:
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
                        if actions_elev[j]["time"]-actions_elev[i]["time"] < arrive_time[elevators[elev]]-0.00001:
                            print("Arrive after close too fast!")
                            print("Arrive after close too fast!", file=WrongLog)
                            return False
                        break
            if (actions_elev[i+1]["floor"]-actions_elev[i]["floor"] > 1 and
                actions_elev[i]["floor"] != -1) or \
                    (actions_elev[i+1]["floor"]-actions_elev[i]["floor"] < -1 and
                     actions_elev[i+1]["floor"] != -1):
                print("Wrong floor movement! "+str(actions_elev[i+1]))
                print("Wrong floor movement! "+str(actions_elev[i+1]), file=WrongLog)
                return False

        for i in range(len(actions_elev)):
            if actions_elev[i]["action"] != "ARRIVE" and actions_elev[i]["floor"] not in arrive_floors[elevators[elev]]:
                print("Stop at wrong floor! floor:"+str(actions_elev[i]["floor"])+"elev: "+str(actions_elev[i]))
                print("Stop at wrong floor! floor:"+str(actions_elev[i]["floor"])+"elev: "+str(actions_elev[i]),
                      file=WrongLog)
                return False

    return True


def check_people(people, requests, WrongLog):
    for id in people.keys():
        source = requests[id]["from"]
        target = requests[id]["to"]
        movements = people[id]
        if len(movements)%2 == 1:
            print("Person movements are odd number! person"+str(id))
            print("Person movements are odd number! person"+str(id),
                  file=WrongLog)
            return False
        i = 0
        while i < len(movements)-1:
            if movements[i]["action"] != "IN" or movements[i+1]["action"] != "OUT":
                print("In and out movements mismatch! person"+str(id))
                print("In and out movements mismatch! person"+str(id),
                      file=WrongLog)
                return False
            if movements[i]["elevator"] != movements[i+1]["elevator"]:
                print("In and out elevator mismatch! person"+str(id))
                print("In and out elevator mismatch! person"+str(id),
                      file=WrongLog)
                return False
            if i+1 != len(movements)-1:
                if movements[i+1]["floor"] != movements[i+2]["floor"]:
                    print("Transfer floor mismatch! person"+str(id))
                    print("Transfer floor mismatch! person"+str(id),
                          file=WrongLog)
                    return False
            i += 2
        if movements[-1]["floor"] != target:
            print("Wrong target! person"+str(id))
            print("Wrong target! person"+str(id),
                  file=WrongLog)
            return False
        if movements[0]["floor"] != source:
            print("Wrong source! person"+str(id))
            print("Wrong source! person"+str(id),
                  file=WrongLog)
            return False
        #IN OUT IN OUT IN OUT
        #IN elevator = out elevator
        #OUT floor = IN floor
        #source target
    return True


if __name__ == '__main__':
    id = "Assassin"
    fin = open("in.txt", "r")
    data_in = fin.readlines()
    fin.close()
    print(judge(data_in, open(id + "_out.txt").readlines(), id, {id: 0}, open("wrong_log.txt", "w"),
          {id: 0}))
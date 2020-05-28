from random import randint, random, choice
from numpy.random import permutation

TIME_MAX = 5


def generate(length, num_new_elevator):
    id = []
    ans = []
    add_elev_index = 0
    add_elev_time = []
    order = permutation([1, 2, 3])
    if num_new_elevator == -1:
        num_new_elevator = randint(0, 3)
    for i in range(num_new_elevator):
        add_elev_time.append(randint(0, length - 1))
    # ans: time id from to

    for i in range(length):
        # generate time
        ans.append([TIME_MAX*random()])
        # generate id
        id.append(i+1)

    ans.sort()
    min_time = min(ans)[0]-random()-1

    for i in range(length):
        ans[i][0] -= min_time
        ans[i].append(id[i])
        # generate floor
        floors = list(range(1, 21))
        floors.extend([-1, -2, -3])
        ans[i].append(choice(floors))
        ans[i].append(choice(floors))
        while ans[i][2] == ans[i][3]:
            ans[i][3] = choice(floors)

    for i in range(length):
        if i not in add_elev_time:
            ans[i] = "[{0:.1f}]{1}-FROM-{2}-TO-{3}\n".format(ans[i][0], ans[i][1], ans[i][2], ans[i][3])
        else:
            ans[i] = "[{0:.1f}]{1}-ADD-ELEVATOR-{2}\n".format(ans[i][0], "X"+str(order[add_elev_index]),
                                                              choice(["A", "B", "C"]))
            add_elev_index += 1
    return ans


def generate_coverage():
    ans = ["[1.0]X1-ADD-ELEVATOR-A\n", "[1.0]X2-ADD-ELEVATOR-B\n", "[1.0]X3-ADD-ELEVATOR-C\n"]
    count = 1
    floors = [-3, -2, -1]
    floors.extend(list(range(1, 21)))
    for i in floors:
        for j in floors:
            if i == j:
                continue
            ans.append("[2.0]{}-FROM-{}-TO-{}\n".format(count, i, j))
            count += 1
    return ans


def generate_coverage_no_time():
    ans = ["X1-ADD-ELEVATOR-A\n", "X2-ADD-ELEVATOR-B\n", "X3-ADD-ELEVATOR-C\n"]
    count = 1
    floors = [-3, -2, -1]
    floors.extend(list(range(1, 21)))
    for i in floors:
        for j in floors:
            if i == j:
                continue
            ans.append("{}-FROM-{}-TO-{}\n".format(count, i, j))
            count += 1
    return ans


if __name__ == "__main__":
    print("".join(generate_coverage_no_time()))
from random import randint, random, choice

TIME_MAX = 5


def generate(length, num_elevator):
    id = []
    ans = []
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
        floors = list(range(1, 16))
        floors.extend([-1, -2, -3])
        ans[i].append(choice(floors))
        ans[i].append(choice(floors))
        while ans[i][2] == ans[i][3]:
            ans[i][3] = randint(1, 15)

    for i in range(length):
        ans[i] = "[{0:.1f}]{1}-FROM-{2}-TO-{3}\n".format(ans[i][0], ans[i][1], ans[i][2], ans[i][3])
    ans.insert(0, "[0.0]{}\n".format(num_elevator))
    return ans


if __name__ == "__main__":
    print(generate(20,5))
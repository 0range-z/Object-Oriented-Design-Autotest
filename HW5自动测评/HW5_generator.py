from random import randint, random

TIME_MAX = 9


def generate(length):
    id = []
    ans = []
    # ans: time id from to

    for i in range(length):
        # generate time
        ans.append([TIME_MAX * random()])
        # generate id
        new_id = randint(0, 100)
        while new_id in id:
            new_id = randint(0, 100)
        id.append(new_id)

    ans.sort()
    min_time = min(ans)[0] - random()

    for i in range(length):
        ans[i][0] -= min_time
        ans[i].append(id[i])
        # generate floor
        ans[i].append(randint(1, 15))
        ans[i].append(randint(1, 15))
        while ans[i][2] == ans[i][3]:
            ans[i][3] = randint(1, 15)
        '''
        k = random()
        if k < 0.25 and ans[i][3] != 1:
            ans[i][2] = 1
        elif k < 0.5 and ans[i][2] != 1:
            ans[i][3] = 1
        elif k < 0.75 and ans[i][3] != 15:
            ans[i][2] = 15
        elif ans[i][2] != 15:
            ans[i][3] = 15
        '''
    for i in range(length):
        ans[i] = "[{0:.1f}]{1}-FROM-{2}-TO-{3}\n".format(ans[i][0], ans[i][1], ans[i][2], ans[i][3])

    return ans


def data_generate(length):
    ans = []
    for i in range(length):
        from_floor, to_floor = randint(1, 15), randint(1, 15)
        while from_floor == to_floor:
            from_floor, to_floor = randint(1, 15), randint(1, 15)
        ans.append("[{0:.1f}]{1}-FROM-{2}-TO-{3}\n".format(TIME_MAX * random(), i, from_floor, to_floor))
        ans.sort()
    return ans


if __name__ == "__main__":
    print(data_generate(20))

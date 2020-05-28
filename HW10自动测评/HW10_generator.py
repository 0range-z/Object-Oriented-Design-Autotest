from random import choice, randint, random
from os import listdir, popen

instrs = ['ap', 'ap', 'ar', 'qv', 'qc',
          'qas', 'ca', 'cn', 'qnr',
          'qps', 'qci', 'qci', 'ag', 'atg',
          'qgs', 'qgps', 'qgrs','qgvs','qgrs','qgvs','qgrs','qgvs','qgrs','qgvs','qgrs','qgvs','qgrs','qgvs','qgrs','qgvs','qgrs','qgvs','qgrs','qgvs',
           'qgcs', 'qgam', 'qgav']

#name = ["limbo", "nyima", "claw", "orange"]
#adj = ["beautiful", "ugly", "clever", "rubbish", "great", "bad", "excellent", "terrible"]
name = ["l", "n", "c", "o"]
adj = ["beau", "ugly", "clever", "rubbish", "great", "bad", "excel", "terrible"]



limit = {
    "ap" : 5000,
    "qnr": 333,
    "qci": 333,
    "ag" : 10
}

instr_count = {
    "ap" : 0,
    "qnr": 0,
    "qci": 0,
    "ag" : 0
}


def r(people_num):
    return randint(1, people_num + 1)  # +1 allow for exception


def generate(LENGTH, PEOPLE):
    if random() < 0.7:
        print("GENERATE ADD FIRST")
        return generate_add_first(LENGTH, PEOPLE)
    #elif random() < 0.5:
    #    print("GENERATE N SQUARE")
    #    return generate_n_square(LENGTH, PEOPLE)
    else:
        print("GENERATE RANDOM")
        return generate_random(LENGTH, PEOPLE)


def generate_n_square(LENGTH, PEOPLE):
    instrlist = ''
    people_num = PEOPLE
    group_num = 0

    for i in range(people_num):
        instrlist += "ap {} {} {} {}\n".format(i, choice(adj) + "_" + choice(name), randint(1000000, 10000000),
                                               randint(1, 80))
    relations = randint(people_num, people_num*(people_num)/2)
    relations = min(LENGTH - 2*people_num, relations)
    for i in range(relations):
        instrlist += "ar {} {} {}\n".format(r(people_num), r(people_num), randint(1,50))

    for i in range(LENGTH - PEOPLE - relations):
        pass

    return instrlist



def generate_circle(LENGTH, PEOPLE):
    instrlist = ''
    people_num = PEOPLE
    for i in range(people_num):
        instrlist += "ap {} {} {} {}\n".format(i, choice(adj) + "_" + choice(name), randint(1000000, 10000000),
                                               randint(1, 80))
    relations = randint(people_num, people_num*(people_num)/2)
    relations = min(LENGTH - 50, relations)
    for i in range(relations):
        instrlist += "ar {} {} {}\n".format(r(people_num), r(people_num), 111)
    for i in range(LENGTH - PEOPLE - relations):
        instr = choice(["qgvs", "qgrs"])
        instrlist += '{} {}\n'.format(instr, randint(0, group_num))
    return instrlist


def generate_add_first(LENGTH, PEOPLE):
    instrlist = ''
    people_num = PEOPLE
    group_num = 0
    for i in range(people_num):
        instrlist += "ap {} {} {} {}\n".format(i, choice(adj) + "_" + choice(name), randint(1000000, 10000000),
                                               randint(1, 80))
    for i in range(LENGTH - people_num):
        instr = choice(instrs)
        if instr == "ap":
            continue
        if instr in limit.keys():
            if instr_count[instr] > limit[instr]:
                continue
            else:
                instr_count[instr] += 1
        if instr == 'ar':
            instrlist += "ar {} {} {}\n".format(r(people_num), r(people_num), 111)
        elif instr == 'qv' or instr == 'qc':
            instrlist += '{} {} {}\n'.format(instr, r(people_num), r(people_num))
        elif instr == 'qas' or instr == 'qnr':
            instrlist += '{} {}\n'.format(instr, r(people_num))
        elif instr == 'ca' or instr == 'cn' or instr == 'qci':
            instrlist += '{} {} {}\n'.format(instr, r(people_num), r(people_num))
        elif instr == 'ag':
            instrlist += 'ag {}\n'.format(group_num)
            group_num += 1
        elif instr == 'atg':
            instrlist += 'atg {} {}\n'.format(r(people_num), randint(1, 10))
        elif instr == 'qgps' or instr == 'qgrs' or instr == 'qgvs':
            instrlist += '{} {}\n'.format(instr, randint(0, group_num))
        elif instr == 'qgcs' or instr == 'qgam' or instr == 'qgav':
            instrlist += '{} {}\n'.format(instr, randint(0, group_num))
    return instrlist


def generate_random(LENGTH, PEOPLE):
    instrlist = ''
    people_num = PEOPLE
    group_num = 0
    for i in range(LENGTH):
        instr = choice(instrs)
        if instr in limit.keys():
            if instr_count[instr] > limit[instr]:
                continue
            else:
                instr_count[instr] += 1
        if instr == 'ap':
            instrlist += "ap {} {} {} {}\n".format(i, choice(adj) + "_" + choice(name), randint(1000000, 10000000),
                                                   randint(1, 80))
        elif instr == 'ar':
            instrlist += "ar {} {} {}\n".format(r(people_num), r(people_num), 111)
        elif instr == 'qv' or instr == 'qc':
            instrlist += '{} {} {}\n'.format(instr, r(people_num), r(people_num))
        elif instr == 'qas' or instr == 'qnr':
            instrlist += '{} {}\n'.format(instr, r(people_num))
        elif instr == 'ca' or instr == 'cn' or instr == 'qci':
            instrlist += '{} {} {}\n'.format(instr, r(people_num), r(people_num))
        elif instr == 'ag' and group_num < 10:
            instrlist += 'ag {}\n'.format(group_num)
            group_num += 1
        elif instr == 'atg':
            instrlist += 'atg {} {}\n'.format(r(people_num), randint(1, 10))
        elif instr == 'qgps' or instr == 'qgrs' or instr == 'qgvs':
            instrlist += '{} {}\n'.format(instr, randint(0, group_num))
        elif instr == 'qgcs' or instr == 'qgam' or instr == 'qgav':
            instrlist += '{} {}\n'.format(instr, randint(0, group_num))
    return instrlist


if __name__ == '__main__':
    f = open("data_generate.txt", "w")
    f.write(generate(100000, 5000))
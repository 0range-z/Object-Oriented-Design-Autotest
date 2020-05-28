from random import choice, randint, random

instrs = ['ap', 'ap', 'ar',
          'qci', 'qci', 'ag', 'atg', 'ag', 'atg', 'ag', 'atg',
          'qgps', 'qgrs', 'qgvs',
          'qgcs', 'qgam', 'qgav',
          'qasu', 'bf', 'qm',
          'qmp', 'qmp', 'qmp', 'qmp',
          'qsl', 'qsl',
          'dfg', 'dfg',
          'qbs', 'qbs'
          ]

name = ["Limbo", "Nyima", "Claw", "Orange"]
adj = ["fuck", "ugly", "damn", "shit", "nuts", "crap", "ass", "dick", "jerk", "cum", "cunt"]

limit = {
    "ap" : 800,
    "qsl": 20,
    "ag" : 10
}

instr_count = {
    "ap" : 0,
    "qsl": 0,
    "ag" : 0
}


def r(people_num):
    return randint(1, people_num + 2)  # +1 allow for exception


def generate(LENGTH, PEOPLE):
    print(choice(adj) + choice(name) + " is coming...")
    if random() < 0.8:
        print("GENERATE ADD FIRST")
        return generate_add_first(LENGTH, PEOPLE)
    else:
        print("GENERATE RANDOM")
        return generate_random(LENGTH, PEOPLE)


def generate_n_square(LENGTH, PEOPLE):
    instrlist = ''
    people_num = PEOPLE
    group_num = 0

    for i in range(people_num):
        instrlist += "ap {} {} {} {}\n".format(i, choice(adj) + choice(name), randint(1000000, 10000000),
                                               randint(1, 80))
    relations = randint(people_num, people_num*(people_num)/2)
    relations = min(LENGTH - 2*people_num, relations)
    for i in range(relations):
        instrlist += "ar {} {} {}\n".format(r(people_num), r(people_num), randint(1, 50))

    for i in range(LENGTH - PEOPLE - relations):
        pass

    return instrlist


def generate_add_first(LENGTH, PEOPLE):
    instrlist = ''
    people_num = PEOPLE
    group_num = 1
    for i in range(people_num):
        instrlist += "ap {} {} {} {}\n".format(i, choice(adj) + choice(name), randint(1000000, 10000000),
                                               randint(0, 80))
    relations = randint(int(people_num/2), min(people_num*10, int(LENGTH/2)))
    for i in range(relations):
        instrlist += "ar {} {} {}\n".format(r(people_num), r(people_num), randint(0, 1000))

    for i in range(LENGTH - people_num - relations):
        instr = choice(instrs)
        if instr in limit.keys():
            if instr_count[instr] > limit[instr]:
                i -= 1
                continue
            else:
                instr_count[instr] += 1
        if instr == 'ap':
            instrlist += "ap {} {} {} {}\n".format(people_num + i, choice(adj) + choice(name), randint(1000000, 10000000),
                                                   randint(0, 80))
        elif instr in ['ar', 'bf']:
            instrlist += "{} {} {} {}\n".format(instr, r(people_num), r(people_num), randint(0, 1000))
        elif instr in ['qci', 'qmp', 'qsl']:
            instrlist += '{} {} {}\n'.format(instr, r(people_num), r(people_num))
        elif instr == 'ag':
            instrlist += 'ag {}\n'.format(group_num + 1)
            group_num += 1
        elif instr in ['atg', 'dfg']:
            instrlist += '{} {} {}\n'.format(instr, r(people_num), randint(1, group_num))
        elif instr == 'qasu':
            instrlist += 'qasu {} {}\n'.format(randint(0, 20), randint(0, 80))
        elif instr == 'qbs':
            instrlist += 'qbs\n'
        elif instr == 'qm':
            instrlist += 'qm {}\n'.format(r(people_num))
        elif instr in ['qgps', 'qgrs', 'qgvs']:
            instrlist += '{} {}\n'.format(instr, randint(0, group_num))
        elif instr in ['qgcs', 'qgam', 'qgav']:
            instrlist += '{} {}\n'.format(instr, randint(0, group_num))
        else:
            print("unimplemented instruction {}".format(instr))
            exit(1)
    #print(len(instrlist.split("\n")))
    return instrlist


def generate_random(LENGTH, PEOPLE):
    instrlist = ''
    people_num = PEOPLE
    group_num = 0
    for i in range(LENGTH):
        instr = choice(instrs)
        if instr in limit.keys():
            if instr_count[instr] > limit[instr]:
                i -= 1
                continue
            else:
                instr_count[instr] += 1
        if instr == 'ap':
            instrlist += "ap {} {} {} {}\n".format(i, choice(adj) + choice(name), randint(1000000, 10000000),
                                                   randint(0, 80))
        elif instr in ['ar', 'bf']:
            instrlist += "{} {} {} {}\n".format(instr, r(people_num), r(people_num), randint(0, 1000))
        elif instr in ['qci', 'qmp', 'qsl']:
            instrlist += '{} {} {}\n'.format(instr, r(people_num), r(people_num))
        elif instr == 'ag':
            instrlist += 'ag {}\n'.format(group_num)
            group_num += 1
        elif instr in ['atg', 'dfg']:
            instrlist += '{} {} {}\n'.format(instr, r(people_num), randint(1, 10))
        elif instr == 'qasu':
            instrlist += 'qasu {} {}\n'.format(randint(0, 20), randint(0, 80))
        elif instr == 'qbs':
            instrlist += 'qbs\n'
        elif instr == 'qm':
            instrlist += 'qm {}\n'.format(r(people_num))
        elif instr in ['qgps', 'qgrs', 'qgvs']:
            instrlist += '{} {}\n'.format(instr, randint(0, group_num))
        elif instr in ['qgcs', 'qgam', 'qgav']:
            instrlist += '{} {}\n'.format(instr, randint(0, group_num))
        else:
            print("unimplemented instruction {}".format(instr))
            exit(1)
    #print(len(instrlist.split("\n")))
    return instrlist


if __name__ == '__main__':
    f = open("data_generate.txt", "w")
    print(generate(3000, 800))
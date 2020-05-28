from random import choice, randint, random
from os import listdir, popen

instrs = ['add_person', 'add_person', 'add_relation', 'query_value', 'query_conflict',
          'query_acquaintance_sum', 'compare_age', 'compare_name', 'queury_name_rank',
          'query_people_sum', 'query_circle', 'query_circle']

name = ["limbo", "nyima", "claw", "orange"]
adj = ["beautiful", "ugly", "clever", "rubbish", "great", "bad", "excellent", "terrible"]


def generate(LENGTH, PEOPLE):
    if random() < 0.5:
        print("GENERATE ADD FIRST")
        return generate_add_first(LENGTH, PEOPLE)
    elif random() < 0.5:
        print("GENERATE CIRCLE")
        return generate_circle(LENGTH, PEOPLE)
    else:
        print("GENERATE RANDOM")
        return generate_random(LENGTH, PEOPLE)


def generate_circle(LENGTH, PEOPLE):
    instrlist = ''
    people_num = PEOPLE
    for i in range(people_num):
        instrlist += "add_person"
        instrlist += ' '
        instrlist += str(i)
        instrlist += ' '
        instrlist += choice(adj)+"_"+choice(name)
        instrlist += ' '
        instrlist += str(randint(1000000, 10000000))
        instrlist += ' '
        instrlist += str(randint(1, 80))
        instrlist += '\n'
    relations = randint(people_num, people_num*(people_num)/2)
    relations = min(LENGTH - 50, relations)
    for i in range(relations):
        instrlist += "add_relation"
        instrlist += ' '
        instrlist += str(randint(1,people_num))
        instrlist += ' '
        instrlist += str(randint(1,people_num))
        instrlist += ' '
        instrlist += str(111)
        instrlist += '\n'
    for i in range(LENGTH - PEOPLE -relations):
        instrlist += "query_circle"
        instrlist += ' '
        instrlist += str(randint(1,people_num))
        instrlist += ' '
        instrlist += str(randint(1,people_num))
        instrlist += '\n'
    return instrlist

def generate_add_first(LENGTH, PEOPLE):
    instrlist = ''
    people_num = PEOPLE
    for i in range(people_num):
        instrlist += "add_person"
        instrlist += ' '
        instrlist += str(i)
        instrlist += ' '
        instrlist += choice(adj)+"_"+choice(name)
        instrlist += ' '
        instrlist += str(randint(1000000, 10000000))
        instrlist += ' '
        instrlist += str(randint(1, 80))
        instrlist += '\n'
    for i in range(LENGTH-people_num):
        instr = choice(instrs)
        if instr == "add_person":
            continue
        instrlist += instr
        if instr == 'add_relation':
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
            instrlist += ' '
            instrlist += str(randint(1, 15))
        elif instr == 'query_value' or instr == 'query_conflict':
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
        elif instr == 'query_acquaintance_sum' or instr == 'queury_name_rank':
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
        elif instr == 'compare_age' or instr == 'compare_name' or instr == 'query_circle':
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
        instrlist += '\n'
    return instrlist


def generate_random(LENGTH, PEOPLE):
    instrlist = ''
    people_num = PEOPLE
    for i in range(LENGTH):
        instr = choice(instrs)
        instrlist += instr
        if instr == 'add_person':
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
            instrlist += ' '
            instrlist += choice(adj)+"_"+choice(name)
            instrlist += ' '
            instrlist += str(randint(1000000, 10000000))
            instrlist += ' '
            instrlist += str(randint(1, 80))
        elif instr == 'add_relation':
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
            instrlist += ' '
            instrlist += str(randint(1, 15))
        elif instr == 'query_value' or instr == 'query_conflict':
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
        elif instr == 'query_acquaintance_sum' or instr == 'queury_name_rank':
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
        elif instr == 'compare_age' or instr == 'compare_name' or instr == 'query_circle':
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
        instrlist += '\n'
    #print(instrlist)
    return instrlist


def test():
    for indi in listdir('./projects/'):
        sub = popen('java -jar projects/'+indi+'>'+indi+'.txt', 'w')
        sub.write(instrlist)
        sub.flush()
        sub.close()
    for indi in listdir('./'):
        if indi.endswith(".txt"):
            aans = ''
            with open(indi, 'r') as f:
                for line in f.readlines():
                    aans += line
                f.close()
                ans.append(aans)
                names.append(indi)
    for i in range(len(ans)):
        for j in range(i+1, len(ans)):
            if ans[i] != ans[j]:
                with open('wronglog'+str(wrong)+'.txt', 'w') as f:
                    f.write(name[i]+'different with'+name[j])
                    f.write(instrlist)
                    f.close()
            else:
                print('correct')
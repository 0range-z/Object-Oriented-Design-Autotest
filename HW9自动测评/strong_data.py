from random import choice

name = ["limbo", "nyima", "claw", "orange"]
adj = ["beautiful", "ugly", "clever", "rubbish", "great", "bad", "excellent", "terrible"]


if __name__ == '__main__':
    instrlist = ''
    for i in range(1,500):
        instrlist += "add_person"
        instrlist += ' '
        instrlist += str(i)
        instrlist += ' '
        instrlist += choice(adj)+"_"+choice(name)
        instrlist += ' '
        instrlist += str(666)
        instrlist += ' '
        instrlist += str(233)
        instrlist += '\n'
    for i in range(1,400):
        instrlist += "add_relation"
        instrlist += ' '
        instrlist += str(i)
        instrlist += ' '
        instrlist += str(i+1)
        instrlist += ' '
        instrlist += str(111)
        instrlist += '\n'
    for i in range(400,500):
        instrlist += "query_circle"
        instrlist += ' '
        instrlist += str(1)
        instrlist += ' '
        instrlist += str(i)
        instrlist += '\n'
    f = open("strong_data.txt", "w")
    print(instrlist, file=f)
    f.close()

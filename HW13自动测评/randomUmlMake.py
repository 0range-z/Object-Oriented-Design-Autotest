from model import *
from setting import *

PARENTNAME = 'parent'
CLASSNAME = 'class'
INTERFACENAME = 'inter'
OPERATIONNAME = 'method'
ATTRIBUTENAME = 'attribute'
VISIBILITY = ['public', 'private', 'protected', 'package']
PARA = 'para'

methodsName = set()


def makeClassName(num):
    return CLASSNAME + str(num)


def makeInterfaceName(num):
    if (interfaceNameMulti):
        return INTERFACENAME + str(random.randint(0, num))
    return INTERFACENAME + str(num)


def makeOperationName(parentnum, num, isClass):
    if (isClass):
        name = CLASSNAME + str(parentnum) + OPERATIONNAME + str(num)
    else:
        name = INTERFACENAME + str(parentnum) + OPERATIONNAME + str(num)
    methodsName.add(name)
    return name


def makeAttributeName(parentnum, num, isClass):
    if (isClass):
        return CLASSNAME + str(parentnum) + ATTRIBUTENAME + str(num)
    else:
        return INTERFACENAME + str(parentnum) + ATTRIBUTENAME + str(num)


def makeVisibility(randomMode=False):
    if (randomMode):
        if (random.randint(0, 4) != 0):
            return 'private'
    return VISIBILITY[random.randint(0, 3)]


def makeOperation(builder, parentid, inputcount, isreturn, visibility, opname):
    inmode = ['in', 'out', 'inout']
    opid = builder.createOperation(parentid, opname, visibility)
    for i in range(inputcount):
        mode = inmode[random.randint(0, 2)]
        builder.createParameter(opid, PARA + str(i), 'int', mode)
    if (isreturn):
        builder.createParameter(opid, 'return', 'int', 'return')


def randomParent(total, builder, parentlist, void, create, isClass=True):
    for i in range(total):
        parentid = create(void(i), makeVisibility())
        parentlist.append(parentid)
        opcount = 0
        opnum = 0
        oppara = []
        if (~isClass):
            continue
        while (opcount < operationtotal):
            opcount += 1
            if (random.randint(0, 2) == 0):
                oppara = []
                opnum += 1
            inputcount = random.randint(0, parameterCount)
            isreturn = random.choice([True, False])
            visibility = makeVisibility()
            while (str(inputcount) + str(isreturn) + str(visibility) in oppara):
                inputcount = random.randint(0, 4)
                isreturn = random.choice([True, False])
                visibility = makeVisibility()
            makeOperation(builder, parentid, inputcount, isreturn, visibility, makeOperationName(i, opnum, isClass))
        attricount = 0
        while (attricount < attributetotal):
            attricount += 1
            parentnum = i
            if (random.randint(0, attributeSameCount) == 0):
                while (parentnum == i):
                    parentnum = random.randint(0, total)
            builder.createAttribute(parentid, makeAttributeName(parentnum, attricount, isClass), makeVisibility(True),
                                    'int')


def randomGen(builder, gentotal, parentlist, parenttotal, struct):
    def findfather(a):
        if (parent[a] != a):
            parent[a] = findfather(parent[a])
        return parent[a]

    def link(a, b):
        fa = findfather(a)
        fb = findfather(b)
        if (fa != fb):
            parent[fa] = fb

    parent = {}
    struct.write('classes:\n')
    for i in range(parenttotal):
        parent[i] = i
    for i in range(gentotal):
        fa = random.randint(0, parenttotal - 1)
        while (findfather(fa) == findfather(i)):
            fa = random.randint(0, parenttotal - 1)
        link(i, fa)
        struct.write(str(i) + ' father is ' + str(fa) + '\n')
        builder.createGeneralization('gen', parentlist[i], parentlist[fa])
    struct.write('\n')


def randomInterfaceGenerealization(builder, struct, parentlist):
    struct.write('interfaces:\n')
    parent = {}
    for i in range(interfacetotal):
        parent[i] = set()

    for i in range(geneintertotal):
        n = random.randint(1, interfaceFatherCount)
        fathers = list(range(interfacetotal))
        del fathers[i]
        for j in range(n):
            if (len(fathers) == 0):
                break
            faindex = random.randint(0, len(fathers) - 1)
            fa = fathers[faindex]
            k = True
            while (fa in parent[i]) or (i in parent[fa]):
                del fathers[faindex]
                if (len(fathers) == 0):
                    k = False
                    break
                faindex = random.randint(0, len(fathers) - 1)
                fa = fathers[faindex]
            if (k):
                parent[i].add(fa)
                parent[i].update(parent[fa])
                for t in parent:
                    if i in parent[t]:
                        parent[t].update(parent[i])
                struct.write(parentlist[i] + ' father is ' + parentlist[fa] + '\n')
                '''
                print('new')
                for s in parent:
                    print('\t'+str(s)+'\t'+str(parent[s]))
                '''
                builder.createGeneralization('intergen', parentlist[i], parentlist[fa])


def randomRealization(builder, classlist, interlist):
    create = []
    for i in range(realizationtotal):
        source = classlist[random.randint(0, classtotal - 1)]
        target = interlist[random.randint(0, interfacetotal - 1)]
        s = source + '#' + target
        while s in create:
            source = classlist[random.randint(0, classtotal - 1)]
            target = interlist[random.randint(0, interfacetotal - 1)]
            s = source + '#' + target
        create.append(s)
        builder.createInterfaceRealization('interreal', source, target)


def randomAssociation(builder, list):
    for i in range(associationtotal):
        end1 = random.choice(list)
        end2 = random.choice(list)
        builder.createAssociation('asso', 'public', 'public', end1, end2)


def randomData(file, struct):
    with ModelBuilder('random', file) as builder:
        classlist = []
        interfacelist = []
        randomParent(classtotal, builder, classlist, makeClassName, builder.createClass, True)
        randomParent(interfacetotal, builder, interfacelist, makeInterfaceName, builder.createInterface, False)
        if (classNameMulti):
            builder.createClass(makeClassName(random.randint(0, classtotal)), 'public')
        randomGen(builder, geneclasstotal, classlist, classtotal, struct)
        randomInterfaceGenerealization(builder, struct, interfacelist)
        randomRealization(builder, classlist, interfacelist)
        randomAssociation(builder, classlist + interfacelist)
        model = builder.getModel()
    return model


class randomUmlMake:
    def __init__(self, filecount):
        file = '../data.txt'
        filestruct = '../data_struct.txt'
        self._file = open(file, 'w')
        self._struct = open(filestruct, 'w')

    def __enter__(self):
        return (randomData(self._file, self._struct), self._file)

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._file.close()
        self._struct.close()
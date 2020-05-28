from randomUmlMake import randomUmlMake
from randomUmlMake import methodsName
from randomUmlMake import makeClassName
from setting import *
import sys
import random


def createClassCount():
    return 'CLASS_COUNT'


'''
def createClassOpCount(className):
    modes = ['NON_RETURN', 'RETURN', 'NON_PARAM', 'PARAM', 'ALL']
    result = []
    for i in modes:
        result.append('CLASS_OPERATION_COUNT ' + className + ' ' + i)
    return result
'''


def createClassOpCount(className):
    modes = ['NON_RETURN', 'RETURN', 'NON_PARAM', 'PARAM', 'ALL']
    result = []
    result.append('CLASS_OPERATION_COUNT ' + className)
    for i in modes:
        result.append('CLASS_OPERATION_COUNT ' + className + ' ' + i)
    for i in range(10):
        j, k = random.randint(0, 4), random.randint(0, 4)
        while j == k:
            j, k = random.randint(0, 4), random.randint(0, 4)
        result.append('CLASS_OPERATION_COUNT ' + className + ' ' + modes[j] + ' ' + modes[k])
    return result


def createClassAttrCount(className):
    modes = ['ALL', 'SELF_ONLY']
    result = []
    for s in modes:
        result.append('CLASS_ATTR_COUNT ' + className + ' ' + s)
    return result


def createClassAssoCount(className):
    return 'CLASS_ASSO_COUNT ' + className


def createClassAssoClassList(className):
    return 'CLASS_ASSO_CLASS_LIST ' + className


def createOpVisibility(className, methodName):
    return 'CLASS_OPERATION_VISIBILITY ' + className + ' ' + methodName


def createAttrVisibility(className, AttrName):
    return 'CLASS_ATTR_VISIBILITY ' + className + ' ' + AttrName


def createClassTop(className):
    return 'CLASS_TOP_BASE ' + className


def createImpleInterList(className):
    return 'CLASS_IMPLEMENT_INTERFACE_LIST ' + className


def createInfoHidden(className):
    return 'CLASS_INFO_HIDDEN ' + className


def StrongData(count='1', mode='normal'):
    with randomUmlMake(count) as m:
        instrs = []
        if (mode == 'normal'):
            model = m[0]
            datafile = m[1]
            classidMap = model.getClass()
            interfaceidMap = model.getInterface()
            for classid in classidMap:
                className = classidMap[classid]
                attrnames = []
                id = classid
                while (id != None):
                    attrnames.extend(model.getClassAttributes(id))
                    id = model.getClassParentId(id)
                attrnames = set(attrnames)
                for i in range(normalCount):
                    instrs.extend(createClassAttrCount(className))
                    instrs.append(createClassAssoCount(className))
                    instrs.append(createClassAssoClassList(className))
                    for s in attrnames:
                        instrs.append(createAttrVisibility(className, s))
                    instrs.append(createClassTop(className))
        elif (mode == 'strong'):
            model = m[0]
            datafile = m[1]
            classidMap = model.getClass()
            interfaceidMap = model.getInterface()
            for classid in classidMap:
                className = classidMap[classid]
                for i in range(strongCount):
                    instrs.append(createImpleInterList(className))
                    # instrs.append(createInfoHidden(className))
        for instr in range(len(instrs) - 1):
            datafile.write(instrs[instr] + '\n')
        datafile.write(instrs[-1])


def randomMake(count='1'):
    instrs = []
    with randomUmlMake(count) as m:
        model = m[0]
        datafile = m[1]
        classidMap = model.getClass()
        interfaceidMap = model.getInterface()
        instrs.append(createClassCount())
        if (notFoundClass):
            notFoundClassName = random.randint(len(classidMap), 99999)
            notFoundClassName = makeClassName(notFoundClassName)
            instrs.append(createClassTop(notFoundClassName))
            instrs.append(createImpleInterList(notFoundClassName))
            instrs.append(createInfoHidden(notFoundClassName))
            instrs.extend(createClassAttrCount(notFoundClassName))
            instrs.append(createAttrVisibility(notFoundClassName, notFoundClassName))
            instrs.extend(createClassOpCount(notFoundClassName))
            instrs.append(createOpVisibility(notFoundClassName, notFoundClassName))
            instrs.append(createClassAssoClassList(notFoundClassName))
            instrs.append(createClassAssoCount(notFoundClassName))
        for i in classidMap:
            className = classidMap[i]
            instrs.extend(createClassOpCount(className))
            instrs.extend(createClassAttrCount(className))
            instrs.append(createClassAssoCount(className))
            instrs.append(createClassAssoClassList(className))
            instrs.append(createClassTop(className))
            instrs.append(createImpleInterList(className))
            instrs.append(createInfoHidden(className))
            classid = i
            methods = list(methodsName)
            for method in methods:
                instrs.append(createOpVisibility(className, method))
            attrnames = []
            while (classid != None):
                attrnames.extend(model.getClassAttributes(classid))
                classid = model.getClassParentId(classid)
            attrnames = set(attrnames)
            for s in attrnames:
                instrs.append(createAttrVisibility(className, s))
            if (notFountAttri):
                instrs.append(createAttrVisibility(className, className))
        for i in range(len(instrs)):
            if (i != len(instrs) - 1):
                datafile.write(instrs[i] + '\n')
            else:
                datafile.write(instrs[i])


def dataMake(count='1', mode='normal', isStrong=False):
    if (isStrong):
        StrongData(count, mode)
    else:
        randomMake(count)
    print('Data gen finish!')


if __name__ == "__main__":
    if (len(sys.argv) < 3):
        dataMake()
    else:
        dataMake(sys.argv[1], sys.argv[2], isStrong=True)
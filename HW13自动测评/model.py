import random

class Model:
    def __init__(self,modelname):
        self._modelname = modelname
        # id -> name
        self._map = {}
        # classid -> classname
        self._classes = {}
        # interfaceid -> interfacename
        self._interfaces = {}
        # operationid -> operationname
        self._operations = {}
        # classid -> [operationsid]
        self._classOperations = {}
        # classid -> [attributesid]
        self._classAttributes = {}
        # interfaceid -> [operationsid]
        self._interfaceOperations = {}
        # interfaceid -> [attributesid]
        self._interfaceAttributes = {}
        # classid -> classFatherid
        self._classesFather = {}
        # interfaceid -> interfaceFatherid
        self._interfaceFather = {}
    
    def _addClass(self,classname,visibility,id):
        self._map[id] = classname
        self._classes[id] = classname

    def _addInterface(self,interfaceName,visibility,id):
        self._map[id] = interfaceName
        self._interfaces[id] = interfaceName

    def _addOperation(self,parentId,operationName,visibility,id):
        self._map[id] = operationName
        self._operations[id] = operationName
        if (parentId in self._classes):
            if (parentId in self._classOperations):
                self._classOperations[parentId].append(id)
            else:
                self._classOperations[parentId] = []
        elif (parentId in self._interfaces):
            if (parentId in self._interfaceOperations):
                self._interfaceOperations[parentId].append(id)
            else:
                self._interfaceOperations[parentId] = []

    def _addAttribute(self,parentId,attributeName,visibility,id,attributeType):
        self._map[id] = attributeName
        if (parentId in self._classes):
            if (parentId in self._classAttributes):
                self._classAttributes[parentId].append(id)
            else:
                self._classAttributes[parentId] = []
        elif (parentId in self._interfaces):
            if (parentId in self._interfaceAttributes):
                self._interfaceAttributes[parentId].append(id)
            else:
                self._interfaceAttributes[parentId] = []

    def _addParameter(self,parentId,parameterName,id,parameterType,direction):
        self._map[id] = parameterName

    def _addGeneralization(self,source,target):
        if (source in self._classes):
            self._classesFather[source] = target
        else:
            self._interfaceFather[source] = target

    def getClass(self):
        return self._classes

    def getInterface(self):
        return self._interfaces

    def getClassAttributes(self,classid):
        names = []
        if classid not in self._classAttributes:
            return names
        for id in self._classAttributes[classid]:
            if self._map[id] not in names:
                names.append(self._map[id])
        return names

    def getClassParentId(self,classid):
        if (classid in self._classesFather):
            return self._classesFather[classid]
        else:
            return None

    def getClassOperations(self,classid):
        names = []
        for id in self._classOperations[classid]:
            names.append(self._operations[id])
        return set(names)

class ModelBuilder:
    def __init__(self,modelname,file):
        self._file = file
        self._class = 'UMLClass'
        self._interface = 'UMLInterface'
        self._operation = 'UMLOperation'
        self._attribute = 'UMLAttribute'
        self._association = 'UMLAssociation'
        self._interfaceRealization = 'UMLInterfaceRealization'
        self._associationEnd = 'UMLAssociationEnd'
        self._generalization = 'UMLGeneralization'
        self._parameter = 'UMLParameter'
        self._model = Model(modelname)
        self._parent = '"_parent":'
        self._id = '"_id":'
        self._name = '"name":' 
        self._type = '"_type":'
        self._visibility = '"visibility":'
        self._idlist = ['=','/','+']
        for i in range(10):
            self._idlist.append(str(i))
        for i in range(26):
            self._idlist.append(chr(i+65))
            self._idlist.append(chr(i+97))
        self._idlist.remove('A')
        random.shuffle(self._idlist)
        self._idlist = random.sample(list(self._idlist),9)
        self._idlist.insert(0,'A')
        self._idnum = []
        self._umls = []
        begin = random.randint(9999999,999999999)
        for i in range(1000):
            self._idnum.append(begin + i*11)
        self._parentId = None

    def _makeId(self):
        length = 20
        i = random.randint(0,len(self._idnum) - 1)
        num = self._idnum[i]
        del self._idnum[i]
        s = str(num)
        ret = ''
        for i in range(length - len(s)):
            ret += self._idlist[0]
        for i in s:
            ret += self._idlist[int(i)]
        return ret

    def __enter__(self):
        self._parentId = self._makeId()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        random.shuffle(self._umls)
        for s in self._umls:
            self._file.write(s+'\n')
        self._file.write('END_OF_MODEL\n')

    def _makeUml(self,id,parent,name,umlType,info):
        uml = '{'
        stype = '"type":'
        direction = '"direction":'
        source = '"source":'
        target = '"target":'
        end1 = '"end1":'
        end2 = '"end2":'
        reference = '"reference":'
        multiplicity = '"multiplicity":"",'
        aggregation = '"aggregation":"none",'
        if (umlType == self._class):
            uml += self._parent + '"' + parent + '",'
            uml += self._visibility + '"' + info[0] + '",'
            uml += self._name + '"' + name + '",'
            uml += self._type + '"' + self._class + '",'
            uml += self._id + '"' + id + '"'
        elif (umlType == self._interface):
            uml += self._parent + '"' + parent + '",'
            uml += self._visibility + '"' + info[0] + '",'
            uml += self._name + '"' + name + '",'
            uml += self._type + '"' + self._interface + '",'
            uml += self._id + '"' + id + '"'
        elif (umlType == self._operation):
            uml += self._parent + '"' + parent + '",'
            uml += self._visibility + '"' + info[0] + '",'
            uml += self._name + '"' + name + '",'
            uml += self._type + '"' + self._operation + '",'
            uml += self._id + '"' + id + '"'
        elif (umlType == self._attribute):
            uml += self._parent + '"' + parent + '",'
            uml += self._visibility + '"' + info[0] + '",'
            uml += self._name + '"' + name + '",'
            uml += self._type + '"' + self._attribute + '",'
            uml += self._id + '"' + id + '",'
            uml += stype + '"' + info[1] + '"'
        elif (umlType == self._parameter):
            uml += self._parent + '"' + parent + '",'
            uml += self._name + '"' + name + '",'
            uml += self._type + '"' + self._parameter + '",'
            uml += self._id + '"' + id + '",'
            uml += stype + '"' + info[0] + '",'
            uml += direction + '"' + info[1] + '"'
        elif (umlType == self._generalization):
            uml += self._parent + '"' + parent + '",'
            uml += self._name + '"' + name + '",'
            uml += self._type + '"' + self._generalization + '",'
            uml += self._id + '"' + id + '",'
            uml += source + '"' + info[0] + '",'
            uml += target + '"' + info[1] + '"'
        elif (umlType == self._association):
            uml += self._parent + '"' + parent + '",'
            uml += self._name + '"' + name + '",'
            uml += self._type + '"' + self._association + '",'
            uml += end2 + '"' + info[1] + '",'
            uml += end1 + '"' + info[0] + '",'
            uml += self._id + '"' + id + '"'
        elif (umlType == self._associationEnd):
            uml += reference + '"' + info[0] + '",'
            uml += multiplicity
            uml += self._parent + '"' + parent + '",'
            uml += self._visibility + '"' + info[1] + '",'
            uml += self._name + '"' + name + '",'
            uml += self._type + '"' + self._associationEnd + '",'
            uml += aggregation
            uml += self._id + '"' + id + '"'
        elif (umlType == self._interfaceRealization):
            uml += self._parent + '"' + parent + '",'
            uml += self._name + '"' + name + '",'
            uml += self._type + '"' + self._interfaceRealization + '",'
            uml += self._id + '"' + id + '",'
            uml += source + '"' + info[0] + '",'
            uml += target + '"' + info[1] + '"'
        uml += '}'
        self._umls.append(uml)

    def createClass(self,className,visibility):
        id = self._makeId()
        parentId = self._parentId
        self._model._addClass(className,visibility,id)
        self._makeUml(id,parentId,className,self._class,(visibility,))
        return id

    def createInterface(self,interfaceName,visibility):
        id = self._makeId()
        parentId = self._parentId
        self._model._addInterface(interfaceName,visibility,id)
        self._makeUml(id,parentId,interfaceName,self._interface,(visibility,))
        return id

    def createOperation(self,parentId,operationName,visibility):
        if (parentId not in self._model._classes)&(parentId not in self._model._interfaces):
            return None
        id = self._makeId()
        self._model._addOperation(parentId,operationName,visibility,id)
        self._makeUml(id,parentId,operationName,self._operation,(visibility,)) 
        return id
    
    def createAttribute(self,parentId,attributeName,visibility,attributeType):
        if (parentId not in self._model._classes)&(parentId not in self._model._interfaces):
            return None
        id = self._makeId()
        self._model._addAttribute(parentId,attributeName,visibility,id,attributeType)
        self._makeUml(id,parentId,attributeName,self._attribute,(visibility,attributeType)) 
        return id

    def createParameter(self,parentId,parameterName,parameterType,direction):
        if (parentId not in self._model._operations):
            return None
        id = self._makeId()
        self._model._addParameter(parentId,parameterName,id,parameterType,direction)
        self._makeUml(id,parentId,parameterName,self._parameter,(parameterType,direction)) 
        return id

    def createGeneralization(self,name,source,target):
        if (source not in self._model._classes)&(source not in self._model._interfaces):
            return None
        if (target not in self._model._classes)&(target not in self._model._interfaces):
            return None
        id = self._makeId()
        parentId = source
        self._model._addGeneralization(source,target)
        self._makeUml(id,parentId,name,self._generalization,(source,target)) 
        return id
    
    def createAssociation(self,name,end1Visibility,end2Visibility,end1Ref,end2Ref):
        if (end1Ref not in self._model._map)|(end2Ref not in self._model._map):
            return None
        id = self._makeId()
        parentId = end1Ref
        end1Id = self._makeId()
        end2Id = self._makeId()
        end1ParentId = id
        end2ParentId = id
        self._makeUml(id,parentId,name,self._association,(end1Id,end2Id)) 
        self._makeUml(end1Id,end1ParentId,name,self._associationEnd,(end1Ref,end1Visibility)) 
        self._makeUml(end2Id,end2ParentId,name,self._associationEnd,(end2Ref,end2Visibility)) 
        return id

    def createInterfaceRealization(self,name,source,target):
        if (source not in self._model._classes):
            return None
        if (target not in self._model._interfaces):
            return None
        id = self._makeId()
        parentId = source
        self._makeUml(id,parentId,name,self._interfaceRealization,(source,target)) 
        return id

    def getModel(self):
        return self._model

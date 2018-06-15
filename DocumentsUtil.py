def ExtractZones(ZoneDoc):#path to csv containing zones
    csv = open(ZoneDoc).read()
    Rows = csv.split('\n')
    Rows.pop(0) #remove the labels
    Zones = []
    for row in Rows:
        Zones.append(row.split(',')[0])
    return Zones

def PrintCheckedBoxes(KeyVar,KeyList,DisVar,DisList):
    for i,val in enumerate(KeyVar):
        if val.get():
            print(KeyList[i])
            
def ExtractReferences(RefDoc):#returns a Dictionary of all references
    file = open(RefDoc).read()
    Lines = file.split('\n')
    References = {}
    for sec in Lines:
        Tokens = sec.split(',')
        if not Tokens[0]=='':
            References[Tokens[0]] = []
        for i in range(1,len(Tokens)):
            if not Tokens[i]=='':
                References[Tokens[0]].append(Tokens[i])
    return References

def ExtractDistricts(DistrictDoc):
    return open(DistrictDoc).read().split('\n')

def ExtractKeyBuckets(File):
    txt = open(File).read()
    KeyWor = []
    KeyBucke=[]
    KeyFin = []
    for i,line in enumerate(txt.split('\n')):
        temp = line.split(',')
        KeyWor.append(temp[0])
        KeyFin.append(temp[1])
        KeyBucke.append([])
        for count in range(2,len(temp)):
            KeyBucke[i].append(temp[count])
    return KeyWor,KeyFin,KeyBucke

##def ExtractKeyBuckets(filename):
##    txt = open(filename,mode='r')
##    KeyBuckets = []
##    for i,line in enumerate(txt):
##        KeyBuckets.append(line.split(','))
##        KeyBuckets[i].remove('\n')
##    txt.close()
##    return KeyBuckets

def ExtractKeyBucketsDictionary(filename): #file is line w/ keyword followed by the next line a ',' delimited list of keywords associated.K
    txt = open(filename,mode='r')
    KeyBuckets = {}
    for i,line in enumerate(txt):
        if i%2 ==0:
            name = line.replace('\n','')
        else:
            KeyBuckets[name] = line.split(',')
            KeyBuckets[name].remove('\n')
    txt.close()
    return KeyBuckets

def KeySet(KeyWords):
    KeySet = []
    for sec in KeyWords:
        for item in sec:
            KeySet.append(item)
    return sorted(list(set(KeySet)))
##    return PolishKeySet(sorted(list(set(KeySet))))

def PolishKeySet(KeySet):
    Whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ()-')
    BlackList = ['\r','\n','\x0c','  ','   ']
    PolishedKeySet = []
    for item in KeySet:
        if len(item) < 50:
            for char in BlackList:
                item = item.replace(char,' ')
            PolishedKeySet.append(item)
    
    for i in range(len(PolishedKeySet)):
        PolishedKeySet[i] = PolishedKeySet[i].replace('  ',' ')
        PolishedKeySet[i] = ''.join(filter(Whitelist.__contains__, PolishedKeySet[i]))
    return PolishedKeySet

def DistrictSet(References):
    Set = set()
    for List in References:
        for item in List:
            Set.add(item)
    return sorted(list(Set))

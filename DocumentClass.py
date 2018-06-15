import codecs
import re
from DocumentsUtil import *
import json


MinimumSection = 11 #Sections are numbered xx(x)-y(yy), i.e. 14-142
                    # 11 is the smallest xx can be
def PrintList(item):
    for i,tok in enumerate(item):
        print(i,": ",tok)

class Document:
    def __init__(self,DocFile,ZonesFile=None):
        self.DocFile = DocFile                                             #Document name
        self.ZoneDoc = codecs.open(self.DocFile, encoding="utf-8").read()  #Document as read()
        self.Sections,self.ZoningIDs = self.Regex_Sec_and_IDs()#self.Generate_Regex_Sections()
        self.IDsGiven = False
        self.Titles = self.Generate_Titles()
        #Default, assume no ID list is given
        if not ZonesFile==None:#for setting All_IDs
            self.IDsGiven = True
            self.IDsFile = ZonesFile
        self.IDtoIndex = self.Generate_index_dict()                         #Dictionary to references indexes by ZoneID
        self.All_IDs = self.Generate_ChaptIDs()                             #All IDs in the document
        self.Zone_References = self.Generate_Zone_References()          #references to other sections found in each zone
        self.KeyWords = self.ExtractKeyWords()
        self.District_References = self.Regex_District_References()
        self.DistrictList = DistrictSet(self.District_References)

##EXPLANATION OF ARGUMENTS
##DocFile: file containing the entire document to be analyzed
##ZonesFile: file containing a list of Zones known to be in DocFile, delimited by '\n'
##DistrictFile: file containing list of Districts known to be in DocFile, delimited by '\n'
##
    def Regex_Sec_and_IDs(self):
        DateLineRegex = re.compile(r'(\(\d+/\d+/\d+\))[\r\n\x0c]+(\d\d\d?-A?\d\d\d?)') #Search for (mm/dd/yy) then \r\n then xx(x)-y(yy) ZoningID
        Split = DateLineRegex.split(self.ZoneDoc)
        Sections =[]
        ZoningIDs = []
        Sections.append(Split[0])   #Add title text w/ no section
        ZoningIDs.append('')
        EvenCheck = 0               #Prevents going over index of Split in for loop
        if len(Split)%2 ==0:
            EvenCheck = 1
        for i in range(1,len(Split)-EvenCheck,3):
            Sections.append(Split[i]+'\r\n\r\n'+Split[i+1]+Split[i+2])
            ZoningIDs.append(Split[i+1])
        return Sections,ZoningIDs



    def PolishKeyWords(self,KeyWords):
        PolishedWords = []
        PolishRegex = re.compile(r'\w+')
        for i,lis in enumerate(KeyWords):
            PolishedWords.append([])
            for word in lis:
                if len(word)>100:
                    continue
                else:
                    PolishedWords[i].append(' '.join(PolishRegex.findall(word.lower())))
        return PolishedWords

    def ExtractKeyWords(self):
        KeyWords = []
        KeyWordRegex = re.compile(r'#(.*?)#',re.DOTALL)
        for k, sec in enumerate(self.Sections):
            KeyWords.append(sorted(list(set(KeyWordRegex.findall(sec)))))
        return self.PolishKeyWords(KeyWords)

    def Generate_index_dict(self):
        Dict = {}
        for j,ID in enumerate(self.ZoningIDs):
            Dict[ID] = j
        return Dict
    #Simply maps IDs to a dictionary


    def Regex_District_References(self):
        SpecialOne = re.compile(r'([UCL])')
        SpecialB = re.compile(r'(B[PR]C?)')
        SpecialC = re.compile(r'(C[DILOP])')
        SpecialD = re.compile(r'(D[BJ])')
        SpecialE = re.compile(r'(EC-[123456])')
        SpecialF = re.compile(r'(FH)')
        SpecialG = re.compile(r'(G[CI])')
        SpecialH = re.compile(r'(H[RSPY][WQ]?)')
        SpecialL = re.compile(r'(L[CIM]C?)')
        SpecialM = re.compile(r'(M[IMP][DU]?)')
        SpecialMX = re.compile(r'(MX-\d\d?)')
        SpecialNA = re.compile(r'(NA-[1234])')
        SpecialO = re.compile(r'(OP)')
        SpecialP = re.compile(r'(P[CI])')
        SpecialS = re.compile(r'(S[BGHRVW][PDI-W]1?)')
        SpecialT = re.compile(r'(T[MA]U?)')
        SpecialU = re.compile(r'(US?)')
        SpecialW = re.compile(r'(W[CP]H?)')

        SpecialRegexes = [SpecialMX, SpecialNA,SpecialB,SpecialC,SpecialD,SpecialE,SpecialF,SpecialG,
                          SpecialH,SpecialL,SpecialM,SpecialO,SpecialP,SpecialS,
                          SpecialT,SpecialW]
        DistrictRegex = re.compile(r'''(
            ([CMRL][\dH])                 #Starts with CMRL, next is either number or H
            (
            ([\dABDFHX]{0,2})?            #Next either Number or one of these letters, up to 2
            (\\r\\n)?
            (-(\\r\\n)?[\dA-Z.]{1,3})?             #if -, must have num of capital letter after
            )?
            )''',re.VERBOSE)

        DistrictReferences = []
        SpecialReferences = []
        Districts = ExtractDistricts('DistList')
        SpecialDistricts = ExtractDistricts('SpecialDistricts')
        for i,sec in enumerate(self.Sections):
            sec = sec.replace('\r\n','')
            Temp = DistrictRegex.findall(sec)
            DistrictReferences.append(set())
            for item in Temp:
                if item[0] in Districts:
                    DistrictReferences[i].add(item[0])

        for i,sec in enumerate(self.Sections):
            sec = sec.replace('\r\n','')
            for regex in SpecialRegexes:
                Temp = regex.findall(sec)
                for item in Temp:
                    if item in SpecialDistricts:
                        DistrictReferences[i].add(item)
        for i,sec in enumerate(DistrictReferences):
            DistrictReferences[i] = sorted(DistrictReferences[i])

        return DistrictReferences

    def Generate_Zone_References(self):
        References = []
        ZoneRegex = re.compile(r'\d\d\d?-A?\d\d\d?')
        for sec in self.Sections:
            References.append(ZoneRegex.findall(sec))
        return References

    def Generate_ChaptIDs(self):
        if self.IDsGiven:
            Parents = ExtractDistricts(self.IDsFile)
        else:
            Parents = self.ZoningIDs
        return list(set(Parents))

    def Generate_Titles(self):  #Based on the structure that the section id appears
        titles = []             #Followed by \r\n\r\n,  This is only in general, not for every case
        for i,sec in enumerate(self.Sections):
            lines = sec.split('\r\n\r\n')
            for x in lines:
                if self.ZoningIDs[i] in x:
                    title = x.replace(self.ZoningIDs[i],'')
                    title = title.replace('\r\n',' ')
                    titles.append(title.strip())
                    break

        return titles




Doc = Document("NYZoningResolution.txt")

# Doc = Document("UnitTest.txt")
def AllSectionsToJSON(Doc):
    JSON = {}
    for i,sec in enumerate(Doc.Sections):
        dict = {}
        dict['Section'] = sec
        dict['ID'] = Doc.ZoningIDs[i]
        dict['Title'] = Doc.Titles[i]
        dict['Keywords'] = Doc.KeyWords[i]
        dict['Zone_References'] = Doc.Zone_References[i]
        dict['District_References'] = Doc.District_References[i]
        JSON[i] = json.dumps(dict)

    r = json.dumps(JSON)

    file = open('Sections.json', mode = 'w+')
    # file = open('Sections/'+str(i)+'.txt', mode = 'w+')

    file.write(r)
    file.close()


def AllSectionsToTXT(Doc):
    for i,sec in enumerate(Doc.Sections):
        dict = {}
        dict['Section'] = sec
        dict['ID'] = Doc.ZoningIDs[i]
        dict['Title'] = Doc.Titles[i]
        r = json.dumps(dict)
        file = open('Sections/'+str(i)+'.txt', mode = 'w+')

        file.write(r)
        file.close()


##AllSectionsToJSON(Doc)

# for i in range(0,10000,5):
#     print(Doc.Title[i])
    # print(Doc.Sections[i])

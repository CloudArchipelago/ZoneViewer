#/usr/bin/python
import Tkinter as tk
##from tkinter import ttk
from Tkinter import *
import ttk
from DocumentsUtil import*
from DocumentClass import Document
import codecs
import random

import matplotlib
matplotlib.use('Agg')

VivacityColors = [
'#0471BD', #blue
'#2DD354', #green
'#FCD015', #Yellow
'#F8941E', #orange
'#EF4037', #red
'#B442CD', #purple
'#19B774', #dark green
'#6BF6F6', #baby blue
    ]
LARGE_FONT = ("Tempus Sans ITC",20)
class Window(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        
        tk.Tk.wm_title(self,"Vivacity")
        self.configure(background='black')
        container = tk.Frame(self)
        container.pack(side='top',fill='both',expand=True)
        
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        
        self.frames={}

        for F in (StartPage,DistrictsPage,KeyWordsPage,DocumentViewPage,SentenceLabelPage):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(StartPage)

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()
        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        page = Frame(self)
        page.configure(background='black')
        page.pack(side=LEFT,anchor='w',fill='both')
        outputText = Text(self)
        self.configure(background='black')
        scroll = Scrollbar(page, command=outputText.yview,background='black')
        outputText.configure(yscrollcommand=scroll.set,background='black',highlightbackground='black')
        outputText.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
        outputText.tag_configure('big', font=('Verdana', 16, 'bold'),foreground='white')
        outputText.tag_configure('color', foreground='grey', 
                                                        font=('Tempus Sans ITC', 12, 'bold'))
        outputText.pack(side=LEFT,fill='both',anchor='e')

        scroll.pack(side=RIGHT, fill=Y,anchor='w')
        path = "VivacityTitle.gif"
        photo = PhotoImage(file=path)
        label = tk.Label(page, image=photo,background='black')#, font=LARGE_FONT,fg='white',background='black')
        label.image = photo
        label.pack()

        
        def fetch(entries,Preview):
            outputText.insert(END, 'Writing File to '+str(entries[0][1].get()),'color')
            MakeFile(str(entries[0][1].get()),Preview)
        def MakeFile(title,Preview):
            if Preview:
                PrintInformation()
            else:
                File = codecs.open('../../../'+title,mode='w+',encoding='utf-8')
##                File = codecs.open(title,mode='w+',encoding='utf-8')
                WriteInformation(File)
                File.close()
        
        def WriteInformation(File):
            Dists = []
            Keys = []
            File.write('This file contains the sections pertaining to:\nDistricts: ')
            for i,val in enumerate(DistrictVar):
                if val.get():
                    File.write(', '+Districts[i])
                    Dists.append(Districts[i])
            File.write('\nKeyWords: ')
            for i,val in enumerate(KeyVar):
                if val.get():
                    Keys.append(i)#KeyWords[i])
                    File.write(', '+KeyWords[i])
                  
            DistrictSections = FindDistrictSections(Dists)
            if len(Keys) > 0: #no keys selected, still output districts
                Sections,TieKeys = FindKeys(Keys,DistrictSections)
            else:
                Sections = DistrictSections
                TieKeys = None
                
            WriteSections(File,Sections,TieKeys)
            
        def PrintInformation():
            outputText.delete('1.0', 'end')
            Dists = []
            Keys = []
            outputText.insert(END,'This file contains the sections pertaining to:\nDistricts: ','color')
            for i,val in enumerate(DistrictVar):
                if val.get():
                    outputText.insert(END,', '+Districts[i],'color')
                    Dists.append(Districts[i])
            outputText.insert(END,'\nKeyWords: ','color')
            for i,val in enumerate(KeyVar):
                if val.get():
                    Keys.append(i)#KeyWords[i])
                    outputText.insert(END,', '+KeyWords[i],'color')
                 
            DistrictSections = FindDistrictSections(Dists)
            if len(Keys) > 0: #no keys selected, still output districts
                Sections,TieKeys = FindKeys(Keys,DistrictSections)
            else:
                Sections = DistrictSections
                TieKeys = None
        
            PrintSections(Sections,TieKeys)
        def Clear():
            outputText.delete('1.0', 'end')
            
        def PrintSections(Sections,TieKeys):
            outputText.insert(END,'\nTotal number of sections: '+str(len(Sections))+'\nSectionList:\n','color')
            for item in Sections:
                outputText.insert(END,Doc.ZoningIDs[item]+', ','color')
                
            outputText.insert(END,'\n\n\n\n','color') 
            for sec in Sections:
                outputText.insert(END,'#################################################################\n','color')
                outputText.insert(END,'Index: '+str(sec)+'\n','color')
                outputText.insert(END,'Zone ID: '+Doc.ZoningIDs[sec]+'\n','color')
                outputText.insert(END,'\nZone References: \n','color')
                for item in Doc.Zone_References[sec]:
                    outputText.insert(END,item+', ','color')
                outputText.insert(END,'\nDistrict References: \n','color')
                for item in Doc.District_References[sec]:
                    outputText.insert(END,item+', ','color')
                if TieKeys:
                    outputText.insert(END,'\nKey Words: \n','color')
                    outputText.insert(END,[item for item in TieKeys[sec]],'color')
                    
                outputText.insert(END,'\n#################################################################\n','color')
                outputText.insert(END,'\n'+Doc.Sections[sec],'color')
            
        def makeform(self, fields):
           entries = []
           for field in fields:
              row = Frame(page)
              lab = Label(row, width=15, text=field, anchor='w',highlightbackground='black',bg='black',fg='white')
              ent = Entry(row)
              row.pack(side=TOP, fill=X, padx=5, pady=5)
              lab.pack(side=LEFT)
              ent.pack(side=RIGHT, expand=YES, fill=X)
              entries.append((field, ent))
           return entries
        
        fields = 'File Name',
        ents = makeform(self, fields)
        self.bind('<Return>', (lambda event, e=ents: fetch(e))) 
        
        button0 = tk.Button(page, text="Zoning Viewer",height=2,command=lambda:controller.show_frame(DocumentViewPage),highlightbackground=VivacityColors[2])
        button0.pack(fill=X,padx=5,pady=2)
        button6 = tk.Button(page, text="Sentence Labeler",height=2,command=lambda:controller.show_frame(SentenceLabelPage),highlightbackground=VivacityColors[2])
        button6.pack(fill=X,padx=5,pady=2)
        button1 = tk.Button(page, text="Filter Districts",height=2,command=lambda:controller.show_frame(DistrictsPage),highlightbackground=VivacityColors[3])
        button1.pack(fill=X,padx=5,pady=2)
        button2 = tk.Button(page, text="Filter KeyWords",height=2,command=lambda:controller.show_frame(KeyWordsPage),highlightbackground=VivacityColors[3])
        button2.pack(fill=X,padx=5,pady=2)
        button3 = tk.Button(page, text="Show Filters",height=2,command=lambda:ShowFilters(),highlightbackground=VivacityColors[4])
        button3.pack(fill=X,padx=5,pady=2)
        button5 = Button(page, text='Show Preview',
              command=(lambda e=ents: fetch(e,True)),height=2,highlightbackground=VivacityColors[4])
        button5.pack(fill=X,padx=5,pady=2)

        button4 = Button(page, text='Save Primer',
              command=(lambda e=ents: fetch(e,False)),height=2,highlightbackground=VivacityColors[5])
        button4.pack(fill=X,padx=5,pady=2)
        b2 = Button(page, height=2,text='Clear',
              command=(lambda e=ents: Clear()),highlightbackground=VivacityColors[6])
        b2.pack(side=TOP, padx=5,fill=X,pady=2)


 
        def ShowFilters():
            outputText.delete('1.0', 'end')
            outputText.insert(END,'\nDistricts:\n', 'big')
            for i,val in enumerate(DistrictVar):
                if val.get():
                    outputText.insert(END,Districts[i]+'\n', 'color') 
            outputText.insert(END,'\nKey Words:\n', 'big')
            for i,val in enumerate(KeyVar):
                if val.get():
                    outputText.insert(END,KeyWords[i]+'\n', 'color')
            
        
class DistrictsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        page2 = Frame(self)
        page2.configure(background='black')
        page2.pack(side=LEFT,anchor='e',fill='x',padx=20)
        label2 = tk.Label(page2, font=LARGE_FONT,bg='black',fg='black',width=5)
        label2.pack(padx=10,pady=10,fill=Y,side=LEFT)
        label2 = tk.Label(page2, text="Residential", font=LARGE_FONT,bg=VivacityColors[2],fg='black',width=15)
        label2.pack(padx=10,pady=10,fill=X,side=TOP)
        label3 = tk.Label(page2, text="Commercial", font=LARGE_FONT,bg=VivacityColors[4],fg='black',width=15)
        label3.pack(padx=10,pady=10,fill=X,side=TOP)
        label4 = tk.Label(page2, text="Manufacturing", font=LARGE_FONT,bg=VivacityColors[5],fg='black',width=15)
        label4.pack(padx=10,pady=10,side=TOP)
        label5 = tk.Label(page2, text="Limited Height", font=LARGE_FONT,bg=VivacityColors[0],fg='black',width=15)
        label5.pack(padx=10,pady=10,side=TOP)
        label5 = tk.Label(page2, text="Special Districts", font=LARGE_FONT,bg=VivacityColors[7],fg='black',width=15)
        label5.pack(padx=10,pady=10,side=TOP)
        
        self.configure(background='black')
        label = tk.Label(self, text="Districts", font=LARGE_FONT,fg='white',bg='black')
        label.pack(padx=10,pady=10)
        vsb = tk.Scrollbar(orient="vertical")
        text = tk.Text(self, width=30, height=20, yscrollcommand=vsb.set,background='black',highlightbackground='black')
        vsb.config(command=text.yview)
        vsb.pack(side="right",fill="y")
        text.pack(side=TOP,fill='both',expand=True,padx=10,pady=10)
        Boxes = {}
        color=0
        SortSections=[[],[],[],[],[]]
        for x,key in enumerate(Districts):
            DistrictVar.append(tk.IntVar())
            if key in SpecialDists:
                SortSections[4].append((key,7,x))
            elif key[0] == 'M':
                SortSections[2].append((key,5,x))
            elif key[0] == 'C':
                SortSections[1].append((key,4,x))
            elif key[0] == 'R':
                SortSections[0].append((key,2,x))
            else:
                SortSections[3].append((key,0,x))
        for List in SortSections:
            for tup in List:
                Boxes[tup[2]]=(tk.Checkbutton(self,text=tup[0], bg=VivacityColors[tup[1]],variable=DistrictVar[tup[2]],width=40))
                text.window_create("end", window=Boxes[tup[2]])
                text.tag_configure("center", justify='center')
                text.tag_add("center", 1.0, "end")
                text.insert("end", "\n",'center') # to force one checkbox per line
        button1 = tk.Button(self,  width=37,height=2,text="Back",command=lambda:controller.show_frame(StartPage),highlightbackground=VivacityColors[7])
        button1.pack()
        
        
class DocumentViewPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        page = Frame(self)
        page.configure(background='black')
        page.pack(side=LEFT,anchor='w',fill='both')
    
        self.configure(background='black',highlightbackground='black')
        outputText = Text(self,highlightbackground='black',bg='black',fg='white')#, height=20, width=50)
        scroll = Scrollbar(page, command=outputText.yview)
        outputText.configure(yscrollcommand=scroll.set)
        outputText.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
        outputText.tag_configure('big', font=('Verdana', 20, 'bold'))
        outputText.tag_configure('color', foreground='grey',
                                                        font=('Tempus Sans ITC', 12, 'bold'))#476042
        outputText.pack(side=LEFT,fill='both',anchor='w')
        scroll.pack(side=RIGHT, fill=Y)
        label = tk.Label(page, text="Zone Viewer", font=LARGE_FONT,bg='black',fg='white')
        label.pack(padx=10,pady=10,)
        

        
        Attributes = {1:Doc.Sections,
              2:Doc.Sections,
              3:Doc.ZoningIDs,
              4:Doc.Zone_References,
              5:Doc.District_References,
              6:Doc.KeyWords
          
          }
        Options = [
            ("Raw Text",1),
            ("Formatted Text",2),
            ("Zoning ID",3),
            ("Zone References",4),
            ("District References",5),
            ("Key Words",6),   
        ]
        RadioVar = IntVar()
        RadioVar.set(1)  # initializing the choice, i.e. Python
        color=0
        for txt, val in Options:
            btn = Radiobutton(page, 
                        text=txt,
                        padx = 20,
                        variable=RadioVar,
                        value=val,foreground='white',highlightbackground='grey',bg='#666666')#VivacityColors[color])
            btn.config(fg='white')
            btn.pack(anchor=W,side=TOP,fill='x',padx=5)
            color+=1

        fields = 'File Name','Index Number','Zoning ID'
        ActionIndicator = "#################################################################"
        
        def fetch(entries,TstWrite):
            if not len(Inquiry[1].get()) == 0: #index
                if '-' in Inquiry[1].get():
                    Range = str(Inquiry[1].get()).split("-")
                    Action(int(RadioVar.get()),int(Range[0]),int(Range[1]),entries,TstWrite)
                else:
                    num = int(Inquiry[1].get())
                    Action(int(RadioVar.get()),num,num,entries,TstWrite)                  
            elif not len(Inquiry[2].get()) == 0: #zone
                Action(int(RadioVar.get()),Doc.IDtoIndex[Inquiry[2].get()],Doc.IDtoIndex[Inquiry[2].get()],entries,TstWrite)

            return None
        def Clear():
            outputText.delete('1.0', 'end')
        def Action(Type, Start,Stop,entries,TstWrite):
            if TstWrite:
                txt = open(Inquiry[0].get(),mode="w+")
            for i in range(3):
                outputText.insert(END,ActionIndicator+'\n','color')
            for i in range(Start,Stop+1):
                if Type == 1:        #Want raw text
                    if TstWrite:
                        txt.write(str(i)+': '+Attributes[Type][i].encode('utf-8')+'\n')
                    else:
                        outputText.insert(END,repr(Attributes[Type][i])+'\n','color')
                elif Type == 2 or Type == 3:
                    if TstWrite:
                        txt.write(str(i)+': '+Attributes[Type][i].encode('utf-8')+'\n')
                    else:
                        outputText.insert(END,str(i)+': '+Attributes[Type][i]+'\n','color')
                else:
                    outputText.insert(END,'Index '+str(i)+': \n','color')
                    for item in Attributes[Type][i]:
                        outputText.insert(END,'\t'+item+'\n','color')
                    
            if TstWrite:
                txt.close()
                
                    
        def makeform(self, fields):
            entries = []
            for i,field in enumerate(fields):
              row = Frame(page)
              Inquiry.append(StringVar())
              lab = Label(row, width=15, text=field, anchor='w',bg='black',fg='white',highlightbackground='black')
              ent = Entry(row,textvariable=Inquiry[i])
              row.pack(side=TOP, padx=5, pady=5,anchor='w')
              lab.pack(side=LEFT,anchor='w')
              ent.pack(side=RIGHT,anchor='w', fill=X,expand=YES)
              entries.append((field, ent))
            entries[1][1].insert(0,'0-'+str(len(Doc.Sections)-1))
            return entries

                            
        
        Inquiry = []
        
        ents = makeform(self, fields)
        self.bind('<Return>', (lambda event, e=ents: fetch(e)))   
        b1 = Button(page, height=2,text='Show Preview',
              command=(lambda e=ents: fetch(e,False)),highlightbackground=VivacityColors[0])
        b1.pack(side=TOP, padx=5,fill=X,pady=1)
        b4 = Button(page, height=2,text='Save to File',
              command=(lambda e=ents: fetch(e,True)),highlightbackground=VivacityColors[5])
        b4.pack(side=TOP, padx=5,fill=X,pady=1)
        b2 = Button(page, height=2,text='Clear',
              command=(lambda e=ents: Clear()),highlightbackground=VivacityColors[6])
        b2.pack(side=TOP, padx=5,fill=X,pady=1)
        b3 = tk.Button(page, height=2,text="Back",command=lambda:controller.show_frame(StartPage),highlightbackground=VivacityColors[7])
        b3.pack(side=TOP,padx=5,fill=X,pady=1)



class SentenceLabelPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        page = Frame(self)
        page.configure(background='black')
        page.pack(side=LEFT,anchor='w',fill='both')
    
        self.configure(background='black',highlightbackground='black')
        outputText = Text(self,highlightbackground='black',bg='black',fg='white')#, height=20, width=50)
        scroll = Scrollbar(page, command=outputText.yview)
        outputText.configure(yscrollcommand=scroll.set)
        outputText.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
        outputText.tag_configure('big', font=('Verdana', 20, 'bold'))
        outputText.tag_configure('color', foreground='grey',
                                                        font=('Tempus Sans ITC', 12, 'bold'))#476042
        outputText.pack(side=LEFT,fill='both',anchor='w')
        scroll.pack(side=RIGHT, fill=Y)
        label = tk.Label(page, text="Sentence Labeler", font=LARGE_FONT,bg='black',fg='white')
        label.pack(padx=10,pady=10,)
        

        
        Attributes = {1:Doc.Sections,
              2:Doc.Sections,
              3:Doc.ZoningIDs,
              4:Doc.Zone_References,
              5:Doc.District_References,
              6:Doc.KeyWords,
              7:Doc.Titles          
          }
        Options = [
            ("Random Sentence",1),
  
        ]
        RadioVar = IntVar()
        RadioVar.set(1)  # initializing the choice, i.e. Python
        color=0
        for txt, val in Options:
            btn = Radiobutton(page, 
                        text=txt,
                        padx = 20,
                        variable=RadioVar,
                        value=val,foreground='white',highlightbackground='grey',bg='#666666')#VivacityColors[color])
            btn.config(fg='white')
            btn.pack(anchor=W,side=TOP,fill='x',padx=5)
            color+=1

        fields = ['File Name','Section']
        ActionIndicator = "_________________________________________________"
        
        def fetch(entries,TstWrite):
            if not len(Inquiry[1].get()) == 0: #index
                if '-' in Inquiry[1].get():
                    Range = str(Inquiry[1].get()).split("-")
                    Action(int(RadioVar.get()),int(Range[0]),int(Range[1]),entries,TstWrite)
                else:
                    num = int(Inquiry[1].get())
                    Action(int(RadioVar.get()),num,num,entries,TstWrite)                  
            elif not len(Inquiry[2].get()) == 0: #zone
                Action(int(RadioVar.get()),Doc.IDtoIndex[Inquiry[2].get()],Doc.IDtoIndex[Inquiry[2].get()],entries,TstWrite)

            return None
        def Clear():
            outputText.delete('1.0', 'end')
        def Action(Type, Start,Stop,entries,TstWrite):
            if TstWrite:
                txt = open(Inquiry[0].get(),mode="w+")
            for i in range(3):
                outputText.insert(END,ActionIndicator+'\n','color')
            for i in range(Start,Stop+1):
                if Type == 1:        #Want raw text
                    if TstWrite:
                        txt.write(str(i)+': '+Attributes[Type][i].encode('utf-8')+'\n')
                    else:
                        outputText.insert(END,repr(Attributes[Type][i])+'\n','color')
                elif Type == 2 or Type == 3:
                    if TstWrite:
                        txt.write(str(i)+': '+Attributes[Type][i].encode('utf-8')+'\n')
                    else:
                        outputText.insert(END,str(i)+': '+Attributes[Type][i]+'\n','color')
                else:
                    outputText.insert(END,'Index '+str(i)+': \n','color')
                    for item in Attributes[Type][i]:
                        outputText.insert(END,'\t'+item+'\n','color')
                    
            if TstWrite:
                txt.close()
                
                    
        def makeform(self, fields):
            entries = []
            for i,field in enumerate(fields):
              row = Frame(page)
              Inquiry.append(StringVar())
              lab = Label(row, width=15, text=field, anchor='w',bg='black',fg='white',highlightbackground='black')
              ent = Entry(row,textvariable=Inquiry[i])
              row.pack(side=TOP, padx=5, pady=5,anchor='w')
              lab.pack(side=LEFT,anchor='w')
              ent.pack(side=RIGHT,anchor='w', fill=X,expand=YES)
              entries.append((field, ent))
            entries[0][1].insert(0,'SentenceLog.txt')
            return entries

        def ShowSentence(ents):
            Clear()
            ents[1][1].delete('0','end')
            #Grab Random section and sentence
            ind =  random.randint(0,len(Attributes[1])-1)
            section = Attributes[1][ind]
            ents[1][1].insert(0,Attributes[3][ind])
            sentences = section.split('.')
            if len(sentences)>1:
                ind =  random.randint(0,len(sentences)-1)
            else:
                ind = 0
                
            #Remove Unwanted characters in sentences
            sent = sentences[ind]
            stripChars = ['\t','\r\n','\r','\x0c','\n', '  ']
            for char in stripChars:
                sent = sent.replace(char,' ')
                
            #Write to output
            outputText.insert(END,sent,'color')
            
        def LabelSentence(Label,ents):
            sentence = outputText.get("1.0",'end-1c')
            txt = open(Inquiry[0].get(),mode="a")
            txt.write(sentence.encode('utf-8')+'~'+Label+'~'+Inquiry[1].get()+'\n')
            txt.close()
            ShowSentence(ents)
            return None
            

                            
        
        Inquiry = []
        
        ents = makeform(self, fields)
        self.bind('<Return>', (lambda event, e=ents: fetch(e)))   
        b0 = Button(page, height=2,text='Next Sentence',
              command=(lambda e=ents: ShowSentence(e)),highlightbackground=VivacityColors[5])
        b0.pack(side=TOP, padx=5,fill=X,pady=1)
        b1 = Button(page, height=2,text='Good',
              command=(lambda e=ents: LabelSentence('Good',e)),highlightbackground=VivacityColors[6])
        b1.pack(side=TOP, padx=5,fill=X,pady=1)
        b2 = Button(page, height=2,text='Bad',
              command=(lambda e=ents: LabelSentence('Bad',e)),highlightbackground=VivacityColors[4])
        b2.pack(side=TOP, padx=5,fill=X,pady=1)

        b3 = tk.Button(page, height=2,text="Back",command=lambda:controller.show_frame(StartPage),highlightbackground=VivacityColors[7])
        b3.pack(side=TOP,padx=5,fill=X,pady=1)

            
class KeyWordsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.configure(background='black')
        label = tk.Label(self, text="Key Words", font=LARGE_FONT,fg='white',bg='black',highlightbackground='black')
        label.pack(padx=10,pady=10)
        vsb = tk.Scrollbar(orient="vertical")
        text = tk.Text(self, width=30, height=20, yscrollcommand=vsb.set,bg='black',highlightbackground='black')
        vsb.config(command=text.yview)
        vsb.pack(side="right",fill="y")
        text.pack(side="top",fill="both",expand=True,padx=10,pady=10)
        Boxes = []
        color=0
        for x,key in enumerate(KeyWords):
            bg = 'white'
            if x%2==0:
                bg='grey'
            KeyVar.append(tk.IntVar())
            Boxes.append(tk.Checkbutton(self,text=key, bg=bg,variable=KeyVar[x],width=40))
            text.window_create("end", window=Boxes[x])
            text.tag_configure("center", justify='center')
            text.tag_add("center", 1.0, "end")
            text.insert("end", "\n",'center') # to force one checkbox per line

        button1 = tk.Button(self, width=37,height=2,text="Back",command=lambda:controller.show_frame(StartPage),highlightbackground=VivacityColors[7],bg=VivacityColors[7])
        button1.pack()
        

    
def FindKeys(KeyList,DistrictSections): #Sections returned here contain a keyword AND the district
    SectionList = set()
    StripList = ['\r','\n','\x0c']
    TieKeys = {}
    if len(DistrictSections) ==0:#if none selected, search all sections
        DistrictSections = [x for x in range(len(Doc.Sections))]
    for index in KeyList:
        print(KeyWords[index])
        if KeyFind[index] == 'Y':
            for key in KeyBuckets[index]:
                for sec in DistrictSections:
                    for word in Doc.KeyWords[sec]:
                        if key in word:
                            SectionList.add(sec)
                            if sec in TieKeys:
                                TieKeys[sec].add(word)
                            else:
                                TieKeys[sec] = set([word])
        else:
            for key in KeyBuckets[index]:
                for sec in DistrictSections:
                    temp = Doc.Sections[sec]
                    for char in StripList:
                        temp = temp.replace(char,'')
                    if key in temp.lower():
                        SectionList.add(sec)
                        if sec in TieKeys:
                            TieKeys[sec].add(key)
                        else:
                            TieKeys[sec]=set([key])
                        
    return sorted(list(SectionList)),TieKeys


def FindDistrictSections(DistList):
    SectionList = set()
    for district in DistList:
        for i,List in enumerate(Doc.District_References):
            if district in List:
                    SectionList.add(i)
    return sorted(list(SectionList))

def WriteSections(File,Sections,TieKeys):
    File.write('\nTotal number of sections: '+str(len(Sections))+'\nSectionList:\n')
    for item in Sections:
        File.write(item+', ')
    File.write('\n\n\n\n')
    for sec in Sections:
        File.write('#################################################################\n')
        File.write('Index: '+str(sec)+'\n')
        File.write('Zoning ID '+Doc.ZoningIDs[sec]+'\n')
        File.write('\nZone References: \n')
        for item in Doc.Zone_References[sec]:
            File.write(item+', ')
        File.write('\nDistrict References: \n')
        for item in Doc.District_References[sec]:
            File.write(item+', ')   ################ HERE
        if TieKeys:
            File.write('\nKey Words: \n')
            File.write(str(TieKeys[sec]))
        File.write('\n#################################################################\n')
        File.write('\n'+Doc.Sections[sec])





    
KeyWords,KeyFind,KeyBuckets= ExtractKeyBuckets('KeyWords')


Doc = Document("NYZoningResolution.txt")


SpecialDists= ExtractDistricts('SpecialDistricts')
Districts = Doc.DistrictList
KeyVar = []
DistrictVar = []

        
app = Window()
app.mainloop()



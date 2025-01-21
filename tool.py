from tkinter import * 
from tkinter import ttk as ttk
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from PIL import ImageTk, Image
import os


def info():
    mb.showinfo("Info","Either upload sequence file or paste it! You can't do both!")
    root.destroy()
    displayGUI()


def openfile():
    filename=fd.askopenfilename()
    #print(filename)
    e1.insert(0,filename)


def draw_pie(rf_predictions):
    rf_predictions=rf_predictions
    count_p=0
    count_n=0
    sizes=[]
    labels="MTBP","Non-MTBP"
    for ele in rf_predictions:
        if ele==-1:
            count_n+=1
        else:
            count_p+=1
    sizes.append(count_p)
    sizes.append(count_n)
    import matplotlib.pyplot as plt

    
    explode = (0.1,0)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig("Pie-Chart.png")
    plt.show()
    return       
    

def display_result(rf_predictions,report,ids):
    
    rf_predictions=rf_predictions.tolist()
    
    root2=Toplevel()
    root2.title("MTBPred-Results")
    
    root2.geometry("600x620+100+100")
    root2.resizable(False,False)
    root2.config(background="lavender blush")
    logo = ImageTk.PhotoImage(Image.open("logo.jpg"))
    juitlogo = ImageTk.PhotoImage(Image.open("JP Logo.png"))
    text=StringVar()

    w1 = tk.Label(root2, image=logo)
    w1.image=logo
    w1.place(x=10,y=20)
    w2 = tk.Label(root2, image=juitlogo)
    w2.image=juitlogo
    w2.place(x=470,y=15)
    
    l1=Label(root2,text="MTBPred-Results",fg="white",bg="pale violet red",font="Calibri 20 bold",relief=RIDGE,padx=10)
    l1.place(x=230,y=55)
    count_p=0
    count_n=0
    sizes=[]
    
    for ele in rf_predictions:
        if ele==-1:
            count_n+=1
        else:
            count_p+=1
    sizes.append(count_p)
    sizes.append(count_n)
    class_count="Out of "+str(len(rf_predictions))+" sequences in the input file:\n"+str(sizes[0])+" are MTBPs,Class=1\n"+str(sizes[1])+" are non-MTBPs,Class=-1\n"
    output="\nPlease wait till the Output file is saved to the MTBP \nfolder."
    result="Overall statistics of the model:-\n\n"+str(report)+"\n        ------------------------------------------------\n"+class_count+output
    ta=Text(root2,height=20,width=65,bg="white")
    ta.insert(tk.END,result)
    ta.place(x=40,y=170)
    draw_pie(rf_predictions)
    
    ids=ids.tolist()
    output_file=open("Output.csv","w+")
    id_class=dict(zip(ids,rf_predictions))
    col_headers=output_file.write("Seq Id,Predicted Class,Predicted Class Label\n")
    for key in id_class:
        if id_class[key]==1:
            line=str(key)+","+str(id_class[key])+","+"MTBP"+"\n"
            output_file.write(line)
        else:
            line=str(key)+","+str(id_class[key])+","+"Non-MTBP"+"\n"
            output_file.write(line)
            
    output_file.close()
    return
       
def predict_svm(inputdata,test,g,c):
    import pandas as pd
    import numpy as np
    
    from sklearn.metrics import classification_report, confusion_matrix
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import cross_val_score
    
    from sklearn.svm import SVC

    
    X = inputdata.drop(['#','Class'],axis=1)
    y = inputdata['Class']
    ids=test['#']
    test=test.drop('#',axis=1)
   
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)


    svclassifier = SVC(kernel='rbf', C=c, gamma=g)

    svclassifier.fit(X_train, y_train)
    
    print(svclassifier.score(X_test,y_test))
    y_pred = svclassifier.predict(test)
   
    pred=svclassifier.predict(X_test)

    
    report=classification_report(y_test,pred)

    display_result(y_pred,report,ids)
    
    return

def predict_rfc(inputdata,test,n_estimators,max_depth):
    import pandas as pd
    import numpy as np
    from sklearn.metrics import classification_report, confusion_matrix
    from sklearn.metrics import accuracy_score
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn import model_selection
    
    X = inputdata.drop(['#','Class'], axis=1)
    y = inputdata['Class']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state=80)
    ids=test['#']
    test=test.drop('#', axis=1)

    # random forest model creation
    rfc = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, bootstrap = True)
    rfc.fit(X_train,y_train)
    # predictions
    pred = rfc.predict(X_test)
    
    rf_predictions = rfc.predict(test)
    # Probabilities for each class
    #rf_probs = rfc.predict_proba(test)[:, 1]
    
    report=classification_report(y_test,pred)
    accuracy=accuracy_score( y_test,pred)
    display_result(rf_predictions,report,ids)
    return

def load_file(a,b,c,d,e):
    import pandas as pd
    if a==1:
        inputdata = pd.read_csv("APAAC_input.csv")
        test=pd.read_csv("APAAC_test.csv").fillna(0)
        if n1.get()==1:
            n_estimators=32
            max_depth=120
            predict_rfc(inputdata,test,n_estimators,max_depth)
        if n1.get()==2:
            g=0.005
            c=91
            predict_svm(inputdata,test,g,c)
    if b==1:
        inputdata = pd.read_csv("CTDC_input.csv")
        test=pd.read_csv("CTDC_test.csv").fillna(0)
        if n1.get()==1:
            n_estimators=16
            max_depth=150
            predict_rfc(inputdata,test,n_estimators,max_depth)
        if n1.get()==2:
            g=16
            c=31
            predict_svm(inputdata,test,g,c)
    
    if c==1:
        inputdata = pd.read_csv("CTDT_input.csv")
        test=pd.read_csv("CTDT_test.csv").fillna(0)
        if n1.get()==1:
            n_estimators=200
            max_depth=150
            predict_rfc(inputdata,test,n_estimators,max_depth)
        if n1.get()==2:
            g=20
            c=11
            predict_svm(inputdata,test,g,c)
        
    if d==1:
        inputdata = pd.read_csv("NMBroto_input.csv")
        test=pd.read_csv("NMBroto_test.csv").fillna(0)
        if n1.get()==1:
            n_estimators=32
            max_depth=170
            predict_rfc(inputdata,test,n_estimators,max_depth)
        if n1.get()==2:
            g=2
            c=11
            predict_svm(inputdata,test,g,c)
    if e==1:
        inputdata = pd.read_csv("DPC_input.csv")
        test=pd.read_csv("DPC_test.csv").fillna(0)
        if n1.get()==1:
            n_estimators=64
            max_depth=110
            predict_rfc(inputdata,test,n_estimators,max_depth)
        if n1.get()==2:
            g=19
            c=46
            predict_svm(inputdata,test,g,c)
    return
    
def write_input_file(fh,fh2,a,b,c,d,e):
    string=""
    first_line=next(fh)
    string=",".join(first_line)
    fh2.write(string+"\n")
    string=""   
    for line in fh:
        string=",".join(line)
        string=string+"\n"
        fh2.write(string)
        string=""
    
    fh2.close()
    load_file(a,b,c,d,e)
    return

def prepare_input_file(a,b,c,d,e):
    import csv
    if a==1:
        fh=fh=csv.reader(open("APAAC.tsv"),delimiter="\t")
        fh2=open("APAAC_test.csv","w+")
        write_input_file(fh,fh2,a,b,c,d,e)
    if b==1:
        fh=fh=csv.reader(open("CTDC.tsv"),delimiter="\t")
        fh2=open("CTDC_test.csv","w+")
        write_input_file(fh,fh2,a,b,c,d,e)
    if c==1:
        fh=fh=csv.reader(open("CTDT.tsv"),delimiter="\t")
        fh2=open("CTDT_test.csv","w+")
        write_input_file(fh,fh2,a,b,c,d,e)
    if d==1:
        fh=fh=csv.reader(open("NMBroto.tsv"),delimiter="\t")
        fh2=open("NMBroto_test.csv","w+")
        write_input_file(fh,fh2,a,b,c,d,e)
    if e==1:
        fh=fh=csv.reader(open("DPC.tsv"),delimiter="\t")
        fh2=open("DPC_test.csv","w+")
        write_input_file(fh,fh2,a,b,c,d,e)
    return
  

def extractfeature(filename):
    import os
    import shutil
    path, fn = os.path.split(filename)
    loc=os.getcwd()
    loc=str(loc)
    loc=loc.replace("\\","/")
    locforcopy=loc+"/iFeature/examples"
    locforifeature=loc+"/iFeature/iFeature.py"
    shutil.copy(filename,locforcopy)
    
    if n2.get()==3:
        a=1
        b=0
        c=0
        d=0
        e=0
        command="python "+locforifeature+" --file "+locforcopy+"/"+str(fn)+" --type APAAC --out APAAC.tsv"
        os.system(command)
        prepare_input_file(a,b,c,d,e)
        return
    if n2.get()==4:
        a=0
        b=1
        c=0
        d=0
        e=0
        command="python "+locforifeature+" --file "+locforcopy+"/"+str(fn)+" --type CTDC --out CTDC.tsv"
        os.system(command)
        prepare_input_file(a,b,c,d,e)
        return
    if n2.get()==5:
        a=0
        b=0
        c=1
        d=0
        e=0
        command="python "+locforifeature+" --file "+locforcopy+"/"+str(fn)+" --type CTDT --out CTDT.tsv"
        os.system(command)
        prepare_input_file(a,b,c,d,e)
        return
    if n2.get()==6:
        a=0
        b=0
        c=0
        d=1
        e=0
        command="python "+locforifeature+" --file "+locforcopy+"/"+str(fn)+" --type NMBroto --out NMBroto.tsv"
        os.system(command)
        prepare_input_file(a,b,c,d,e)   
        return
    if n2.get()==7:
        a=0
        b=0
        c=0
        d=0
        e=1
        command="python "+locforifeature+" --file "+locforcopy+"/"+str(fn)+" --type DPC --out DPC.tsv"
        os.system(command)
        prepare_input_file(a,b,c,d,e)
        return
          
    #print(fn)
    
    

def checkforambigouscharacter(filename):
    fh=open(filename,"r")
    headerList = []
    seqList = []
    currentSeq = ''
    for line in fh:
       if line[0] == ">":
          headerList.append(line[1:].strip())
          if currentSeq != '':
             seqList.append(currentSeq)

          currentSeq = ''
       else:
          currentSeq += line.strip()

    seqList.append(currentSeq)
    for seq in seqList:     
        c=seq.count("B")
        d=seq.count("J")
        e=seq.count("O")
        f=seq.count("U")
        g=seq.count("X")
        h=seq.count("Z")
                
        if c>0 or d>0 or e>0 or f>0 or g>0 or h>0:
            mb.showerror("Error","File contains ambiguous amino acids!")
            root.destroy()
            displayGUI()
            return
        else:
            
            extractfeature(filename)
            return




def check_input_file(event):
    text=scr.get('1.0', 'end-1c')
    if text=="":
        filename=str(e1.get())
        if filename =="":
            info()   
        else:
            result=re.search(r'\.([A-Za-z0-9]+$)',filename)
            if result:
                fileformat=str(result.group(1))
                fileformat=fileformat.lower()
                
                if fileformat!="fasta":
                    
                    e1.delete(0,'end')
                    mb.showerror("Error","Only FASTA files supported!")
                    root.destroy()
                    displayGUI()
                else:
                    e1.delete(0,'end')                
                    checkforambigouscharacter(filename)
            else:
                e1.delete(0,'end')
                mb.showerror("Error","Only FASTA files supported!")
                root.destroy()
                displayGUI()
    else:
        filename=str(e1.get())
        if filename !="":
            info()
        else:
            if text[0]!=">":
                mb.showerror("Error","Only FASTA format supported!")
                root.destroy()
                displayGUI()
            else:
                fh=open("InputSequences.fasta","w+")
                
                fh.write(text)
                fh.close()
                checkforambigouscharacter(str(fh.name))
                
    

            
def cancel(event):
    e1.delete(0,'end')
    
def exitfn(event):
    b=mb.askyesno("confirmation","Do you want to exit?")
    if(b):
        root.destroy()
            


def displayGUI():
    from tkinter import scrolledtext 
    global w1,l1,bt,e1,l2,n1,root,rb1,rb2,bt2,bt3,bt4,n2,scr,text
    root=Tk()
    root.title("MTBPred")
    root.geometry("600x600")
    root.geometry("600x600+100+100")
    root.resizable(False,False)
    root.config(background="lavender blush")
    logo = ImageTk.PhotoImage(Image.open("logo.jpg"))
    juitlogo = ImageTk.PhotoImage(Image.open("JP Logo.png"))
    text=StringVar()

    w1 = tk.Label(root, image=logo)
    w1.image=logo
    w1.place(x=10,y=20)
    w2 = tk.Label(root, image=juitlogo)
    w2.image=juitlogo
    w2.place(x=470,y=15)


    l1=Label(root,text="MTBPred",fg="white",bg="pale violet red",font="Calibri 20 bold",relief=RIDGE,padx=10)
    l1.place(x=275,y=50)

    bt=Button(root,text="Click here to browse File",fg="white",bg="pale violet red",width=20,font="Arial 10 bold",command=openfile)
    bt.place(x=20,y=150)

    e1=Entry(root,width=55)
    e1.place(x=210,y=155)
    scrolW=40  
    scrolH=7  
    scr=scrolledtext.ScrolledText(root, width=scrolW, height=scrolH, wrap=tk.WORD)
    scr.place(x=210,y=190)
    l2=Label(root,text="Choose classifier:",fg="white",bg="pale violet red",font="Calibri 11 bold" )
    l3=Label(root,text="Choose feature:",fg="white",bg="pale violet red",font="Calibri 11 bold" )
    l4=Label(root,text="OR Paste FASTA Sequence(s):",fg="white",bg="pale violet red",font="Calibri 11 bold" )
    l2.place(x=40,y=330)
    l3.place(x=40,y=380)
    l4.place(x=20,y=190)
    n1=IntVar()
    n2=IntVar()
    rb1=Radiobutton(root,text="Random Forest",variable=n1,value=1,bg="light pink")
    rb2=Radiobutton(root,text="Support Vector Machine",variable=n1,value=2,bg="light pink")
    rb3=Radiobutton(root,text="APAAC",variable=n2,value=3,bg="light pink")
    rb4=Radiobutton(root,text="CTDC",variable=n2,value=4,bg="light pink")
    rb5=Radiobutton(root,text="CTDT",variable=n2,value=5,bg="light pink")
    rb6=Radiobutton(root,text="NMBroto",variable=n2,value=6,bg="light pink")
    rb7=Radiobutton(root,text="DPC",variable=n2,value=7,bg="light pink")

    rb1.place(x=210,y=330)
    rb2.place(x=330,y=330)
    rb3.place(x=210,y=380)
    rb4.place(x=210,y=400)
    rb5.place(x=210,y=420)
    rb6.place(x=210,y=440)
    rb7.place(x=210,y=460)



    bt2=Button(root,text="Predict",fg="white",bg="pale violet red",width=10,font="Arial 10 bold")
    bt2.place(x=180,y=520)
    bt2.bind('<Button>',check_input_file)
    bt3=Button(root,text="Cancel",fg="white",bg="pale violet red",width=10,font="Arial 10 bold")
    bt3.bind('<Button>',cancel)
    bt3.place(x=280,y=520)
    bt4=Button(root,text="Exit",fg="white",bg="pale violet red",width=10,font="Arial 10 bold")
    bt4.place(x=380,y=520)
    bt4.bind('<Button>',exitfn)


displayGUI()

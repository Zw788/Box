
# coding: utf-8

# In[2]:


import xlrd
import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter
import scipy.stats as st
import re 

def sortit( l=None ):  #sorting
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)


# In[4]:


pbook = xlrd.open_workbook("C:\\Users\Zhonghan\Desktop\PACE_DATA_From_Validation.xls").sheet_by_index(0)

def pace_getname(name=None):
    A=pbook.row_values(2) #'METHOD', 'ISOTOPE', 'Lab Sample ID', 'MATRIX', 'CONC', '2 S', 'MDC', 'QUALIFIERS', 'QUALIFIER', 'UNITS' 'Client Sample ID'     
    for i in np.arange(len(pbook.col_values(0))):
        if pbook.cell(i,1).value == name:
            B=pbook.row_values(i)
            for j in np.arange(50):
                if pbook.cell(i-j,0).value.find('-SB')+1 or pbook.cell(i-j,0).value.find('RB-0')+1 :
                    B[-1]=pbook.cell(i-j,0).value
                    break
            A=np.vstack([A,B])
    return(A)


# In[5]:


K40=pace_getname(name="Potassium-40")

U235_236 =pace_getname(name="U235_236")
U235 =pace_getname(name="Uranium-235")

Th232 =pace_getname(name="Thorium-232")
Ra228 =pace_getname(name="Radium-228")
Th228 =pace_getname(name="Thorium-228")
Pb212 =pace_getname(name="Lead-212")
Bi212 =pace_getname(name="Bismuth-212")
Tl208 =pace_getname(name="Thallium-208")

U238 =pace_getname(name="Uranium-238")
Th234 =pace_getname(name="Thorium-234")
U233_234 =pace_getname(name="U233_234")
Th230 =pace_getname(name="Thorium-230")
Ra226 =pace_getname(name="Radium-226")
Pb210 =pace_getname(name="Lead-210")

ID=np.array(list(set(xlrd.open_workbook("C:\\Users\Zhonghan\Desktop\PACE_DATA_From_Validation.xls").sheet_by_index(1).col_values(0))))

cluster=np.array([K40,U235_236,U235,Th232,Ra228,Th228,Pb212,Bi212,Tl208,U238,Th234,U233_234,Th230,Ra226,Pb210])

def pace_plot(A=None): #  A is an array of index of cluster
    x = np.arange(len(ID))
    plt.figure(figsize=(15,10))
    a=[]
    Title = "Plot of " 
    for i in A:
        error=[]
        y = []
        for j in ID:
            if j in cluster[i][:,-1]:
                val=float(cluster[i][list(cluster[i][:,-1]).index(j),4])
                val2=float(cluster[i][list(cluster[i][:,-1]).index(j),5])
                error=np.append(error,val2)
                y=np.append(y,val)
            else:
                error=np.append(error,0)
                y=np.append(y,0)
        plt.plot(x,y,"o",linestyle="None",label=cluster[i][1,1])
        plt.errorbar(x, y, yerr=error,capsize=5,linestyle="None",barsabove=True,elinewidth=.5,ecolor='black')
        plt.xticks(x,ID,rotation=90)
        Title += cluster[i][1,1] + ", "
        a=np.ndarray.flatten(np.append(np.append(a,y-error),y+error))
    plt.legend(loc=3,fontsize=10)
    plt.title(Title)
    plt.ylabel('Specific Activity, $pCi/g$')
    plt.xlabel('Locations')
    plt.yticks(np.linspace(np.floor(min(a)), np.ceil(max(a)), 20))
    plt.grid()
    plt.show()

def pace_compare(pairs=None): # pairs is a 1x2 array, (parent/daughter)
    x = []
    plt.figure(figsize=(15,10))
    Title= cluster[pairs[0]][1,1] + " vs. " + cluster[pairs[1]][1,1]
    y = []
    for j in ID:
        if j in cluster[pairs[0]][:,-1] and j in cluster[pairs[1]][:,-1] :
            val=[float(cluster[pairs[k]][list(cluster[pairs[k]][:,-1]).index(j),4]) for k in [0,1]]
            y=np.append(y,val[0])
            x=np.append(x,val[1])
    plt.plot(x,y,"o")
    m, b, r2=st.linregress(x,y)[:3]
    best=lambda x:m*x+b
    if max(x)<max(y):
        plt.plot(y,best(y),label=r"$y=$"+str(m)+r"$x+$"+str(b)+","+r"  $R^2 =$"+str(r2))
    else:
        plt.plot(x,best(x),label=r"$y=$"+str(m)+r"$x+$"+str(b)+","+r"  $R^2 =$"+str(r2))
    plt.title(Title)
    plt.legend(loc=4,fontsize=15)
    plt.ylabel(cluster[pairs[0]][1,1])
    plt.xlabel(cluster[pairs[1]][1,1])
    plt.xticks(np.linspace(np.floor(min(x)),np.ceil(max(x)),10))
    plt.yticks(np.linspace(np.floor(min(y)),np.ceil(max(y)),10))
    plt.grid()
    plt.show()


# In[6]:


nbook = xlrd.open_workbook("C:\\Users\Zhonghan\Desktop\\NAREL_DATA_From_Validation.xlsx").sheet_by_index(0)
names=["Thorium-232","Radium-228","Thorium-228","Lead-212","Bismuth-212","Thallium-208","Uranium-238","Thorium-234","Uranium-234","Thorium-230","Radium-226","Lead-214","Bismuth-214","Lead-210","Uranium-235","Thorium-227","Bismuth-207","Caesium-137","Europium-155","Potassium-40"]       
def narel_getname(name=None):
    A=nbook.row_values(1) #'METHOD', 'ISOTOPE', 'Lab Sample ID', 'CONC', '2 S', 'MDC', 'I-QUALIFIERS', 'F-QUALIFIER', 'UNITS' 'Client Sample ID'     
    for i in np.arange(len(nbook.col_values(1))):
        if nbook.cell(i,1).value == name:
            B=nbook.row_values(i)
            for j in np.arange(50):
                if nbook.cell(i-j,0).value.find('-SB')+1:
                    B[-1]=nbook.cell(i-j,0).value
                    break
            A=np.vstack([A,B])
    return(A)


# In[7]:


Th232_ =narel_getname(names[0])
Ra228_ =narel_getname(names[1])
Th228_ =narel_getname(names[2])
Pb212_ =narel_getname(names[3])
Bi212_ =narel_getname(names[4])
Tl208_ =narel_getname(names[5])

U238_ =narel_getname(names[6])
Th234_ =narel_getname(names[7])
U234_ =narel_getname(names[8])
Th230_ =narel_getname(names[9])
Ra226_ =narel_getname(names[10])
Pb214_ =narel_getname(names[11])
Bi214_ =narel_getname(names[12])
Pb210_ =narel_getname(names[13])

U235_ =narel_getname(names[14])
Th227_ =narel_getname(names[15])

K40_ =narel_getname(names[-1])

ncluster=np.array([Th232_,Ra228_,Th228_,Pb212_,Bi212_,Tl208_,U238_,Th234_,U234_,Th230_,Ra226_,Pb214_,Bi214_,Pb210_,U235_,Th227_,K40_])                
locs=np.array(list(set(np.ndarray.tolist(ncluster[6][1:,-1]))))


# In[8]:


def narel_plot(A=None): #  A is an array of index of cluster
    x = np.arange(len(locs))
    plt.figure(figsize=(15,10))
    a=[]
    Title = "Plot of " 
    for i in A:
        error=[]
        y = []
        for j in locs:
            if j in ncluster[i][:,-1]:
                val=float(ncluster[i][list(ncluster[i][:,-1]).index(j),3])
                val2=float(ncluster[i][list(ncluster[i][:,-1]).index(j),4])
                error=np.append(error,val2)
                y=np.append(y,val)
            else:
                error=np.append(error,0)
                y=np.append(y,0)
        plt.plot(x,y,"o",linestyle="None",label=ncluster[i][1,1])
        plt.errorbar(x, y, yerr=error,capsize=5,linestyle="None",barsabove=True,elinewidth=.5,ecolor='black')
        plt.xticks(x,locs,rotation=90)
        Title += ncluster[i][1,1] + ", "
        a=np.ndarray.flatten(np.append(np.append(a,y-error),y+error))
    plt.legend(loc=3,fontsize=10)
    plt.title(Title)
    plt.ylabel('Specific Activity, $pCi/g$')
    plt.xlabel('Locations')
    plt.yticks(np.linspace(np.floor(min(a)), np.ceil(max(a)), 20))
    plt.grid()
    plt.show()

def narel_compare(pairs=None): # pairs is a 1x2 array, (parent/daughter)
    x = []
    plt.figure(figsize=(15,10))
    Title= ncluster[pairs[0]][1,1] + " vs. " + ncluster[pairs[1]][1,1]
    y = []
    for j in locs:
        if j in ncluster[pairs[0]][:,-1] and j in ncluster[pairs[1]][:,-1] :
            val=[float(ncluster[pairs[k]][list(ncluster[pairs[k]][:,-1]).index(j),3]) for k in [0,1]]
            y=np.append(y,val[0])
            x=np.append(x,val[1])
    plt.plot(x,y,"o")
    m, b, r2=st.linregress(x,y)[:3]
    best=lambda x:m*x+b
    if max(x)<max(y):
        plt.plot(y,best(y),label=r"$y=$"+str(m)+r"$x+$"+str(b)+","+r"  $R^2 =$"+str(r2))
    else:
        plt.plot(x,best(x),label=r"$y=$"+str(m)+r"$x+$"+str(b)+","+r"  $R^2 =$"+str(r2))
    plt.title(Title)
    plt.legend(loc=4,fontsize=15)
    plt.ylabel(ncluster[pairs[0]][1,1])
    plt.xlabel(ncluster[pairs[1]][1,1])
    plt.xticks(np.linspace(np.floor(min(x)),np.ceil(max(x)),10))
    plt.yticks(np.linspace(np.floor(min(y)),np.ceil(max(y)),10))
    plt.grid()
    plt.show()


    
loc_combine=list(np.append(ID,locs))
for x in loc_combine:
    if "MS" in x or "RB-" in x:
        loc_combine.remove(x)
loc_combine=np.array(sortit(loc_combine))

Iso=np.array(["Thorium-232","Radium-228","Thorium-228","Lead-212","Bismuth-212","Thallium-208","Uranium-238","Thorium-234","Uranium-234","Thorium-230","Radium-226","Lead-214","Bismuth-214","Lead-210","Uranium-235","U235_236","Thorium-227","Potassium-40"])            

def data_combine(name=None):
    A=np.array(["Locations","Method","Isotope","Lab ID","CONC","2S","MDC","Qualifier"])
    for i in loc_combine:
        if i in cluster[0][:,-1]:
            for j in cluster:
                if name in j[1] and i in j[:,-1]:
                    k=list(j[:,-1]).index(i)
                    a=np.append(i,j[k][[0,1,2,4,5,6,8]])
                    A=np.vstack([A,a])
                    break
        else:
            for j in ncluster:
                if name in j[1] and i in j[:,-1] :
                    k=list(j[:,-1]).index(i)
                    a=np.append(i,j[k][[0,1,2,3,4,5,7]])
                    A=np.vstack([A,a])
                    break
    return(A)


combined=list(np.zeros(len(Iso)))
for i in np.arange(len(combined)):
    combined[i]=np.array(data_combine(Iso[i]))
combined=np.array(combined)


def filt(x=None,back=None): #Array input, [] on single value , background filter 0 or 1
    A=list(np.zeros(len(x)))
    if back:
        for w in np.arange(len(x)):
            A[w]= np.array([y for y in x[w][1:] if float(y[4]) > 4 and float(y[4]) > float(y[5]) and float(y[4]) > float(y[6]) and y[-1] is not "R"])         
        return(np.array(A))
    else:
        for w in np.arange(len(x)):
            A[w]= np.array([y for y in x[w][1:] if float(y[4]) > float(y[5]) and float(y[4]) > float(y[6]) and y[-1] is not "R"])         
        return(np.array(A))
    
def combined_plot(A=None): #  A is an array of arries of data by isotopes
    l = np.arange(len(loc_combine))
    plt.figure(figsize=(20,10))
    a=[]
    Title = "Plot of " 
    for i in A:
        if len(i)>0:
            error=[]
            x = []
            y = []
            for j in l:
                if loc_combine[j] in i[:,0]:
                    val=float(i[list(i[:,0]).index(loc_combine[j]),4])
                    val2=float(i[list(i[:,0]).index(loc_combine[j]),5])
                    error=np.append(error,val2)
                    y=np.append(y,val)
                    x=np.append(x,j)
            plt.plot(x,y,"o",linestyle="None",label=i[0,2])
            plt.errorbar(x, y, yerr=error,capsize=5,linestyle="None",barsabove=True,elinewidth=.5,ecolor='black')
            plt.xticks(l,loc_combine,rotation=90)
            Title += i[0,2] + ", "
            a=np.ndarray.flatten(np.append(np.append(a,y-error),y+error))
    plt.legend(loc=1,fontsize=10)
    plt.title(Title)
    plt.ylabel('Specific Activity, $pCi/g$')
    plt.xlabel('Locations')
    if len(a)>0:
        plt.yticks(np.linspace(np.floor(min(a)), np.ceil(max(a)), 20))
    plt.grid()
    plt.show()   
    
def combined_compare(pairs=None):  # pairs is a 1x2 array set of data, (parent/daughter)
    x = []
    plt.figure(figsize=(15,10))
    Title= pairs[0][0,2] + " vs. " + pairs[1][0,2]
    y = []
    for j in loc_combine:
        if j in pairs[0][:,0] and j in pairs[1][:,0] :
            val=[float(pairs[k][list(pairs[k][:,0]).index(j),4]) for k in [0,1]]
            y=np.append(y,val[0])
            x=np.append(x,val[1])
    plt.plot(x,y,"o")
    m, b, r2=st.linregress(x,y)[:3]
    best=lambda x:m*x+b
    if max(x)<max(y):
        plt.plot(y,best(y),label=r"$y=$"+str(m)+r"$x+$"+str(b)+","+r"  $R^2 =$"+str(r2))
    else:
        plt.plot(x,best(x),label=r"$y=$"+str(m)+r"$x+$"+str(b)+","+r"  $R^2 =$"+str(r2))
    plt.title(Title)
    plt.legend(loc=4,fontsize=15)
    plt.ylabel(pairs[0][0,2])
    plt.xlabel(pairs[1][0,2])
    plt.xticks(np.linspace(np.floor(min(x)),np.ceil(max(x)),10))
    plt.yticks(np.linspace(np.floor(min(y)),np.ceil(max(y)),10))
    plt.grid()
    plt.show()

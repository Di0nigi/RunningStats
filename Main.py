import pytesseract
import cv2
import numpy as np
import os
import pandas as pd
import gdown
import matplotlib.pyplot as plt
from datetime import date



path1="D:\dionigi\Documents\Python scripts\RunningStats\RunningStats"
url="https://drive.google.com/drive/folders/1sziH7NzIL4B4Y2ythZQYkyupOe9X_Wj5?usp=share_link"
fileName='D:\dionigi\Documents\Python scripts\RunningStats\RunningStat.xlsx'
dataframe1 = pd.read_excel(fileName,dtype={ "Distance":str,"Time":str, "Min/KM":str, "Kcal":str,"Date":str})
new=False
print("Working")


def main():
    currentDate= date.today().strftime("%d.%m.%Y")
    if new:
        download()
    imgePath=getFile(path1)
    resized=resize(imgePath)
    Stats=extract(resized)
    formatted=format(Stats,currentDate)
    df=save(formatted)
    graphIt(df)
    flush("dataFlush")
    
    


    return #formatted

def download():
   flush("D:\dionigi\Documents\Python scripts\RunningStats\RunningStats")
   f= gdown.download_folder(url)
   return 

def getFile(path):
    l=os.listdir(path)
    f=l[-1]
    p= os.path.join(path,f)
    return p

def getVpath(path):
    l=[]
    p=list(path.split("\\"))
    l.append(p[-1])
    Vpath=""
    for x in range(len(p)-1):
        os.path.join(Vpath,p[x])
        #Vpath+=p[x]+"\\"
    l.append(Vpath)
    return l

def resize(path):
    flush="dataFlush"
    p=getVpath(path)
    name=p[0]
    Vpath=p[1]
    img= cv2.imread(path)
   # src_points=[[7, 807], [5, 1188], [908, 1180], [901, 814]]
    src_float = np.array([[11, 963], [6, 1389], [1072, 1383], [1061, 954]], dtype=np.float32)
    dst_points = np.array([[0,0], # top left
                    [0,500], # bottom right
                    [800,500], # bottom left
                    [800,0]], dtype=np.float32)
    H = cv2.getPerspectiveTransform(src_float, dst_points)
    output_img = cv2.warpPerspective(img, H, (800, 500))
    final=os.path.join(Vpath,flush,name)
    b=cv2.imwrite(final,img=output_img)
    #print(b)

    return final

def extract(path):
    r=pytesseract.image_to_string(path)
    acc=[",",":"]
    l=[]
    ret=[]
    s=""
    for x in r:
        if x.isalnum() or x in acc:
            s+=x
        else:
            if x=="\n" or x==" ":
                l.append(s)
                s=""
    l=list(filter(None,l))
        
    return l

def format(l,date):
    #l.insert(0,str(dataframe1.iloc.ndim))
    i=-1
    l.append(date)
    d={"Distance":"","Time":"", "Min/KM":"", "Kcal":"",	"Date":""}
    for it in d:
        i+=1
        d[it]=l[i]
    return d

def save(d):
    data=[]
    col=[x for x in d]
    for ind in dataframe1.index:
        l=[]
        for x in list(dataframe1.iloc[ind,:]):
            l.append(x)
        data.append(l)
    if new:
        data.append([d[x] for x in d])
        
    dataframe2= pd.DataFrame(data,columns=col)
    dataframe2.to_excel(fileName,index=False)
    #dataframe1=dataframe2
    return dataframe2

def getData(df,t):
    l=[]
    ret=[]
    for x in df[t]:
        l.append(x)
    print(l)
    for ch in l:
        if "," in ch:
            s=ch.replace(",",".")
            ret.append(s)
        else:
            ret.append(ch)
    return ret

def parseTime(s):
    st=f"{s[3]}{s[4]}.{s[6]}{s[7]}"
    return float(st)

def flush(path):
    for f in os.listdir(path):
        os.remove(os.path.join(path, f))

    return




def graphIt(df):
    #fig= plt.figure()
    Xaxis=getData(df,"Date")
    Y1axis=[float(x) for x in getData(df,"Distance")]
    Y2axis=[parseTime(x) for x in getData(df,"Time")]
    fig, (g1, g2) = plt.subplots(2)
    fig.suptitle('Running Stats')
    fig.set_figwidth(9)
    fig.set_figheight(7)
    g1.bar(Xaxis,Y1axis)
    g2.bar(Xaxis,Y2axis)
    plt.show()

    


    return


print(main())
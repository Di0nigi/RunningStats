import pytesseract
import cv2
import numpy as np
import os
import pandas as pd
import datetime
from google_drive_downloader import GoogleDriveDownloader as gdd

#gdd.DOWNLOAD_URL='https://drive.google.com/drive/folders/1sziH7NzIL4B4Y2ythZQYkyupOe9X_Wj5?usp=share_link'
#gdd.download_file_from_google_drive(file_id='1sziH7NzIL4B4Y2ythZQYkyupOe9X_Wj5',
                                    #dest_path='D:\dionigi\Documents\Python scripts\RunningStats\dataTest\_testdrive01',
                                    #unzip=False,overwrite=True)


path="D:\dionigi\Documents\Python scripts\RunningStats\dataTest\image1.jpeg"
fileName='RunningStats.xlsx'
dataframe = pd.read_excel(fileName)



def main():
    currentDate= "10.10.10"
    
    resized=resize(path)
    Stats=extract(resized)
    formatted=format(Stats,currentDate)
    getData()
    save(formatted)
    getData()
    
    


    return formatted



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
    src_float = np.array([[7, 807], [5, 1188], [908, 1180], [901, 814]], dtype=np.float32)
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
    i=-1
    l.append(date)
    d={"Distance":"","Time":"", "Min/KM":"",	"Kcal":"",	"Date":""}
    for it in d:
        i+=1
        d[it]=l[i]
    



    return d

def save(d):
    #l=["Distance","Time", "Min/KM",	"Kcal"	"Date"]
    #d= {key: st for st in s for key in l}
    #print(d)
    #dataframe.append(d,ignore_index=True)
    
    for key in d:
        dataframe[key].update(d[key])
        dataframe.to_excel(fileName)



    return

def getData():
    print(dataframe)
    #print(dataframe["Date"])
    return




print(main())
import pytesseract
import cv2
import numpy as np
import os

r=""
points=[[7, 807], [5, 1188], [908, 1180], [901, 814]]

path="D:\dionigi\Documents\Python scripts\RunningStats\dataTest\image1.jpeg"

#r= pytesseract.image_to_string(path)

#r=list(r)


def main():
    resized=resize(path)
    Stats=extract(resized)
    


    return Stats



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
    print(b)

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

def format(s):
    str=""

    return

def save(s):
    return

def getData():
    return




main()
import cv2
import os

targetimage="./normal/back.jpeg"

tileroot="./tile/"

cardcolor=[[104,158,188], #normal
           [73,85,152], #effect
           [143,54,98], #fusion
           [197,100,45], #sac
           [239,233,224], #sync
           [25,9,2], #exc
           [135,156,21], #magic
           [99,28,133], #trap
            ]

def readcards(cardtype):
    cardname=os.listdir(tileroot+"/"+cardtype)
    card=[]
    for i in cardname:
        if i == ".DS_Store":
            continue
        card.append(cv2.imread(tileroot+"/"+cardtype+"/"+i))
    return card

def nearcard(imgtemp):
    seqlambda=lambda a,b,c,d,e,f:(a-d)**2+(b-e)**2+(c-f)**2
    seqmin=10000000000
    retnum=0
    for x,y in enumerate(cardcolor):
        if seqlambda(imgtemp[0],imgtemp[1],imgtemp[2],y[0],y[1],y[2])<seqmin:
            seqmin=seqlambda(imgtemp[0],imgtemp[1],imgtemp[2],y[0],y[1],y[2])
            retnum=x
    return retnum

width=int(2)
heigth=int(3)

def nearspacecard(i,j,imgtemp):
    tempnum=[0 for i in range(8)]
    for a in range(i,i+heigth):
        for b in range(j,j+width):
            tempnum[nearcard(imgtemp[a][b])]+=1

    return tempnum.index(max(tempnum))

def maketemp(img):

    temp=[[0 for i in range(int(len(img[0])/width))] for j in range(int(len(img)/heigth))]
    #temp=[[0 for i in range(int(len(img[0])/heigth))] for j in range(int(len(img)/width))]

    for i in range(0,len(img)-heigth,heigth):
        print(i)
        for j in range(0,len(img[i])-width,width):
            temp[int(i/heigth)][int(j/width)]=nearspacecard(i,j,img)

    return temp

#カードの読み込み
def initreadcard():
    cardtable=[]
    cardtable.append(readcards("normal"))
    cardtable.append(readcards("effect"))
    cardtable.append(readcards("fusion"))
    cardtable.append(readcards("sac"))
    cardtable.append(readcards("sync"))
    cardtable.append(readcards("exc"))
    cardtable.append(readcards("magic"))
    cardtable.append(readcards("trap"))

    return cardtable

if __name__ == '__main__':

    img=cv2.imread(targetimage)
    cardtable=initreadcard()

    imgtemp=maketemp(img)

    vtemp=[]

    for i in range(len(imgtemp)):
        print(i)
        retimgtemp = cardtable[0][0]
        for j in range(len(imgtemp[i])):
            retimgtemp=cv2.hconcat([retimgtemp, cardtable[imgtemp[i][j]][0]])
        vtemp.append(retimgtemp)
    retimg=vtemp[0]
    for i in range(len(vtemp)):
        print(i)
        retimg=cv2.vconcat([retimg,vtemp[i]])


    retimg = cv2.resize(retimg, (int(retimg.shape[1] * 0.25), int(retimg.shape[0] * 0.25)))

    cv2.imwrite("./output/back.jpg",retimg)
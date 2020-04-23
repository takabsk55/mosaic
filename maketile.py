import numpy as np
import cv2
import os

# 画像の読み出し
root='./blackcard'
tileroot='./tile'
cardtype=os.listdir(root)
for i in cardtype:
    if i == ".DS_Store":
        continue
    cards=os.listdir(root+'/'+i)
    for j,k in enumerate(cards):
        if k==".DS_Store":
            continue
        img = cv2.imread(root+'/'+i+'/'+k)
        img2 = cv2.resize(img, dsize=(80, 116))
        cv2.imwrite(tileroot+'/'+i+'/'+str(j)+'.jpg',img2)

Z = img.reshape((-1,3))


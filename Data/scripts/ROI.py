from logging import root
import xml.etree.ElementTree as ET
import os
import cv2
from numpy import extract
dir_loc = "../"
loc = "../harappa.com/annotation/annotations.xml"
img_loc = "../harappa.com/"
tree = ET.parse(loc)
root = tree.getroot()
def create_dirs():
    global loc
    global dir_loc
    global tree
    global root

    s = root.find('meta')[0].find('labels')
    for child in s:
        dir = child[0].text
        path = os.path.join(dir_loc,dir )
        os.mkdir(path)
        print("Directory '% s' created" % path)

def check(box):
    att = box.attrib
    if 'xtl' in att and 'ytl' in att and 'xbr' in att and 'ybr' in att:
        return True,[box.get('xtl'),box.get('ytl'),box.get('xbr'),box.get('ybr')]
    return False,None

"""Works for 2 and 4 points rectangle construction"""

def save_img(corr,label,name,img_name):
    print(corr,label,name)
    img = cv2.imread(os.path.join(img_loc,img_name))
    name = label+"/"+name
    name = os.path.join(dir_loc,name)
    if img is not None:
        xtl = int(float(corr[0]))
        ytl = int(float(corr[1]))
        xbr = int(float(corr[2]))
        ybr = int(float(corr[3]))
        print(xtl,xbr)
        k = img[ytl:ybr,xtl:xbr]
        # k = img[int(float(corr[0])):int(float(corr[1])),int(float(corr[2])):int(float(corr[3]))]
        cv2.imwrite(name,k)
        print("image saved in "+name)

def extract_ROI():
    global root
    i = 0

    for child in root:
        if child.tag=="image":
            if len(child)>0 and 'label' in child[0].attrib:
                name = child.get('name')
                for box in child:
                            
                    label = box.get('label')
                    ret,corr = check(box)
                    if ret:
                        save_img(corr,label,str(i)+".jpg",name)
                        i+=1
                        
            

extract_ROI()





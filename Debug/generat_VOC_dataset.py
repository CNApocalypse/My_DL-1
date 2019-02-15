import cv2
import os,sys
import random
import numpy as np
import xml.etree.ElementTree as ET
import xml.dom.minidom as MD
char_folder_path = "KAIST/char/"
image_folder_path = "ImageNet/"
VOC_image_path = "myVOC2007/JPEGImages/"
xml_save_path = "myVOC2007/Annotations/"
txt_save_path = "myVOC2007/Main/"
Dictionary = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","3","4","5","6","9","word"]
roots = []
for root,dirs,files in os.walk(char_folder_path):
    roots.append(root)

def get_random_char():
    random_folder_map = random.randint(1,31)
    random_char_folder_path = roots[random_folder_map]
    chars = []
    for _,_,charname in os.walk(random_char_folder_path):
        chars=charname
    name = chars[random.randint(0,len(chars)-1)]
    img = cv2.imread(random_char_folder_path+"/"+name)
    return img,name[:1]

def get_background_image(i):
    images = []
    for _,_,image in os.walk(image_folder_path):
        images = image
    name = images[i]
    img = cv2.imread(image_folder_path+"/"+name)
    return img
 
def combine_2_image(image1,image2):
        comb = np.zeros((image1.shape[0],image1.shape[1]+image2.shape[1],3))
        for h in range (30):
            for w in range (image1.shape[1]+image2.shape[1]):
                if w<=image1.shape[1]-1:
                    comb[h,w] = image1[h,w]
                else: comb[h,w] = image2[h,w-image1.shape[1]]
        return comb
def combine_to_word(char_img_0,char_img_1,char_img_2=None,char_img_3=None,char_img_4=None): # max contain 5 chars & min is 2,need do better***
    #word_bbox0=[[0,0,1,1],[1,0,2,1],[2,0,3,1],[3,0,4,1],[4,0,5,1]]
    combination = combine_2_image(char_img_0,char_img_1)
    #count = 2
    if np.all(char_img_2 !=None):
        combination = combine_2_image(combination,char_img_2)
        #count = 3
    if np.all(char_img_3 !=None):
        combination = combine_2_image(combination,char_img_3)
        #count = 4
    if np.all(char_img_4 !=None):
        combination = combine_2_image(combination,char_img_4)
        #count = 5
    return combination#,word_bbox0[:count]

def write_to_image(image1,image2,site):
    for h in range(image2.shape[0]-1):
        for w in range(image2.shape[1]):
            image1[h+site[1],w+site[0]] = image2[h,w]
    return image1
def not_touch(box1,box2):
    cat = []
    for  i in range(len(box2)):
        if box1[0]<box2[i][0] and box1[2]<box2[i][0]:cat.append(1)
        elif box2[i][0]<box1[0] and box2[i][2]<box1[0]:cat.append(1)
        elif box1[1]<box2[i][1] and box1[3]<box2[i][1]:cat.append(1)
        elif box2[i][1]<box1[1] and box2[i][3]<box1[1]:cat.append(1)
        else:cat.append(-1)
    for c in range(len(cat)):
        if cat[c] == -1:
            return False
    return True

def get_random_box(im0,im1):
    start = [random.randint(0,im0.shape[1]-im1.shape[1]),random.randint(0,im0.shape[0]-im1.shape[0])]
    t_box = [start[0],start[1],start[0]+im1.shape[1],start[1]+im1.shape[0]]
    return t_box

def add_object(tree,objection):
    root_tree = tree
    object = ET.SubElement(root_tree,'object')
    name = ET.SubElement(object,'name')
    name.text = objection[0]
    bndbox = ET.SubElement(object,'bndbox')
    xmin = ET.SubElement(bndbox,"xmin")
    ymin = ET.SubElement(bndbox,"ymin")
    xmax = ET.SubElement(bndbox,"xmax")
    ymax = ET.SubElement(bndbox,"ymax")
    xmin.text = objection[1]
    ymin.text = objection[2]
    xmax.text = objection[3]
    ymax.text = objection[4]
    return root_tree
def write_xmls(path,filename_put,image_w,image_h,obj_list=[]):
    annotation = ET.Element('annotation')
    folder = ET.SubElement(annotation, 'folder')
    folder.text = "VOC2007"
    filename = ET.SubElement(annotation, 'filename')
    filename.text = str(filename_put).zfill(6)+".jpg"
    size = ET.SubElement(annotation,'size')
    image_width = ET.SubElement(size,"width")
    image_height = ET.SubElement(size,"height")
    image_deepth = ET.SubElement(size,"deepth")
    image_width.text = str(image_w)
    image_height.text = str(image_h)
    image_deepth.text = str(3)
    if obj_list !=[]:
        for objects in range(len(obj_list)):
            annotation = add_object(annotation,obj_list[objects])
    tree = MD.parseString(ET.tostring(annotation).decode())
    annotation = tree.toprettyxml()
    with open(path+str(filename_put).zfill(6)+".xml", "w", encoding='utf-8') as f:
        f.write(annotation)
    return 
def list_mul(list,num):
    list = (np.array(list)*num).tolist()
    return list
def word_method(image,i):
    word_num = random.randint(2,5)
    namelist = ["word"]
    object_list = []
    num = 30
    im1,name1 = get_random_char()
    namelist.append(name1)
    object_list.append([name1,"0","0",str(num),str(num)])
    im2,name2 = get_random_char()
    namelist.append(name2)
    object_list.append([name2,str(num),"0",str(2*num),str(num)])
    if word_num ==2:
        comb_word = combine_to_word(im1,im2)
        object_list.append(["word","0","0",str(2*num),str(num)])
    elif word_num ==3:
        im3,name3 = get_random_char()
        namelist.append(name3)
        object_list.append([name3,str(2*num),"0",str(3*num),str(num)])
        comb_word = combine_to_word(im1,im2,im3)
        object_list.append(["word","0","0",str(3*num),str(num)])
    elif word_num ==4:
        im3,name3 = get_random_char()
        namelist.append(name3)
        object_list.append([name3,str(2*num),"0",str(3*num),str(num)])
        im4,name4 = get_random_char()
        namelist.append(name4)
        object_list.append([name4,str(3*num),"0",str(4*num),str(num)])
        comb_word = combine_to_word(im1,im2,im3,im4)
        object_list.append(["word","0","0",str(4*num),str(num)])
    else:
        im3,name3 = get_random_char()
        im4,name4 = get_random_char()
        im5,name5 = get_random_char()
        namelist.append(name3)
        namelist.append(name4)
        namelist.append(name5)
        object_list.append([name3,str(2*num),"0",str(3*num),str(num)])
        object_list.append([name4,str(3*num),"0",str(4*num),str(num)])
        object_list.append([name5,str(4*num),"0",str(5*num),str(num)])
        comb_word = combine_to_word(im1,im2,im3,im4,im5)
        object_list.append(["word","0","0",str(5*num),str(num)])
    start = [random.randint(0,image.shape[1]-comb_word.shape[1]),random.randint(0,image.shape[0]-comb_word.shape[0])]
    image = write_to_image(image,comb_word,(start[0],start[1]))
    for lenth in range(len(object_list)):
        object_list[lenth][1] = str(int(object_list[lenth][1])+start[0])
        object_list[lenth][2] = str(int(object_list[lenth][2])+start[1])
        object_list[lenth][3] = str(int(object_list[lenth][3])+start[0])
        object_list[lenth][4] = str(int(object_list[lenth][4])+start[1])
    write_xmls(xml_save_path,i,image.shape[1],image.shape[0],object_list)
    cv2.imwrite(VOC_image_path+str(i).zfill(6)+".jpg",image)
    return namelist

def add_char_image_once(image,c_box,namelist,object_list):
    char_img,char_label = get_random_char()
    temp_box = get_random_box(image,char_img)
    while not_touch(temp_box,c_box) ==False:
        temp_box = get_random_box(image,char_img)
    namelist.append(char_label)
    image = write_to_image(image,char_img,(temp_box[0],temp_box[1]))
    t =[char_label]
    for xx in temp_box:
        t.append(str(xx))
    object_list.append(t)
    return image,namelist,object_list,temp_box

def char_method(image,i):
    namelist = []
    object_list = []
    char_num = random.randint(1,6)
    char_img0 , char_label0= get_random_char()
    namelist.append(char_label0)
    start = [random.randint(0,image.shape[1]-char_img0.shape[1]),random.randint(0,image.shape[0]-char_img0.shape[0])]
    c_box = [[start[0],start[1],start[0]+char_img0.shape[1],start[1]+char_img0.shape[0]]]
    image = write_to_image(image,char_img0,(start[0],start[1]))
    temp_list = [char_label0,str(c_box[0][0]),str(c_box[0][1]),str(c_box[0][2]),str(c_box[0][3])]
    object_list.append(temp_list)
    if char_num ==2:
        image,namelist,object_list,temp_box = add_char_image_once(image,c_box,namelist,object_list)
        c_box.append(temp_box)
    elif char_num ==3:
        for _ in range(2):
            image,namelist,object_list,temp_box = add_char_image_once(image,c_box,namelist,object_list)
            c_box.append(temp_box)
    elif char_num ==4:
        for _ in range(3):
            image,namelist,object_list,temp_box = add_char_image_once(image,c_box,namelist,object_list)
            c_box.append(temp_box)
    elif char_num ==5:
        for _ in range(4):
            image,namelist,object_list,temp_box = add_char_image_once(image,c_box,namelist,object_list)
            c_box.append(temp_box)
    else:
        for _ in range(5):
            image,namelist,object_list,temp_box = add_char_image_once(image,c_box,namelist,object_list)
            c_box.append(temp_box)

    write_xmls(xml_save_path,i,image.shape[1],image.shape[0],object_list)
    cv2.imwrite(VOC_image_path+str(i).zfill(6)+".jpg",image)
    return namelist

def main():
    dict = {c:"" for c in Dictionary}
    for i in range(5353):
        image = get_background_image(i)
        p = random.randint(1,10)
        if p>=7:
            namelist = word_method(image,i)
        else:
            namelist = char_method(image,i)
        dict = write_txt(i,namelist,dict)
    for di in Dictionary:
        with open(txt_save_path+di+"_all.txt", 'w') as f: 
            f.write(dict[di])
    print("Done!")

def write_txt(i,namelist,dict):
    num = str(i).zfill(6)
    for di in Dictionary:
        text = "-1"
        for la in namelist:
            while la==di:
                text = " 1"
                break
                
        dict[di]=dict[di]+num+" "+text+"\n"
    return dict
    




if __name__ == "__main__":
    main()

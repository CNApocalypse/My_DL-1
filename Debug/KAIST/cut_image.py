import cv2
import numpy as np
import xml.etree.ElementTree as ET 
import sys,os

def all_file_pathf(folderpath):
  for  _,_,files in os.walk(folderpath):  
    jpegs = []
    xmls = []
    i = 1
    for filename in files:
      if i%2==0:
        xmls.append(filename)
      else:
        jpegs.append(filename)
      i+=1
  return xmls,jpegs

def read_xmls(xml_path):
  print(xml_path)
  try:
    tree = ET.parse(xml_path)
  except ET.ParseError:
    tree = None
  if tree ==None:
    return "error"
  else:
    root = tree.getroot()
    charlist = []
    charboxlist = []
    for character in root.iter('character'):
      charlist.append(character.attrib.get("char"))
      charboxlist.append(character.attrib.get("x"))
      charboxlist.append(character.attrib.get("y"))
      charboxlist.append(character.attrib.get("width"))
      charboxlist.append(character.attrib.get("height"))
    charboxarray = np.zeros(shape = (int(len(charboxlist)/4),4))
    for i in range(int(len(charboxlist)/4)):
      charboxarray[i,0] = charboxlist[i*4]
      charboxarray[i,1] = charboxlist[i*4+1]
      charboxarray[i,2] = charboxlist[i*4+2]
      charboxarray[i,3] = charboxlist[i*4+3]
    return charlist,charboxarray

def cut_image(fn,imgname,charlist,charbox):
  img = cv2.imread(imgname)
  for i in range(len(charlist)):
    tempchar = np.zeros(shape = (int(charbox[i,3]),int(charbox[i,2]),3))
    for h in range(tempchar.shape[0]):
      for w in range(tempchar.shape[1]):
        tempchar[h,w] = img[h+int(charbox[i,1]),w+int(charbox[i,0])]
    write_char_images(tempchar,"new/"+charlist[i]+str(fn)+str(i))

def write_char_images(mat,name):
  cv2.imwrite(name+".jpg",mat)

def main():

  path = "imaxml/"
  xmls,jpegs = all_file_pathf(path)
  for fn in range(len(xmls)):
    try:
      b,c = read_xmls(path+xmls[fn])
    except ValueError:
      continue
    a=path+jpegs[fn]
    cut_image(fn,a,b,c)
  print("Done!")

if __name__ == '__main__':

  main()
import cv2
import os,sys
Dictionary = {"A":0,"B":0,"C":0,"D":0,"E":0,"F":0,"G":0,"H":0,"I":0,"J":0,"K":0,"L":0,"M":0,"N":0,"O":0,"P":0,"Q":0,"R":0,"S":0,
              "T":0,"U":0,"V":0,"W":0,"X":0,"Y":0,"Z":0,"3":0,"4":0,"5":0,"6":0,"9":0}
def resize_image(size,image):
  return cv2.resize(image, (size, size), interpolation=cv2.INTER_LANCZOS4)

def rename_image(filename):
  if Dictionary.get(filename[:1]) != None:
    dic_count = Dictionary.get(filename[:1])
    name = filename[:1] + str(dic_count)+".jpg"
    Dictionary[filename[:1]] = dic_count+1
    return name

def main():

  oldpath = "new/"
  newpath = "char/"
  full_image_list = []
  for  _,_,files in os.walk(oldpath):
    full_image_list = files
  for filename in full_image_list:
    newname = rename_image(filename)
    if newname != None:
      tmp_img = cv2.imread(oldpath+filename)
      tmp_img = resize_image(30,tmp_img)
      cv2.imwrite(newpath+newname,tmp_img)

   
      
  print(Dictionary)
  


if __name__ == '__main__':

  main()
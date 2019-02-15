import cv2
import os,sys
old_path = "ILSVRC2012_img_val/"
new_path = "ImageNet/"
def main():
    full_image_list = []
    for  _,_,files in os.walk(old_path):
        full_image_list = files
    for i in range(6000):
        img = cv2.imread(old_path+full_image_list[i])
        #img = cv2.resize(img, (448, 448), interpolation=cv2.INTER_LANCZOS4)
        cv2.imwrite(new_path+str(i)+".jpg",img)

if __name__ =="__main__":
    main()

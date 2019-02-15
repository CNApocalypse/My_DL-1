import os,sys
spreat_floder = "myVOC2007/Main/"
Dictionary = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","3","4","5","6","9","word"]
file_list = []
for _,_,files in os.walk(spreat_floder):
    file_list.append(files)
def spreat_text(filename):
    val_line = []
    train_line = []
    for line in open(spreat_floder+filename):  
        if int(line[:6])%2 ==0:
            val_line.append(line)
        else:
            train_line.append(line)
    return val_line,train_line

def write_txt(filename,linespace):
    with open(spreat_floder + filename,"w") as f:
        f.write(''.join(linespace))
    return

def main():
    for name in Dictionary:
        filename = name + "_all.txt"
        val_line,train_line = spreat_text(filename)
        write_txt(name+"_val.txt",val_line)
        write_txt(name+"_train.txt",train_line)
    print("Done!!")

if __name__  == "__main__":
    main()




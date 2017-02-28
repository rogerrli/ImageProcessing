import os

fo = open("bg.txt", "a")
for i in range(2,6003):
    if i < 10:
        zeros = "000"
    elif i < 100:
        zeros = "00"
    elif i < 1000:
        zeros = "0"
    else:
        zeros = ""
    fo.write("non_images/animal" + zeros + str(i) + ".jpg\n")
fo.close()

import os
import Image
def thumb(one):
	i=Image.open("item0/"+one)
	print i.size
	i=i.resize((i.size[0]/10,i.size[1]/10))
	i.save("item/"+one)
fs=os.listdir("item0")
for f in fs:
	thumb(f)

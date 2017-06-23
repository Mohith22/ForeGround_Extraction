import cv2
import operator
from PIL import Image
import numpy as np
import os
import json
import time
import ast
from matplotlib import pyplot as plt
from matplotlib import pyplot as plt
from pyexcel_ods import get_data


# -----------------------------  Inputs -----------------------------------

#Input - Input Folder Path
product = raw_input("Enter Input Image Path: ")


#Input - Excel File Path (For Re-Naming)
excel_file = raw_input("Enter Excel File Path: ")

#Input - Bounding Box Dynamics Variations
print "Try values of bounding errors, e1,e2,e3,e4 - in range [-5,+5] untill you get desired output"
print "Enter sign followed by integer value"
print "If zero enter +0"
e1 = raw_input("E1: ")
e2 = raw_input("E2: ")
e3 = raw_input("E3: ")
e4 = raw_input("E4: ")

#---------------------------------------------------------------------------

ops = { "+": operator.add, "-": operator.sub }

# ---------------------Step1 - Store Excel File Into Dictionary ------------

data = get_data(excel_file)
dict_data = ast.literal_eval(json.dumps(data))
dict_data = dict(dict_data['Sheet1'])

# --------------------------------------------------------------------------



#Start Time (For Execution Time Calculation)
start_time = time.time()


img = cv2.imread(product,0)
print img.shape
fin_pro = product.split(".")[0]
fin_pro = product
path2 =  str(dict_data[fin_pro])+".png"


# ---Finding extreme points (To find bounding rectangel) ----
c=0
cmax=99999

for i in range(img.shape[0]):
	for j in range(img.shape[1]):
		if img[i,j]!=255:
			if c<cmax:
				xl=j
				yl=i
				cmax=c
			c=0
			break
		else:
			c=c+1

c=0
cmax=99999

for i in range(img.shape[0]):
	for j in range(img.shape[1]-1,-1,-1):
		if img[i,j]!=255:
			if c<cmax:
				xr=j
				yr=i
				cmax=c
			c=0
			break
		else:
			c=c+1

c=0
cmax=99999


for i in range(img.shape[1]):
	for j in range(img.shape[0]):
		if img[j,i]!=255:
			if c<cmax:
				xt=i
				yt=j
				cmax=c
			c=0
			break
		else:
			c=c+1


c=0
cmax=99999

for i in range(img.shape[1]):
	for j in range(img.shape[0]-1,-1,-1):
		if img[j,i]!=255:
			if c<cmax:
				xb=i
				yb=j
				cmax=c
			c=0
			break
		else:
			c=c+1

# -------------------------------------------------------

mask = np.zeros(img.shape[:2],np.uint8)

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

img = cv2.imread(product)

#r = 350.0 / img.shape[1]
#dim = (350, int(img.shape[0] * r))
#img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

# ---------------Step 3 - Path Tracing -------------------

#Bounding rectangle - Input to GrabCut Algorithm

#Please make changes here for better foreground extraction
#Change can range from -5 to +5
#Test various permutations from -5 to +5 until you get the expected output
rect = (ops[e1[0]](xl,int(e1[1])),ops[e2[0]](yt,int(e2[1])),ops[e3[0]](xr,int(e3[1])),ops[e4[0]](yb,int(e4[1])))

#Grab Cut Algorithm with 10 iterations
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,10,cv2.GC_INIT_WITH_RECT)

mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]
cv2.imwrite('black.png',img)

imgc = Image.open('black.png')
imgc = imgc.convert("RGBA")
datas = imgc.getdata()
newData = []
for item in datas:
	if (item[0] ==0) and (item[1] ==0) and (item[2] ==0):
		newData.append((255, 255, 255,0))
	else:
		newData.append(item)

imgc.putdata(newData)
imgc.save(path2,"PNG")

#Print Execution Time
print "Execution Time is :"
print time.time() - start_time	

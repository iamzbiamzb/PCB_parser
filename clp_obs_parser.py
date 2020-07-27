#clp parser
import string
import os
import sys
import re

clp_name = sys.argv[1]
output_name = sys.argv[2]
TargetLayer = sys.argv[3]

file = open(clp_name, 'r')
pin = "_clpInitPinText"
pinName = ""
nameBuf=""
nameArr=""
locArr=""
typeBuf=""
locBuf=""
sameChip=""
anoSameChip=""
pinX = ""
pinY = ""
buf=""
usefulChip=""
chipDict={}
chipAllPinDict={}
ID_TypeDict={}
line = file.readline()
count = 0

chipLayerDict = {}

# Parse Pin info
while line:
	if line.find('_clpDBCreateText')!=-1:
		chip_name=line.split('"')[1]
		line = file.readline()
		line = file.readline()
		if line.find('TOP')!=-1:
			chipLayerDict[chip_name] = "TOP"
		elif line.find('BOTTOM')!=-1:
			chipLayerDict[chip_name] = "BOTTOM"
		else:
			chipLayerDict[chip_name] = "Undefined"

	if line.find('_clpInitPinText')!=-1:
		nameBuf=line.split('"')[1]
	elif line.find('_clpDBCreatePin(')!=-1:
		typeBuf=line.split('"')[1]
		locBuf=line.split('"')[2].lstrip(' _clpAdjustPt(')
		pinX=locBuf.split(':')[0]
		pinY=locBuf.split(':')[1].split()[0]
		nameArr=nameArr+nameBuf+' '
		locArr=locArr+pinX+','+pinY+' '
		sameChip=sameChip+nameBuf+' '+typeBuf+' '+pinX+' '+pinY+'\n'
	elif line.find(' "PACKAGE" "')!=-1:
		if typeBuf=='KM0P25C' or typeBuf=='KM0P4C' or typeBuf=='KM0P325C' or typeBuf=='KM0P22C_SM0P25C' or typeBuf=='PAD28' or typeBuf=='SMD_16CIR' or typeBuf=='SMD_R19':
			usefulChip=usefulChip+' '+line.split('"')[5]
		ID_TypeDict[line.split('"')[5]]=typeBuf
		anoSameChip=""
		for i in sameChip.split('\n'):
			if i == '':
				break
			anoSameChip=anoSameChip+line.split('"')[5]+' '+i+'\n'
		chipAllPinDict[line.split('"')[5]]=anoSameChip
		sameChip=""
		count=0
		for i in nameArr.split(' '):
			if i!='':
				chipDict[line.split('"')[5]+'.'+i]=locArr.split()[count]
			count=count+1
		nameArr=""
		locArr=""
	line = file.readline()
file.close()

obs_file = open(output_name, 'w')

for i,j in chipDict.items():

	chip_name = i.split('.')[0]

	layer = chipLayerDict[chip_name]
	
	if layer == TargetLayer:
		chip_type = ID_TypeDict[chip_name]
		width = 0
		height = 0
		last_char = chip_type[-1]

		if last_char == 'C':
			#circle
			if chip_type.find('0P')!=-1:
				matchObj = re.match(r'(.*)0P([0-9]*)C', chip_type)
				width = float("0." + str(matchObj.group(2)))
				height= float("0." + str(matchObj.group(2)))
			else:
				matchObj = re.match(r'([a-zA-Z]*)([0-9]*)C', chip_type)
				width = float(str(matchObj.group(2)))
				height= float(str(matchObj.group(2)))

		elif last_char == 'S':
			#square
			if chip_type.find('0P')!=-1:
				matchObj = re.match(r'(.*)0P([0-9]*)S', chip_type)
				#print('a' + matchObj.group(2))
				width = float("0." + str(matchObj.group(2)))
				height= float("0." + str(matchObj.group(2)))
			else:
				matchObj = re.match(r'([a-zA-Z]*)([0-9]*)S', chip_type)
				#print('b' + matchObj.group(2))
				width = float(str(matchObj.group(2)))
				height= float(str(matchObj.group(2)))
		elif chip_type.find('X')!=-1 :
			#rectangle
			matchObj = re.match(r'([a-zA-Z]+)([0-9]+P[0-9]+|[0-9]+)X([0-9]+P[0-9]+|[0-9]+)', chip_type)
			print(chip_type)
			print(matchObj.group(2))
			print(matchObj.group(3))
			#str(matchObj.group(2)).replace('P','.')
			#str(matchObj.group(3)).replace('P','.')
			if chip_type.find('P')!=-1:
				width = float(str(matchObj.group(2)).replace('P','.'))
				height= float(str(matchObj.group(3)).replace('P','.'))
			else:
				width = float(str(matchObj.group(2)))
				height= float(str(matchObj.group(3)))

		print("PinPad : " + i)
		print("\t Coor : " + j)
		print("\t Type : " + chip_type)
		print("\t\t Width : " + str(width))
		print("\t\t Height : " + str(height))
		
		left_x = float(j.split(",")[0]) - (width/2)
		right_x = float(j.split(",")[0]) + (width/2)
		lower_y = float(j.split(",")[1]) - (width/2)
		upper_y = float(j.split(",")[1]) + (width/2)
		rect_str = "LB(" + str(left_x) + "," + str(lower_y) + ") RT(" + str(right_x) + "," + str(upper_y) + ")"
		print("\t Rect : " + rect_str)

		output_obs = str(int(left_x*100)) + " " + str(int(lower_y*100)) + " " + str(int(right_x*100)) + " " + str(int(upper_y*100)) + " 0\n"

		obs_file.write(output_obs)

obs_file.close()



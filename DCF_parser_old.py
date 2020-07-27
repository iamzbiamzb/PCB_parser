#dcf parser
import string
import os
import sys
import re


def Normalize (number):
	EPS = 1e-9
	return float(number) / 1000.0 + EPS;

def output_gds(chipDict, ID_TypeDict, UsedPinDict, chipLayerDict, output_name):
	# file = open("temp.gdt", 'wb')
	# timeseq = "1995-04-17 18:00:00"
	# file.write("gds2{600\n")
	# file.write("m="+timeseq+" a="+timeseq+"\n");
	# file.write("lib 'lib' 0.00025 2.5e-10\n");
	# file.write("cell{c="+ timeseq +" m=" + timeseq + "'gdt'" + "\n")

	for i,j in chipDict.items():

		chip_name = i.split('.')[0]

		layer = chipLayerDict[chip_name]
		gds_layer = -1
		if(layer == "TOP"):
			gds_layer = 0
		if(layer == "BOTTOM"):
			gds_layer = 1
		

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
		elif chip_type.find('X')!=-1:
			#rectangle
			matchObj = re.match(r'([a-zA-Z]+)([0-9]P[0-9]+|[0-9]+)X([0-9]P[0-9]+|[0-9]+)', chip_type)
			#print(chip_type)
			#str(matchObj.group(2)).replace('P','.')
			#str(matchObj.group(3)).replace('P','.')
			width = float(str(matchObj.group(2)).replace('P','.'))
			height= float(str(matchObj.group(3)).replace('P','.'))
		

		if UsedPinDict.get(i, 'noExist') != 'noExist':
			print("PinPad : " + i)
			print("\t Coor : " + j)
			print("\t Type : " + chip_type)
			print("\t\t Width : " + str(width))
			print("\t\t Height : " + str(height))
			left_x = float(j.split(",")[0]) - (width/2)
			right_x = float(j.split(",")[0]) + (width/2)
			lower_y = float(j.split(",")[1]) - (width/2)
			upper_y = float(j.split(",")[1]) + (width/2)
			# file.write("b{%d dt%d xy(%.3lf %.3lf %.3lf %.3lf %.3lf %.3lf %.3lf %.3lf)}\n" % (gds_layer, 0, Normalize(left_x),
			#			Normalize(lower_y), Normalize(right_x), Normalize(lower_y), Normalize(right_x), Normalize(upper_y), Normalize(left_x), Normalize(upper_y)))
		else:
			print("ObsPad : " + i)
			print("\t Coor : " + j)
			print("\t Type : " + chip_type)
			print("\t\t Width : " + str(width))
			print("\t\t Height : " + str(height))
			left_x = float(j.split(",")[0]) - (width/2)
			right_x = float(j.split(",")[0]) + (width/2)
			lower_y = float(j.split(",")[1]) - (width/2)
			upper_y = float(j.split(",")[1]) + (width/2)
			# file.write("b{%d dt%d xy(%.3lf %.3lf %.3lf %.3lf %.3lf %.3lf %.3lf %.3lf)}\n" % (gds_layer, 100, Normalize(left_x),
			#			Normalize(lower_y), Normalize(right_x), Normalize(lower_y), Normalize(right_x), Normalize(upper_y), Normalize(left_x), Normalize(upper_y)))

	# file.write("}\n}\n");
	# file.close()
	# os.system("./gdt2gds temp.gdt "+output_name+".gds")

#python InputParser.py [.clp] [net] [.dcf] [out]

clp_name = sys.argv[1]
dcf_name = sys.argv[3]
netlist_name = sys.argv[2]
#output_name = sys.argv[4]

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

# Parse Net info
file = open(netlist_name,'r')
netF=0
netChangeLine=0
pinCount=0
buf=""
netData=""
netMem=""
netName=""
netDict={}
pinToNetDict={}
line=file.readline()
while line:
	if netF==0 and line.find('$NET')!=-1:
		netF=1
	elif netF==1 and line.find('DDR')!=-1:
		pinCount=0
		netData=""
		netMem=""
		netName=line.split(' ;')[0]
		buf=""
		#buf=line.split(';')[1].replace(',','')
		if line.find(',')==-1:
			buf=line.split(';')[1]
		while line.find(',')!=-1:
			netChangeLine=1
			if line.find(',')!=-1 and line.find(';')!=-1:
				buf=line.split(';')[1].replace(',', '').replace('\n','')
			else:
				buf =buf+' '+line.replace(',', '').replace('\n','').replace('	','')
			line=file.readline()
		if netChangeLine==1:
			netChangeLine=0
			buf=buf+' '+line.replace(',','').replace('\n','').replace('	   ','')
		for i in buf.split():
			netData = netData + (i + ' ')
			pinCount= pinCount + 1
		if pinCount>=2:
			netDict[netName]=netData
	elif netF==1 and line.find('EBI')!=-1:
		pinCount = 0
		netData=""
		netMem = ""
		netName = line.split(' ;')[0]
		# buf=line.split(';')[1].replace(',','')
		if line.find(',')==-1:
			buf=line.split(';')[1]
		while line.find(',') != -1:
			netChangeLine = 1
			if line.find(',') != -1 and line.find(';') != -1:
				buf = line.split(';')[1].replace(',', '').replace('\n', '')
			else:
				buf = buf + ' ' + line.replace(',', '').replace('\n', '').replace('	  ', '')
			line = file.readline()
		if netChangeLine == 1:
			netChangeLine = 0
			buf = buf + ' ' + line.replace(',', '').replace('\n', '').replace('	   ', '')
		for i in buf.split():
			netData = netData + i + ' '
			pinCount = pinCount + 1
		if pinCount >= 2:
			netDict[netName] = netData
	elif netF==1 and line.find('DRAM')!=-1:
		pinCount = 0
		netData=""
		netMem = ""
		netName = line.split(' ;')[0]
		# buf=line.split(';')[1].replace(',','')
		if line.find(',')==-1:
			buf=line.split(';')[1]
		while line.find(',') != -1:
			netChangeLine = 1
			if line.find(',') != -1 and line.find(';') != -1:
				buf = line.split(';')[1].replace(',', '').replace('\n', '')
			else:
				buf = buf + ' ' + line.replace(',', '').replace('\n', '').replace('	  ', '')
			line = file.readline()
		if netChangeLine == 1:
			netChangeLine = 0
			buf = buf + ' ' + line.replace(',', '').replace('\n', '').replace('	   ', '')
		for i in buf.split():
			pinCount = pinCount + 1
		if pinCount >= 2:
			netData = netData + i + ' '
			netDict[netName] = netData
	elif netF==1 and line.find('$')!=-1:
		netF=0
	line=file.readline()
file.close()

#Signal Pin pair info
pinPairDict = {}
Final_Net_Dict = {}
file=open(dcf_name,'r')
line=file.readline()
while line:
	if line.find('( signal "')!=-1:
		signal_name = line.split('"')[1]
		count = 0;
		net_data = ""
		while(True):
			if line.find('( pinPairRef "')!=-1:
				pairBuf0=line.split('"')[1].split(':')[0]
				pairBuf1=line.split('"')[1].split(':')[1]
				net_data = net_data + str(pairBuf0) + ' ' + str(pairBuf1) + "\n"
				key = str(pairBuf0) + ':' + str(pairBuf1)
				pinPairDict[key] = signal_name
				count = count + 1
			if line.find('( objectStatus "')!=-1:
				break
			line=file.readline()
		if count > 0:
			Final_Net_Dict[signal_name] = net_data
		if count == 0 and netDict.get(signal_name, 'noExist') != 'noExist':
			#print(signal_name + "\n\t" + netDict[signal_name])
			Final_Net_Dict[signal_name] = netDict[signal_name]

	line=file.readline()
file.close()

#Net class
file=open(dcf_name,'r')
line=file.readline()

netClassDict = {}
physical_Dict = {}
spacing_Dict = {}
while line:
	if line.find('netClass "')!=-1:	  
		net_class_name = line.split('"')[1]
		
		pSetRef = "DEFAULT"
		sSetRef = "DEFAULT"

		while line.find('member (') == -1:
			if line.find('physicalCSetRef "') != -1:
				pSetRef = line.split('"')[1]
			if line.find('spacingCSetRef "') != -1:
				sSetRef = line.split('"')[1]
			line=file.readline()
		
		net_member = []
		while True :
			#print(line)
			net_name = line.split('"')[1]
			net_member.append(net_name)
			line=file.readline()
			if(line.find('member (') == -1):
				break
		physical_Dict[net_class_name] = pSetRef
		spacing_Dict[net_class_name] = sSetRef
		for i in range(0,len(net_member)):
			netClassDict[net_member[i]] = net_class_name
	line=file.readline()
file.close()

#Match Group
UsedPinDict = {}
file=open(dcf_name,'r')
line=file.readline()
while line:
	if line.find('( matchGroup "')!=-1:
		group_name = line.split('"')[1]
		print(group_name)
		member_check = 0
		while(True):
			if line.find('"RELATIVE_PROPAGATION_DELAY"')!=-1:
				Tolerence = line.split('"')[3]
				#print("\tTolerence: " + str(Tolerence))
			if line.find('( member ( pinPairRef "')!=-1:
				pairBuf0=line.split('"')[1].split(':')[0]
				pairBuf1=line.split('"')[1].split(':')[1]
				UsedPinDict[pairBuf0] = 1
				UsedPinDict[pairBuf1] = 1
				print("\tpinPairRef:" + str(pairBuf0) + ' ' + str(pairBuf1))
				key = str(pairBuf0) + ':' + str(pairBuf1)
				if pinPairDict.get(key, 'noExist') != 'noExist':
					print("\t\tReference Net:" + pinPairDict[key])
					if netClassDict.get(pinPairDict[key], 'noExist') != 'noExist':
						net_name = pinPairDict[key]
						print("\t\tNet Class:" + netClassDict[net_name])
						net_class_name = netClassDict[net_name]
						print("\t\t\tphysicalCSetRef:" + physical_Dict[net_class_name])
						print("\t\t\tspacingCSetRef:" + spacing_Dict[net_class_name])
					else : 
						print("\t\tNet Class:DEFAULT")
						net_class_name = netClassDict[net_name]
						print("\t\t\tphysicalCSetRef:DEFAULT")
						print("\t\t\tspacingCSetRef:DEFAULT")

				member_check = 1
			if line.find('( member ( signalRef "')!=-1:
				Net_Name = line.split('"')[1]
				print("\tsignalRef:" + str(Net_Name))
				if Final_Net_Dict.get(Net_Name, 'noExist') != 'noExist':
					print("\t\tReference Pin-Pair:" + Final_Net_Dict[Net_Name].rstrip())
					pin_pair_list = Final_Net_Dict[Net_Name].rstrip().split(' ')
					for pin_pair in pin_pair_list:
						UsedPinDict[pin_pair.rstrip()] = 1
					if netClassDict.get(Net_Name, 'noExist') != 'noExist':
						net_name = Net_Name
						print("\t\tNet Class:" + netClassDict[net_name])
						net_class_name = netClassDict[net_name]
						print("\t\t\tphysicalCSetRef:" + physical_Dict[net_class_name])
						print("\t\t\tspacingCSetRef:" + spacing_Dict[net_class_name])
					else : 
						print("\t\tNet Class:DEFAULT")
						net_class_name = netClassDict[net_name]
						print("\t\t\tphysicalCSetRef:DEFAULT")
						print("\t\t\tspacingCSetRef:DEFAULT")
				member_check = 1
			if member_check == 1 and line.find("member")==-1:
				break
			line=file.readline()
	line=file.readline()
file.close()

#output_gds(chipDict, ID_TypeDict, UsedPinDict, chipLayerDict, output_name)

for i,j in chipDict.items():

	chip_name = i.split('.')[0]

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
	

	if UsedPinDict.get(i, 'noExist') != 'noExist':
		print("PinPad : " + i)
		print("\t Coor : " + j)
		print("\t Type : " + chip_type)
		print("\t\t Width : " + str(width))
		print("\t\t Height : " + str(height))
	else:
		print("ObsPad : " + i)
		print("\t Coor : " + j)
		print("\t Type : " + chip_type)
		print("\t\t Width : " + str(width))
		print("\t\t Height : " + str(height))

	#print(i,j,chip_type,width,height)



# dcf parser
# command
# python3 DCF_parser.py [clp_name].clp [txt_name].txt [dcf_name].dcf [output_name]
import string
import os
import sys
import re


def Normalize (number):
	EPS = 1e-9
	return float(number) / 1000.0 + EPS;

def output_gds(chipDict, ID_TypeDict, UsedPinDict, chipLayerDict, output_name, layerDict):
	
	# timeseq = "1995-04-17 18:00:00"
	# file.write("gds2{600\n")
	# file.write("m="+timeseq+" a="+timeseq+"\n");
	# file.write("lib 'lib' 0.00025 2.5e-10\n");
	# file.write("cell{c="+ timeseq +" m=" + timeseq + "'gdt'" + "\n")
	# print("chipDict")
	# for i,j in chipDict.items():
	# 	print(i+" "+j)
	# print("ID_TypeDict")
	# for i,j in ID_TypeDict.items():
	# 	print(i+" "+j)
	# print("UsedPinDict")
	# print(UsedPinDict)
	# print("chipLayerDict")
	# for i,j in chipLayerDict.items():
	# 	print(i+" "+j)
	obs_file = open(output_name+'.obs','w')
	for i,j in chipDict.items():

		chip_name = i.split('.')[0]

		if chip_name in chipLayerDict:
			layer = chipLayerDict[chip_name]
		# gds_layer = -1
		# if(layer == "TOP"):
		# 	gds_layer = 0
		# if(layer == "BOTTOM"):
		# 	gds_layer = 1
		

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

			
			#os.system("pause")
			#square
			if chip_type.find('0P')!=-1:
				matchObj = re.match(r'(.*)0P([0-9]*)S', chip_type)
				#print('a' + matchObj.group(2))
				width = float("0." + str(matchObj.group(2)))
				height= float("0." + str(matchObj.group(2)))
			elif chip_type.find('P')!=-1:
				matchObj = re.match(r'([a-zA-Z]+)([0-9]+P[0-9]+|[0-9]+)S', chip_type)
				#print('a' + matchObj.group(2))
				width = float(str(matchObj.group(2)).replace('P','.'))
				height= float(str(matchObj.group(2)).replace('P','.'))
			else:
				#print(chip_type)
				matchObj = re.match(r'([a-zA-Z]*)([0-9]*)S', chip_type)
				#print('b' + matchObj.group(2))
				width = float(str(matchObj.group(2)))
				height= float(str(matchObj.group(2)))
		elif chip_type.find('X')!=-1:
			#print(chip_type)
			#rectangle
			#print()
			matchObj = re.match(r'([a-zA-Z]+)([0-9]+P[0-9]+|[0-9]+)X([0-9]+P[0-9]+|[0-9]+)', chip_type)
			#print(chip_type)
			#str(matchObj.group(2)).replace('P','.')
			#str(matchObj.group(3)).replace('P','.')
			width = float(str(matchObj.group(2)).replace('P','.'))
			height= float(str(matchObj.group(3)).replace('P','.'))
		

		if UsedPinDict.get(i, 'noExist') != 'noExist':
			#print("PinPad : " + i)
			print("pin " + i,end=' ')
			print(j+" "+layer)
			#print("\t Coor : " + j)
			#print("\t Type : " + chip_type)
			#print("\t\t Width : " + str(width))
			#print("\t\t Height : " + str(height))
			left_x = float(j.split(",")[0]) - (width/2)
			right_x = float(j.split(",")[0]) + (width/2)
			lower_y = float(j.split(",")[1]) - (width/2)
			upper_y = float(j.split(",")[1]) + (width/2)
			# file.write("b{%d dt%d xy(%.3lf %.3lf %.3lf %.3lf %.3lf %.3lf %.3lf %.3lf)}\n" % (gds_layer, 0, Normalize(left_x),
			# 			Normalize(lower_y), Normalize(right_x), Normalize(lower_y), Normalize(right_x), Normalize(upper_y), Normalize(left_x), Normalize(upper_y)))
		else:
			# print("ObsPad : " + i)
			# print("\t Coor : " + j)
			# print("\t Type : " + chip_type)
			# print("\t\t Width : " + str(width))
			# print("\t\t Height : " + str(height))
			left_x = float(j.split(",")[0]) - (width/2)
			right_x = float(j.split(",")[0]) + (width/2)
			lower_y = float(j.split(",")[1]) - (width/2)
			upper_y = float(j.split(",")[1]) + (width/2)
			output_obs = str(int(left_x*100)) + " " + str(int(lower_y*100)) + " " + str(int(right_x*100)) + " " + str(int(upper_y*100)) + " "+ str(layerDict[layer]) +"\n"
			#obs_file.write(i+" "+keys+"\n")
			# file.write("b{%d dt%d xy(%.3lf %.3lf %.3lf %.3lf %.3lf %.3lf %.3lf %.3lf)}\n" % (gds_layer, 100, Normalize(left_x),
			# 			Normalize(lower_y), Normalize(right_x), Normalize(lower_y), Normalize(right_x), Normalize(upper_y), Normalize(left_x), Normalize(upper_y)))
			obs_file.write(output_obs)
	# file.write("}\n}\n");
	# file.close()
	#os.system("./gdt2gds temp.gdt "+output_name+".gds")

			
	obs_file.close()

#python InputParser.py [.clp] [net] [.dcf] [out]

clp_name = sys.argv[1]
netlist_name = sys.argv[2]
dcf_name = sys.argv[3]
output_name = sys.argv[4]

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
		if line.find('BOTTOM')!=-1:
			chipLayerDict[chip_name] = "BOTTOM"

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
		netName = netName.strip('\'')
		buf=""
		#buf=line.split(';')[1].replace(',','')
		if line.find(',')==-1:
			buf=line.split(';')[1]
		while line.find(',')!=-1:
			netChangeLine=1
			if line.find(',')!=-1 and line.find(';')!=-1:
				buf=line.split(';')[1].replace(',', '').replace('\n','')
			else:
				buf =buf+' '+line.replace(',', '').replace('\n','').replace('   ','')
			line=file.readline()
		if netChangeLine==1:
			netChangeLine=0
			buf=buf+' '+line.replace(',','').replace('\n','').replace('    ','')
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
		netName = netName.strip('\'')
		# buf=line.split(';')[1].replace(',','')
		if line.find(',')==-1:
			buf=line.split(';')[1]
		while line.find(',') != -1:
			netChangeLine = 1
			if line.find(',') != -1 and line.find(';') != -1:
				buf = line.split(';')[1].replace(',', '').replace('\n', '')
			else:
				buf = buf + ' ' + line.replace(',', '').replace('\n', '').replace('   ', '')
			line = file.readline()
		if netChangeLine == 1:
			netChangeLine = 0
			buf = buf + ' ' + line.replace(',', '').replace('\n', '').replace('    ', '')
		for i in buf.split():
			netData = netData + i + ' '
			pinCount = pinCount + 1
		if pinCount >= 2:
			netDict[netName] = netData
	elif netF==1 and line.find('DRAM')!=-1:

		pinCount=0
		netData=""
		netMem=""
		netName=line.split(' ;')[0]
		netName = netName.strip('\'')
		buf=""
		#buf=line.split(';')[1].replace(',','')
		if line.find(',')==-1:
			buf=line.split(';')[1]
		while line.find(',')!=-1:
			netChangeLine=1
			if line.find(',')!=-1 and line.find(';')!=-1:
				buf=line.split(';')[1].replace(',', '').replace('\n','')
			else:
				buf =buf+' '+line.replace(',', '').replace('\n','').replace('   ','')
			line=file.readline()
		if netChangeLine==1:
			netChangeLine=0
			buf=buf+' '+line.replace(',','').replace('\n','').replace('    ','')
		for i in buf.split():
			netData = netData + (i + ' ')
			pinCount= pinCount + 1
		if pinCount>=2:
			netDict[netName]=netData
	elif netF==1 and line.find('$')!=-1:
		netF=0
	line=file.readline()
file.close()



# 
#print(netDict)
#Signal Pin pair info
pinPairDict = {}
Final_Net_Dict = {}
#file=open(dcf_name,'r')
layerDict={}
with open(dcf_name, 'r', errors='ignore',encoding="utf-8") as file:
	line=file.readline()


	laayer_count = 0;
	while line:
		if line.find('( layer "')!=-1:
			layer_name = line.split('"')[1]
			if line.find('DIELECTRIC')==-1 and line.find('SURFACE')==-1:
				if line.find('TOP')!=-1 or line.find('V')!=-1 or line.find('G')!=-1 or line.find('S')!=-1 or line.find('BOTTOM')!=-1:
					layerDict[layer_name] = laayer_count
					laayer_count = laayer_count + 1
		line=file.readline()
	#print(layerDict)

with open(dcf_name, 'r', errors='ignore',encoding="utf-8") as file:
	line=file.readline()
	while line:
		if line.find('( signal "')!=-1:

			signal_name = line.split('"')[1]
			# print(signal_name)
			count = 0;
			net_data = ""
			while(True):
				line=file.readline()
				if line.find('( pinPairRef "')!=-1:
					pairBuf0=line.split('"')[1].split(':')[0]
					pairBuf1=line.split('"')[1].split(':')[1]
					net_data = net_data + str(pairBuf0) + ' ' + str(pairBuf1) + "\n"
					key = str(pairBuf0) + ':' + str(pairBuf1)
					pinPairDict[key] = signal_name
					count = count + 1
				if line.find('( objectStatus "')!=-1 or line.find('( signal "')!=-1:
					break
				
			if count > 0:
				Final_Net_Dict[signal_name] = net_data
			if count == 0 and netDict.get(signal_name, 'noExist') != 'noExist':
				#print(signal_name + "\n\t" + netDict[signal_name])
				Final_Net_Dict[signal_name] = netDict[signal_name]
		if line.find('( signal "')!=-1:
			continue
		line=file.readline()
	#file.close()
# print("Final_Net_Dict")
# print(Final_Net_Dict)
# print("pinPairDict")
# print(pinPairDict)
#Net class
#file=open(dcf_name,'r')
Wire_Width_Dict = {}
Wire_Space_Dict = {}
with open(dcf_name, 'r', errors='ignore',encoding="utf-8") as file:
	line=file.readline()
	while line:
		if line.find('physicalCSet ')!=-1:
				set_name = line.split('"')[1]
				print(set_name)
				while line.find('attribute "MIN_LINE_WIDTH"')==-1:
					line=file.readline()
				min_width = line.rstrip().split(',')[0].split("\" \"")[1]
				#pCSet_file.write("physicalCSet " + str(set_name) + '\n');
				#pCSet_file.write("\tMIN_LINE_WIDTH " + str(min_width) + '\n');
				print(" MIN_WIDTH: " + str(min_width))
				Wire_Width_Dict[str(set_name)] = str(int((float(min_width)*100)))
		if line.find('spacingCSet ')!=-1:
			set_name = line.split('"')[1]
			print(set_name)
			while line.find('attribute "LINE_TO_LINE_SPACING"')==-1:
				line=file.readline()
			min_spacing = line.rstrip().split(',')[0].split("\" \"")[1]
			#sCSet_file.write("spacingCSet " + str(set_name) + '\n');
			#sCSet_file.write("\tLINE_TO_LINE_SPACING " + str(min_spacing) + '\n');
			print("LINE_TO_LINE_SPACING: " + str(min_spacing))
			Wire_Space_Dict[str(set_name)] = str(int((float(min_spacing)*100)))
		line=file.readline()


# print(Wire_Space_Dict)
# print(Wire_Width_Dict)

with open(dcf_name, 'r', errors='ignore',encoding="utf-8") as file:
	line=file.readline()
	netClassDict = {}
	physical_Dict = {}
	spacing_Dict = {}
	while line:
		if line.find('netClass "')!=-1:   
			net_class_name = line.split('"')[1]
			
			pSetRef = "DEFAULT"
			sSetRef = "DEFAULT"
			line=file.readline()
			while line.find('member (') == -1:
				if line.find('physicalCSetRef "') != -1:
					pSetRef = line.split('"')[1]
				if line.find('spacingCSetRef "') != -1:
					sSetRef = line.split('"')[1]
				if line.find('netClass "')!=-1 or line.find('objectStatus')!=-1 or not line:
					break
				line=file.readline()
			if line.find('netClass "')!=-1 or line.find('objectStatus')!=-1 or not line:
				continue
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
#file.close()

# print("netClassDict")
# print(netClassDict)
# print("physical_Dict")
# print(physical_Dict)
# print("spacing_Dict")
# print(spacing_Dict)

#diff
elediffDict = {}
diffDict = {}
with open(dcf_name, 'r', errors='ignore',encoding="utf-8") as file:
	line=file.readline()

	while line:
		if line.find('( differentialPair')!=-1:
			diff_list = []
			diff_class_name = line.split('"')[1]
			line=file.readline()
			while line.find('( member (') == -1:
				#print(line)
				if line.find('( electricalCSetRef "')!=-1:
					elename = line.split('"')[1]
					elediffDict[elename] = diff_class_name
				line=file.readline()
			#print(line)
			while line.find("( member (") != -1:
				#print(line)
				diff_net_name = line.split('"')[1]
				# print(diff_net_name)
				# print(">>")
				diff_list.append(diff_net_name)
				line=file.readline()
			diffDict[diff_class_name] = diff_list
		line=file.readline()

diff_file = open(output_name+'.diff','w')
for keys, values in diffDict.items():
	for i in values:
		diff_file.write(i+" "+keys+"\n")
diff_file.close()

#print(pinPairDict)
#print(diffDict)
#Match Group
tmpset = set()
UsedPinDict = {}
groupDict = {}
#file=open(dcf_name,'r')
drc_file = open(output_name+'.drc','w')
with open(dcf_name, 'r', errors='ignore',encoding="utf-8") as file:
	line=file.readline()
	while line:
		if line.find('( matchGroup "')!=-1 or line.find('( netGroup "')!=-1:
			group_name = line.split('"')[1]
			print("group "+group_name)
			tmpset.add(group_name)
			groupnetnamelist = []
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
					#print("\tpinPairRef:" + str(pairBuf0) + ' ' + str(pairBuf1))
					pin_pair_str = str(pairBuf0) + ' ' + str(pairBuf1)
					#print("net " + str(pairBuf0) + ' ' + str(pairBuf1))
					#print("pinPair")

					key = str(pairBuf0) + ':' + str(pairBuf1)
					
					if pinPairDict.get(key, 'noExist') != 'noExist':
						#print("\t\tReference Net:" + pinPairDict[key])
						print("net "+ str(pinPairDict[key]),end=' ')
						print(pin_pair_str.rstrip())
						tmplist = [ str(pinPairDict[key]), key ]
						groupnetnamelist.append(tmplist)
						if netClassDict.get(pinPairDict[key], 'noExist') != 'noExist':
							#print("net "+pinPairDict[key],end=' ')
							#print(str(pairBuf0) + ' ' + str(pairBuf1))
							net_name = pinPairDict[key]
							#print("\t\tNet Class:" + netClassDict[net_name])
							net_class_name = netClassDict[net_name]
							#print("\t\t\tphysicalCSetRef:" + physical_Dict[net_class_name])
							#print("\t\t\t\tWireWidth:" + Wire_Width_Dict[physical_Dict[net_class_name]])
							#print("\t\t\tspacingCSetRef:" + spacing_Dict[net_class_name])
							#print("\t\t\t\tWireSpacing:" + Wire_Space_Dict[spacing_Dict[net_class_name]])
							drc_file.write(str(pinPairDict[key]) + " " + Wire_Width_Dict[physical_Dict[net_class_name]] + " " + Wire_Space_Dict[spacing_Dict[net_class_name]]+ "\n")
						else : 
							#print("\t\tNet Class:DEFAULT")
							net_class_name = netClassDict[net_name]
							#print("\t\t\tphysicalCSetRef:DEFAULT")
							#print("\t\t\t\tWireWidth:" + Wire_Width_Dict["DEFAULT"])
							#print("\t\t\tspacingCSetRef:DEFAULT")
							#print("\t\t\t\tWireSpacing:" + Wire_Space_Dict["DEFAULT"])
							drc_file.write(str(pinPairDict[key]) + " " + Wire_Width_Dict["DEFAULT"] + " " + Wire_Space_Dict["DEFAULT"] + "\n")
						
					member_check = 1
				if line.find('( member ( signalRef "')!=-1:
					Net_Name = line.split('"')[1]
					#print("\tsignalRef:" + str(Net_Name))
					# print("signalRef")
					# print(Net_Name)
					if Final_Net_Dict.get(Net_Name, 'noExist') != 'noExist':
						#print("\t\tReference Pin-Pair:" + Final_Net_Dict[Net_Name].rstrip())
						#print(Net_Name)	
						
						pin_pair_list = Final_Net_Dict[Net_Name].rstrip().split(' ')
						for pin_pair in pin_pair_list:
							UsedPinDict[pin_pair.rstrip()] = 1
						if netClassDict.get(Net_Name, 'noExist') != 'noExist':
							
							net_name = Net_Name
							#print("\t\tNet Class:" + netClassDict[net_name])
							net_class_name = netClassDict[net_name]
							#print("\t\t\tphysicalCSetRef:" + physical_Dict[net_class_name])
							#print("\t\t\t\tWireWidth:" + Wire_Width_Dict[physical_Dict[net_class_name]])
							#print("\t\t\tspacingCSetRef:" + spacing_Dict[net_class_name])
							#print("\t\t\t\tWireSpacing:" + Wire_Space_Dict[spacing_Dict[net_class_name]])
							drc_file.write(str(Net_Name) + " " + Wire_Width_Dict[physical_Dict[net_class_name]] + " " + Wire_Space_Dict[spacing_Dict[net_class_name]]+ "\n")
						else : 
							#print("\t\tNet Class:DEFAULT")
							net_class_name = netClassDict[net_name]
							#print("\t\t\tphysicalCSetRef:DEFAULT")
							#print("\t\t\t\tWireWidth:" + Wire_Width_Dict["DEFAULT"])
							#print("\t\t\tspacingCSetRef:DEFAULT")
							#print("\t\t\t\tWireSpacing:" + Wire_Space_Dict["DEFAULT"])
							drc_file.write(str(Net_Name) + " " + Wire_Width_Dict["DEFAULT"] + " " + Wire_Space_Dict["DEFAULT"]+ "\n")
						print("net "+ str(Net_Name), end=' ')
						tmplist = [ Net_Name , Final_Net_Dict[Net_Name].rstrip().replace('\n',' ') ]
						groupnetnamelist.append(tmplist)
						print(Final_Net_Dict[Net_Name].rstrip().replace('\n',' '))

					member_check = 1
				if line.find('( member ( diffPairRef "')!=-1:
					Net_Name = line.split('"')[1]

					print("diff")
					#print(netClassDict[Net_Name])
					#print(Net_Name)
					for i in diffDict[Net_Name]:
						if i in Final_Net_Dict:
							print("net " + i + " " +Final_Net_Dict[i].rstrip().replace('\n',' '))
							pin_pair_list = Final_Net_Dict[i].rstrip().split(' ')
							for pin_pair in pin_pair_list:
								UsedPinDict[pin_pair.rstrip()] = 1
							if netClassDict.get(i, 'noExist') != 'noExist':
								net_class_name = netClassDict[i]
								drc_file.write(str(i) + " " + Wire_Width_Dict[physical_Dict[net_class_name]] + " " + Wire_Space_Dict[spacing_Dict[net_class_name]]+ "\n")
							else:
								
								drc_file.write(str(i) + " " + Wire_Width_Dict["DEFAULT"] + " " + Wire_Space_Dict["DEFAULT"]+ "\n")
							tmplist = [ i , Final_Net_Dict[i].rstrip().replace('\n',' ') ]
							groupnetnamelist.append(tmplist)
					#print(diffDict[Net_Name])
					member_check = 1
				if line.find('( member (')!=-1:
					member_check = 1
				if member_check == 1 and line.find("member")==-1:
					groupDict[group_name] = groupnetnamelist
					break
				# if line.find('( matchGroup "')!=-1 or line.find('( netGroup "')!=-1:
				# 	break
				
				line=file.readline()
		line=file.readline()

electricalDict = set()
with open(dcf_name, 'r', errors='ignore',encoding="utf-8") as file:
	line=file.readline()
	while line:
		if line.find('( electricalCSet "')!=-1:
			electricalDict.add(line.split('"')[1])
		line=file.readline()

# print("electricalDict")
# print(electricalDict)
for i in electricalDict:
	if i not in tmpset and i != 'DEFAULT':
		if i in elediffDict:
			print("group "+elediffDict[i])
			groupnetnamelist = []
			for j in diffDict[elediffDict[i]]:
				if j in Final_Net_Dict:
					print("net "+j,end=' ')
					print(Final_Net_Dict[j].rstrip().replace('\n',' '))
					pin_pair_list = Final_Net_Dict[j].rstrip().split(' ')
					for pin_pair in pin_pair_list:
						UsedPinDict[pin_pair.rstrip()] = 1
					if netClassDict.get(j, 'noExist') != 'noExist':
						net_class_name = netClassDict[j]
						drc_file.write(str(j) + " " + Wire_Width_Dict[physical_Dict[net_class_name]] + " " + Wire_Space_Dict[spacing_Dict[net_class_name]]+ "\n")
					else:
						drc_file.write(str(j) + " " + Wire_Width_Dict["DEFAULT"] + " " + Wire_Space_Dict["DEFAULT"]+ "\n")
					tmplist = [ j , Final_Net_Dict[j].rstrip().replace('\n',' ') ]
					groupnetnamelist.append(tmplist)
			groupDict[elediffDict[i]] = groupnetnamelist
drc_file.close()

os.system("python InputParser.py " + clp_name + " " + netlist_name + " " + output_name + ".netlist")




group_file = open(output_name+'.group','w')
for keys, values in groupDict.items():
	for i in values:
		#tmpset.add(i[0])
		group_file.write(i[0]+" "+i[1].replace(":"," ")+" "+keys+"\n")
group_file.close()


set_file = open(output_name+'.set','w')
for i in tmpset:
	set_file.write(i+"\n")
set_file.close()



output_gds(chipDict, ID_TypeDict, UsedPinDict, chipLayerDict,output_name, layerDict)

layer_file = open(output_name+'.layer','w')
layer_file.write(str(len(layerDict))+"\n")
for keys, values in layerDict.items():
	layer_file.write(keys+" "+str(values)+"\n")
layer_file.close()


"""
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
	else:
		print("ObsPad : " + i)
		print("\t Coor : " + j)
		print("\t Type : " + chip_type)
		print("\t\t Width : " + str(width))
		print("\t\t Height : " + str(height))

	#print(i,j,chip_type,width,height)
"""



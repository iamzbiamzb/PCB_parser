import string
import os
import sys
import re

class Rule:
	diff = 0
	group = 0
	target = 0
	targetRule = []
	diffRule = []
	groupRule = []
	def __init__(self):
		self.diff = 0
		self.group = 0
		self.target = 0
		self.diffRule = []
		self.groupRule = []
		self.targetRule = []
	def setdiffRule(self, r):
		self.diff = self.diff + 1
		if r != "":
			self.diffRule.append(r)
	def setgroupRule(self, r):
		self.group = self.group + 1
		self.groupRule.append(r)
	def settarget(self, r):
		self.target = 1
		self.targetRule.append(r)


def output_gds(chipDict, ID_TypeDict, UsedPinDict, chipLayerDict, output_name, layerDict):
	
	obs_file = open(output_name+'.obs','w')
	for i,j in chipDict.items():

		chip_name = i.split('.')[0]

		if chip_name in chipLayerDict:
			layer = chipLayerDict[chip_name]

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


def layer(dcf_name):
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
	return layerDict

def pin_info(clp_name,layerDict):
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
	count = 0
	chipDict={}
	chipAllPinDict={}
	ID_TypeDict={}
	chipLayerDict = {}
	file = open(clp_name, 'r')
	line = file.readline()
	while line:
		if line.find('_clpDBCreateText')!=-1:
			chip_name=line.split('"')[1]
			line = file.readline()
			line = file.readline()
			for i in layerDict:
				if line.find(i)!=-1:
					chipLayerDict[chip_name] = i

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
	return chipDict,chipAllPinDict,ID_TypeDict,chipLayerDict



def net(netlist_name):
	file = open(netlist_name,'r')
	netF=0
	netChangeLine=0
	pinCount=0
	buf=""
	netData=""
	netMem=""
	netName=""
	netDict={}
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
	return netDict

def used_net(dcf_name):
	pinPairDict = {}
	Final_Net_Dict = {}
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
		return pinPairDict,Final_Net_Dict

def target(dcf_name):
	SignalTargetDict = {}
	PinpairTargetDict = {}
	with open(dcf_name, 'r', errors='ignore',encoding="utf-8") as file:
		line=file.readline()
		while line:
			if line.find('( signal "')!=-1:
				signal_name = line.split('"')[1]
				while(True):
					line=file.readline()
					if line.find('RELATIVE_PROPAGATION_DELAY')!=-1 and line.find('TARGET,TARGET')!=-1:
						line = file.readline()
						line = file.readline()
						SignalTargetDict[signal_name] = line.split('"')[1]
					if line.find('( objectStatus "')!=-1 or line.find('( signal "')!=-1:
						break
			if line.find('( signal "')!=-1:
				continue
			line=file.readline()

	with open(dcf_name, 'r', errors='ignore',encoding="utf-8") as file:
		line=file.readline()
		while line:
			if line.find('( pinPair "')!=-1:
				pinpair_name = line.split('"')[1]
				while(True):
					line=file.readline()
					if line.find('RELATIVE_PROPAGATION_DELAY')!=-1 and line.find('TARGET,TARGET')!=-1:
						line = file.readline()
						line = file.readline()
						PinpairTargetDict[pinpair_name] = line.split('"')[1]
					if line.find('( pinPair "')!=-1 or line.find('( electricalNet "')!=-1 or line.find('( signal "')!=-1:
						break
			if line.find('( pinPair "')!=-1:
				continue
			line=file.readline()

	return SignalTargetDict, PinpairTargetDict

def drc(dcf_name):
	Wire_Width_Dict = {}
	Wire_Space_Dict = {}
	netClassDict = {}
	physical_Dict = {}
	spacing_Dict = {}
	with open(dcf_name, 'r', errors='ignore',encoding="utf-8") as file:
		line=file.readline()
		while line:
			if line.find('physicalCSet ')!=-1:
					set_name = line.split('"')[1]
					#print(set_name)
					while line.find('attribute "MIN_LINE_WIDTH"')==-1:
						line=file.readline()
					min_width = line.rstrip().split(',')[0].split("\" \"")[1]
					#pCSet_file.write("physicalCSet " + str(set_name) + '\n');
					#pCSet_file.write("\tMIN_LINE_WIDTH " + str(min_width) + '\n');
					#print(" MIN_WIDTH: " + str(min_width))
					Wire_Width_Dict[str(set_name)] = str(int((float(min_width)*100)))
			if line.find('spacingCSet ')!=-1:
				set_name = line.split('"')[1]
				#print(set_name)
				while line.find('attribute "LINE_TO_LINE_SPACING"')==-1:
					line=file.readline()
				min_spacing = line.rstrip().split(',')[0].split("\" \"")[1]
				#sCSet_file.write("spacingCSet " + str(set_name) + '\n');
				#sCSet_file.write("\tLINE_TO_LINE_SPACING " + str(min_spacing) + '\n');
				#print("LINE_TO_LINE_SPACING: " + str(min_spacing))
				Wire_Space_Dict[str(set_name)] = str(int((float(min_spacing)*100)))
			line=file.readline()



	################    DRC   ################
	with open(dcf_name, 'r', errors='ignore',encoding="utf-8") as file:
		line=file.readline()
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
	return Wire_Width_Dict,Wire_Space_Dict,netClassDict,physical_Dict,spacing_Dict

def diff(dcf_name):
	diffRef = {}
	diffDict = {}
	diffRule = {}
	with open(dcf_name, 'r', errors='ignore',encoding="utf-8") as file:
		line=file.readline()

		while line:
			if line.find('( differentialPair')!=-1:
				diff_list = []
				tmplist = []
				diff_class_name = line.split('"')[1]
				line=file.readline()
				
				while line.find('( member (') == -1:
					if line.find('( electricalCSetRef "')!=-1:
						elename = line.split('"')[1]
						diffRef[diff_class_name] = elename
						
					if line.find("DIFFP_PHASE_TOL")!=-1:
						tmplist.append(["DIFFP_PHASE_TOL",line.split('"')[3]])
					if line.find("PROPAGATION_DELAY_MAX")!=-1:
						tmplist.append(["PROPAGATION_DELAY_MAX",line.split('"')[3]])
					if line.find("PROPAGATION_DELAY_MIN")!=-1:
						tmplist.append(["PROPAGATION_DELAY_MIN",line.split('"')[3]])
					if line.find("TOTAL_ETCH_LENGTH_MIN")!=-1:
						tmplist.append(["TOTAL_ETCH_LENGTH_MIN",line.split('"')[3]])
					if line.find("TOTAL_ETCH_LENGTH_MAX")!=-1:
						tmplist.append(["TOTAL_ETCH_LENGTH_MAX",line.split('"')[3]])
					line=file.readline()
				while line.find("( member (") != -1:
					diff_net_name = line.split('"')[1]
					diff_list.append(diff_net_name)
					line=file.readline()
				diffDict[diff_class_name] = diff_list
				diffRule[diff_class_name] = tmplist
			line=file.readline()
	return diffRef,diffDict,diffRule

def ele(dcf_name):
	electricalDict = {}
	with open(dcf_name, 'r', errors='ignore',encoding="utf-8") as file:
		line=file.readline()

		while line:
			if line.find('( electricalCSet "')!=-1:
				name = line.split('"')[1]
				tmplist = []
				line=file.readline()
				while line:
					if line.find("DIFFP_PHASE_TOL")!=-1:
						tmplist.append(["DIFFP_PHASE_TOL",line.split('"')[3]])
					if line.find("PROPAGATION_DELAY_MAX")!=-1:
						tmplist.append(["PROPAGATION_DELAY_MAX",line.split('"')[3]])
					if line.find("PROPAGATION_DELAY_MIN")!=-1:
						tmplist.append(["PROPAGATION_DELAY_MIN",line.split('"')[3]])
					if line.find("TOTAL_ETCH_LENGTH_MIN")!=-1:
						tmplist.append(["TOTAL_ETCH_LENGTH_MIN",line.split('"')[3]])
					if line.find("TOTAL_ETCH_LENGTH_MAX")!=-1:
						tmplist.append(["TOTAL_ETCH_LENGTH_MAX",line.split('"')[3]])
					if line.find('( electricalCSet "')!=-1 or line.find('topologyData')!=-1:
						electricalDict[name] = "DEFAULT"
						break
					line=file.readline()
				electricalDict[name] = tmplist
				continue
			line=file.readline()
	return electricalDict

def Group(dcf_name,pinPairDict,Final_Net_Dict,diffDict):
	groupDict = {}
	groupTolenece = {}
	with open(dcf_name, 'r', errors='ignore',encoding="utf-8") as file:
		line=file.readline()
		while line:
			if line.find('( matchGroup "')!=-1 or line.find('( netGroup "')!=-1:
				group_name = line.split('"')[1]
				groupnetnamelist = []
				tmplist = []
				member_check = 0
				while(True):
					if line.find('"RELATIVE_PROPAGATION_DELAY"')!=-1:
						tmplist.append(["RELATIVE_PROPAGATION_DELAY",line.split('"')[3]])
					if line.find("PROPAGATION_DELAY_MAX")!=-1:
						tmplist.append(["PROPAGATION_DELAY_MAX",line.split('"')[3]])
					if line.find("PROPAGATION_DELAY_MIN")!=-1:
						tmplist.append(["PROPAGATION_DELAY_MIN",line.split('"')[3]])
					if line.find("TOTAL_ETCH_LENGTH_MIN")!=-1:
						tmplist.append(["TOTAL_ETCH_LENGTH_MIN",line.split('"')[3]])
					if line.find("TOTAL_ETCH_LENGTH_MAX")!=-1:
						tmplist.append(["TOTAL_ETCH_LENGTH_MAX",line.split('"')[3]])
					if line.find('( member ( pinPairRef "')!=-1:
						pairBuf0=line.split('"')[1].split(':')[0]
						pairBuf1=line.split('"')[1].split(':')[1]
						pin_pair_str = str(pairBuf0) + ' ' + str(pairBuf1)
						key = str(pairBuf0) + ':' + str(pairBuf1)
						if pinPairDict.get(key, 'noExist') != 'noExist':
							tlist = [ str(pinPairDict[key]), key ]
							groupnetnamelist.append(tlist)
						member_check = 1
					if line.find('( member ( signalRef "')!=-1:
						Net_Name = line.split('"')[1]
						if Final_Net_Dict.get(Net_Name, 'noExist') != 'noExist':
							tlist = [ Net_Name , Final_Net_Dict[Net_Name].rstrip().replace('\n',' ') ]
							groupnetnamelist.append(tlist)
						member_check = 1
					if line.find('( member ( diffPairRef "')!=-1:
						Net_Name = line.split('"')[1]
						for i in diffDict[Net_Name]:
							if i in Final_Net_Dict:
								tlist = [ i , Final_Net_Dict[i].rstrip().replace('\n',' ') ]
								groupnetnamelist.append(tlist)
						member_check = 1
					if line.find('( member (')!=-1:
						member_check = 1
					if member_check == 1 and line.find("member")==-1:
						groupDict[group_name] = groupnetnamelist
						groupTolenece[group_name] = tmplist
						break
					line=file.readline()
			line=file.readline()
	return groupDict,groupTolenece

def netrule(Final_Net_Dict,electricalDict,diffDict,diffRule,diffRef,groupDict,groupTolenece,SignalTargetDict,PinpairTargetDict):
	netRuleDict = {}
	for key,values in electricalDict.items():
		for i,j in diffRef.items():
			if j == key:
				for z in diffDict[i]:
					if z not in Final_Net_Dict:
						continue
					name = z+" "+Final_Net_Dict[z]
					if name not in netRuleDict:
						tmpRule = Rule()
						netRuleDict[name] = tmpRule
					if values != "":
						netRuleDict[name].setdiffRule([values,i])
					for k in diffRule[i]:
						netRuleDict[name].setdiffRule([k,i])
	for key,values in groupDict.items():
		for i in groupTolenece[key]:	
			for j in values:
				name = j[0]+" "+j[1]
				if name not in netRuleDict:
					tmpRule = Rule()
					netRuleDict[name] = tmpRule

				netRuleDict[name].setgroupRule([i,key])
				if j[0] in SignalTargetDict:
					netRuleDict[name].settarget(key)
				if j[1] in PinpairTargetDict:
					netRuleDict[name].settarget(key)
	return netRuleDict

def Usedpin(Final_Net_Dict):
	UsedPinDict = {}
	for i,j in Final_Net_Dict.items():
		arr = j.split(" ")
		for z in arr:
			UsedPinDict[z] = 1
	return UsedPinDict

clp_name = sys.argv[1]
netlist_name = sys.argv[2]
dcf_name = sys.argv[3]
output_name = sys.argv[4]

layerDict = layer(dcf_name)
chipDict,chipAllPinDict,ID_TypeDict,chipLayerDict = pin_info(clp_name,layerDict)
netDict = net(netlist_name)
pinPairDict,Final_Net_Dict = used_net(dcf_name)
Wire_Width_Dict,Wire_Space_Dict,netClassDict,physical_Dict,spacing_Dict = drc(dcf_name)
diffRef,diffDict,diffRule = diff(dcf_name)
electricalDict = ele(dcf_name)
groupDict,groupTolenece = Group(dcf_name,pinPairDict,Final_Net_Dict,diffDict)
SignalTargetDict, PinpairTargetDict = target(dcf_name)
UsedPinDict = Usedpin(Final_Net_Dict) 
netRuleDict = netrule(Final_Net_Dict,electricalDict,diffDict,diffRule,diffRef,groupDict,groupTolenece,SignalTargetDict,PinpairTargetDict)


print("++++++diffRule++++++")
for i in diffRule:
	print(i)
	print(diffRule[i])
print("++++++electricalDict++++++")
for i in electricalDict:
	print(i)
	print(electricalDict[i])
print("++++++groupTolenece++++++")
for i in groupTolenece:
	print(i)
	print(groupTolenece[i])

drc_file = open(output_name+'.drc','w')
for i in netDict:
	if i in netClassDict:
		drc_file.write(i + " " + Wire_Width_Dict[physical_Dict[netClassDict[i]]] + " " + Wire_Space_Dict[spacing_Dict[netClassDict[i]]]+ "\n")
	else:
		drc_file.write(i + " " + Wire_Width_Dict["DEFAULT"] + " " + Wire_Space_Dict["DEFAULT"] + "\n")
drc_file.close()

group_file = open(output_name+'.group','w')
for keys, values in groupDict.items():
	for i in values:
		group_file.write(i[0]+" "+i[1].replace(":"," ")+" "+keys+"\n")
group_file.close()

diff_file = open(output_name+'.diff','w')
for keys, values in diffDict.items():
	for i in values:
		diff_file.write(i+" "+keys+"\n")
diff_file.close()

layer_file = open(output_name+'.layer','w')
layer_file.write(str(len(layerDict))+"\n")
for keys, values in layerDict.items():
	layer_file.write(keys+" "+str(values)+"\n")
layer_file.close()

rule_file = open(output_name+'.rule','w')
for i,j in netRuleDict.items():
	rule_file.write(i+"\n")

	rule_file.write("Target = " + str(j.target) + "\n")
	rule_file.write("Target Rule START\n")
	for z in j.targetRule:
		rule_file.write(z+"\n")
	rule_file.write("Target Rule END\n")

	rule_file.write("Diff = " + str(j.diff) + "\n")
	rule_file.write("Diff Rule START\n")
	for z in j.diffRule:
		rule_file.write(z[1]+" "+z[0][0]+ " " + z[0][1] + "\n")
	rule_file.write("Diff Rule END\n")

	rule_file.write("Group = " + str(j.group) + "\n")
	rule_file.write("Group Rule START\n")
	for z in j.groupRule:
		rule_file.write(z[1]+" "+z[0][0]+ " " + z[0][1] + "\n")
	rule_file.write("Group Rule END\n")
	# print(j.target)
	# print(j.diff)
	# print(j.group)
	# print("gourp")
	# for z in j.groupRule:
	# 	print(z)
	# print("diff")
	# for z in j.diffRule:
	# 	print(z)
rule_file.close()

output_gds(chipDict, ID_TypeDict, UsedPinDict, chipLayerDict,output_name, layerDict)
os.system("python InputParser.py " + clp_name + " " + netlist_name + " " + output_name + ".netlist")






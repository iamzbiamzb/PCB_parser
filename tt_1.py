#dcf parser
from __future__ import division 
import string
import os
import sys
import re
import random

global_dict = {}
#source = ""
target = ""

# A Python3 program to find if 2 given line segments intersect or not 
  
class Point: 
	def __init__(self, x, y): 
		self.x = x 
		self.y = y 

class Net:
	def __init__(self):
		self.net_name = " "
		self.cpu_coor = Point(0,0)
		self.ddr_coor = Point(0,0)
		self.length = 0.0
		self.group_name = " "
		self.pinpair = " "
	def __lt__(self, other):
		if self.cpu_coor.x == other.cpu_coor.x or abs(int(self.cpu_coor.x) - int(other.cpu_coor.x)) < 100:
			return self.cpu_coor.y > other.cpu_coor.y
		return self.cpu_coor.x < other.cpu_coor.x


		
  
# Given three colinear points p, q, r, the function checks if  
# point q lies on line segment 'pr'	 
def onSegment(p, q, r): 
	if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and 
		   (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))): 
		return True
	return False
  
def orientation(p, q, r): 
	val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y)) 
	if (val > 0): 
		  
		# Clockwise orientation 
		return 1
	elif (val < 0): 
		  
		# Counterclockwise orientation 
		return 2
	else: 
		  
		# Colinear orientation 
		return 0

def doIntersect(p1,q1,p2,q2): 
	  
	# Find the 4 orientations required for	
	# the general and special cases 
	o1 = orientation(p1, q1, p2) 
	o2 = orientation(p1, q1, q2) 
	o3 = orientation(p2, q2, p1) 
	o4 = orientation(p2, q2, q1) 
  
	# General case 
	if ((o1 != o2) and (o3 != o4)): 
		return True
  
	# Special Cases 
  
	# p1 , q1 and p2 are colinear and p2 lies on segment p1q1 
	if ((o1 == 0) and onSegment(p1, p2, q1)): 
		return True
  
	# p1 , q1 and q2 are colinear and q2 lies on segment p1q1 
	if ((o2 == 0) and onSegment(p1, q2, q1)): 
		return True
  
	# p2 , q2 and p1 are colinear and p1 lies on segment p2q2 
	if ((o3 == 0) and onSegment(p2, p1, q2)): 
		return True
  
	# p2 , q2 and q1 are colinear and q1 lies on segment p2q2 
	if ((o4 == 0) and onSegment(p2, q1, q2)): 
		return True
  
	# If none of the cases 
	return False

def readfiles(netlist_name,path_name):
	# netlist_name = "see"
	# path_name = "path"

######################## see input ########################
	with open(netlist_name, 'r', errors='ignore',encoding="utf-8") as file:
		#print("open " + netlist_name )

		group = []
		netlist = []
		pinmap = {}
		pinlayer = {}
		#netset = set()
		line = file.readline()
		line = line.encode('utf-8').decode('utf-8-sig')
		#print(line)
		while line:
			arr = line.split()
			if arr[0] == "group":
				tmp = []
				tmp.append(arr[1])
				tmp.append([])
				line = file.readline()
				arr = line.split()
				while arr[0] != "group" and arr[0] != "pin":
					count = int(len(arr)/2)-1
					for i in range(count):
						tt = []
						tt.append(arr[1])
						tt.append(arr[i*2+2]+" "+arr[i*2+3])
						tmp[1].append(tt)
						#netset.add(arr[2]+" "+arr[3])
					#else:

						#print("=====something strange=====")
					line = file.readline()
					arr = line.split()
				group.append(tmp)
			elif arr[0] == "pin":
				#print(arr)
				pinmap[arr[1]] = arr[2].replace(","," ")
				pinlayer[arr[1]] = arr[3]
				line = file.readline()
			else:
				line = file.readline()
	#print(group)
	#print(pinmap)
	#print(pinlayer)
	# print(len(netset))
	# print(netset)
	# print(len(pinmap))
	# print(pinmap)

	newgroup = []
	for i in group:
		tmp = []
		tmp.append(i[0])
		tmp.append([])
		for j in i[1]:
		
			tt = []
			tt.append(j[0])
			arr = j[1].split()
			if arr[0] in pinmap and arr[1] in pinmap:
				tt.append([arr[0],pinmap[arr[0]],arr[1],pinmap[arr[1]]])
				tmp[1].append(tt)
			
			#else:
				#print("=====fail to find pin cood=====")
				#print(arr[0],arr[1])
		
		newgroup.append(tmp)

	# print(newgroup)

	# for i in netset:
	#	arr = i.split()
	#	if arr[0] in pinmap and arr[1] in pinmap:
	#		netlist.append([arr[0],pinmap[arr[0]],arr[1],pinmap[arr[1]]])

######################## path input ########################
	with open(path_name, 'r', errors='ignore',encoding="utf-8") as file:
		#print("open " + path_name )
		line = file.readline()
		line = line.encode('utf-8').decode('utf-8-sig')
		coodlist = []
		while line:
			Layer = ""
			Width = 0.0
			pathlist = []
			line = file.readline()
			arr = line.split()
			if len(arr) > 0 and arr[0] == "Width":
				Width = float(arr[1])
			line = file.readline()
			while line:
				arr = line.split()
				if arr[0] == "Path":
					if len(pathlist) == 1:
						break
					tmplist = []
					tmplist.append(len(coodlist))
					tmplist.append(pathlist[0])
					tmplist.append(pathlist[-1])
					tmplist.append(pathlist)
					tmplist.append(Width)
					#if Layer != "":
					tmplist.append(Layer)
					coodlist.append(tmplist)
					break
				elif arr[0] == "Layer":
					Layer = arr[1]
				else:
					cood = line.lstrip().rstrip()
					pathlist.append(cood)
				line = file.readline()	
			line = file.readline()
	
	return newgroup, coodlist

def line(p1, p2):
	A = (p1[1] - p2[1])
	B = (p2[0] - p1[0])
	C = (p1[0]*p2[1] - p2[0]*p1[1])
	return A, B, -C

def intersection(L1, L2):
	D  = L1[0] * L2[1] - L1[1] * L2[0]
	Dx = L1[2] * L2[1] - L1[1] * L2[2]
	Dy = L1[0] * L2[2] - L1[2] * L2[0]
	if D != 0:
		x = Dx / D
		y = Dy / D
		return x,y
	else:
		return False

######################## cross ########################
def cross(linea,lineb):
	arra = linea.split()
	#print(arra)
	arrb = lineb.split()
	#print(arrb)

	p1 = Point(float(arra[0]), float(arra[1])) 
	q1 = Point(float(arra[2]), float(arra[3])) 
	p2 = Point(float(arrb[0]), float(arrb[1])) 
	q2 = Point(float(arrb[2]), float(arrb[3])) 

	if doIntersect(p1, q1, p2, q2): 
		#print("Yes")

		L1 = line([float(arra[0]),float(arra[1])], [float(arra[2]),float(arra[3])])
		L2 = line([float(arrb[0]),float(arrb[1])], [float(arrb[2]),float(arrb[3])])

		R = intersection(L1, L2)
		if R:
			#print("Intersection detected:"+str(R[0])+" "+str(R[1]))
			return R
		else:
			#print("No single intersection point detected")
			return False
	else:
		return False
		#print("No")


######################## distance ########################

def disance(p1,p2):
	pos1 = p1.split()
	pos2 = p2.split()
	return ((float(pos1[0])-float(pos2[0])) ** 2.0 + (float(pos1[1])-float(pos2[1])) ** 2.0 ) ** 0.5

######################## findnext ########################

def nextpath(source,already):
	#os.system("pause")
	#print(source)
	#print(already)
	tmp = []
	already.add(source)
	ll = global_dict[source]
	if len(ll) > 1:
		pass
		#print("*****************here***************")
	for i in ll:
		if i[1] == source:
			opp = i[2]
		else:
			opp = i[1]

		if opp == target:
			#print("find target")
			return [i]
		elif opp in already:
			pass
		else:
			tmp = nextpath(opp,already)
			#print(tmp)
			if len(tmp) == 0:
				pass
				#already.discard(source)
				#return tmp
			else:
				tmp.append(i)
				return tmp
	already.discard(source)
	return tmp



######################## findpath ########################
def findpath(grouplist,pathlist,line1,line2, target_layer, output_name, drc_name, routing_dir):
	debug = False
	for i in pathlist:
		if i[1] in global_dict:
			global_dict[i[1]].append(i)
		else:
			global_dict[i[1]] = [i]
		if i[2] in global_dict:
			global_dict[i[2]].append(i)
		else:
			global_dict[i[2]] = [i]

	#for i in global_dict:
		#print(i)
		#print(len(global_dict[i]))


	nemo_gdfm = ""
	net_len = []

	net_count = 0
	signal_count = 0

	net_dict = {}
	net_group = []
	net_name = []


	net_list = []

	for i in grouplist:
		
		if debug:
			print("-----------")
			print(i[0])
		#print(i[1])
		
		for j in i[1]:
			
			#print(j[0]+" "+j[1][0]+" "+j[1][1]+" "+j[1][2]+" "+j[1][3])
			if j[1][1] not in global_dict or j[1][3] not in global_dict:
				#print("======find path fail======")
				#print(j[1][0]+" "+j[1][1])
				#print(j[1][2]+" "+j[1][3])
				if debug:
					print("========find path fail=======")
					print(j[0])
				continue
			if j[0] == "DDR_ODT" or j[0] == "DDR_CKE":
				continue
			# if net_dict.get(j[0], "None") == "None":

			# 	net_dict[j[0]] = i[0]
			# else:
			# 	print("j[cry] " + j[0])
			# 	continue
			if debug:
				print("========")
				print(j[0])
			global target
			target = j[1][3]
			already = set()
			mypath = nextpath(j[1][1],already)
			
			withline1 = []
			withline2 = []

			#print(mypath)
			totallen = 0.0
			firsttouch = ""

			nowpos = j[1][3]
			for z in mypath:
				#print(z)
				oldzz = ""

				if nowpos == z[1]:
					nowpos = z[2]
					for zz in z[3]:
						if debug:
							print(zz)
						if oldzz == "":
							oldzz = zz
						else:
							for l in line1:
								ttt = cross(zz+" "+oldzz,l)
								if ttt:
									if firsttouch == "":
										firsttouch = "withline1"
									if debug:
										print("cross")
									tmp = []
									tmp.append(z[5])
									tmp.append(ttt)
									tmp.append(totallen+disance(oldzz,str(ttt[0])+" "+str(ttt[1])))
									withline1.append(tmp)
							for l in line2:
								ttt = cross(zz+" "+oldzz,l)
								if ttt:
									if firsttouch == "":
										firsttouch = "withline2"
									if debug:
										print("cross")
									tmp = []
									tmp.append(z[5])
									tmp.append(ttt)
									tmp.append(totallen+disance(oldzz,str(ttt[0])+" "+str(ttt[1])))
									withline2.append(tmp)
							totallen += disance(oldzz,zz)
							oldzz = zz
							
				else:
					nowpos = z[1]
					for zz in reversed(z[3]):
						if debug:
							print(zz)
						if oldzz == "":
							oldzz = zz
						else:
							for l in line1:
								ttt = cross(zz+" "+oldzz,l)
								if ttt:
									if firsttouch == "":
										firsttouch = "withline1"
									if debug:
										print("cross")
									tmp = []
									tmp.append(z[5])
									tmp.append(ttt)
									tmp.append(totallen+disance(oldzz,str(ttt[0])+" "+str(ttt[1])))
									withline1.append(tmp)
							for l in line2:
								ttt = cross(zz+" "+oldzz,l)
								if ttt:
									if firsttouch == "":
										firsttouch = "withline2"
									if debug:
										print("cross")
									tmp = []
									tmp.append(z[5])
									tmp.append(ttt)
									tmp.append(totallen+disance(oldzz,str(ttt[0])+" "+str(ttt[1])))
									withline2.append(tmp)
							totallen += disance(oldzz,zz)
							oldzz = zz
							
			#print(totallen)
			#print(firsttouch)
			#print(withline1)
			fan_length = 0.0
			ddr_layer = ""
			cpu_layer = ""
			if len(withline1) > 0:
				withline1.sort(key = lambda x : x[2])
				if firsttouch == "withline1":
					for q in withline1:
						if q[0] == target_layer:
							cpu_layer = q[0]
							#print(withline1[0][0],end=' ')
							#print(withline1[0][1],end=' ')
							#print(withline1[0][2])
							fan_length += float(q[2])
				else:
					for q in reversed(withline1):
						if q[0] == target_layer:
							cpu_layer = q[0]
							#print(withline1[-1][0],end=' ')
							#print(withline1[-1][1],end=' ')
							#print(withline1[-1][2],end=' ')
							#print(totallen-withline1[-1][2])
							fan_length += float(totallen-q[2])
				#print(random.choice(withline1))
			#print(withline2)
			if len(withline2) > 0:
				withline2.sort(key = lambda x : x[2])
				if firsttouch == "withline2":
					for q in withline2:
						if q[0] == target_layer:
							ddr_layer = q[0]
							#print(withline2[0][0],end=' ')
							#print(withline2[0][1],end=' ')
							#print(withline2[0][2])
							fan_length += float(q[2])
				else:
					for q in reversed(withline2):
						if q[0] == target_layer:
							ddr_layer = q[0]
							#print(withline2[-1][0],end=' ')
							#print(withline2[-1][1],end=' ')
							#print(withline2[-1][2],end=' ')
							#print(totallen-withline2[-1][2])
							fan_length += float(totallen-q[2])
			if debug:
				print("withline1 " + str(len(withline1)))
				print("withline2 " + str(len(withline2)))
				print("ddr_layer " + ddr_layer)
				print("target_layer " + cpu_layer)
			if len(withline1) > 0 and len(withline2) > 0 and ddr_layer == target_layer and cpu_layer == target_layer:

				withline1.sort(key = lambda x : x[2])

				net = Net()

				content = ""
				if firsttouch == "withline1":
					x = str(int(float(withline1[0][1][0])*100))
					y = str(int(float(withline1[0][1][1])*100))
					content += str(signal_count) + " 0 0 " + str(net_count) + " "  + x + " " + y + "\n"
					net.cpu_coor = Point(x,y)
					signal_count += 1
				else:
					x = str(int(float(withline1[-1][1][0])*100))
					y = str(int(float(withline1[-1][1][1])*100))
					content += (str(signal_count) + " 0 0 " + str(net_count) + " "	+ x + " " + y + "\n")
					net.cpu_coor = Point(x,y)
					signal_count += 1
				withline2.sort(key = lambda x : x[2])
				if firsttouch == "withline2":
					x = str(int(float(withline2[0][1][0])*100))
					y = str(int(float(withline2[0][1][1])*100))
					#print(str(signal_count) + " 0 0 " + str(net_count) + " "  + x + " " + y )
					content += str(signal_count) + " 0 0 " + str(net_count) + " "  + x + " " + y + "\n"
					net.ddr_coor = Point(x,y)
					signal_count += 1
				else:
					x = str(int(float(withline2[-1][1][0])*100))
					y = str(int(float(withline2[-1][1][1])*100))
					#print(str(signal_count) + " 0 0 " + str(net_count) + " "  + x + " " + y )
					content += str(signal_count) + " 0 0 " + str(net_count) + " "  + x + " " + y+ "\n"
					net.ddr_coor = Point(x,y)
					signal_count += 1
				
				nemo_gdfm += content
				net_count += 1
				net_name.append(j[0])
				net_len.append(fan_length)
				net_group.append(i[0])

				net.net_name = str(j[0])
				net.length = fan_length
				net.group_name = str(i[0])
				net.pinpair = j[1][0] +" "+ j[1][2]
				#print(net.pinpair)
				net_list.append(net)
				

				#print(random.choice(withline2))
			# for z in mypath:

			#	oldzz = ""
			#	for idz,zz in enumerate(z[3]):
			#		if idz == 0:
			#			oldzz = zz
			#		else:
			#			ttt = cross(zz+" "+oldzz,line1)
			#			if ttt:
			#				withline1.append(ttt)

			#			ttt = cross(zz+" "+oldzz,line2)
			#			if ttt:
			#				withline2.append(ttt)
			#			oldzz = zz

			# if len(withline1) > 0:
			#	print(random.choice(withline1))
			# #print(withline2)
			# if len(withline2) > 0:
			#	print(random.choice(withline2))
			#print("\n")
		#print("\n\n")

	#drc_file = open(drc_name,'r')

	net_list.sort()
	max_x = 0
	max_y = 0
	
	for i in range(0, len(net_list)):

		# print("Net " + net_list[i].net_name)
		# print("\tGroup " + net_list[i].group_name)
		# print("\tLength " + str(net_list[i].length))
		# print("\tCPU coor " + net_list[i].cpu_coor.x + "," + net_list[i].cpu_coor.y)
		# print("\tDDR coor " + net_list[i].ddr_coor.x + "," + net_list[i].ddr_coor.y)
		if int(net_list[i].cpu_coor.x) > max_x:
			max_x = int(net_list[i].cpu_coor.x)
		if int(net_list[i].ddr_coor.x) > max_x:
			max_x = int(net_list[i].ddr_coor.x)
		if int(net_list[i].cpu_coor.y) > max_y:
			max_y = int(net_list[i].cpu_coor.y)
		if int(net_list[i].ddr_coor.y) > max_y:
			max_y = int(net_list[i].ddr_coor.y)

	max_x += 50000
	max_y += 50000
		
	DRC_DICT = {}
	NET_DRC_DICT = {}
	drc_id = 0
	with open(drc_name, 'r', errors='ignore',encoding="utf-8") as file:
		line=file.readline()
		line = line.encode('utf-8').decode('utf-8-sig')
		while line:
			drc_str = line.split()
			if len(drc_str) > 0:
				key = drc_str[1]+":"+drc_str[2]
				if DRC_DICT.get(key, 'noExist') == 'noExist':
					DRC_DICT[key] = drc_id
					drc_id += 1
				NET_DRC_DICT[drc_str[0]] = DRC_DICT[key]
			line=file.readline()


	group_id_dict = {}
	group_id = 1
	for n in range(0,len(net_list)):
		if group_id_dict.get(net_list[n].group_name, 'noExist') == 'noExist':
			group_id_dict[net_list[n].group_name] = group_id
			group_id += 1
		#print(net_name[n] + " "+ net_group[n] + " " + str(net_len[n]) + " " + str(group_id_dict[net_group[n]]) + " " + str(NET_DRC_DICT[net_name[n]]))
			

	# gdfm
	os.system("mkdir " + output_name )
	arr = output_name.split("/")
	fp = open(output_name + "/" + arr[-1] + ".gdfm", "wt")
	fp.write(".tech\n1 0 0 0 0 0 0 0 " + str(max_x) + " " + str(max_y) + "\n.end\n.cell\n.end\n.net\n")
	sig = 0
	for n in range(0,len(net_list)):
		#0 net0 0 1
		fp.write(str(n) + " net" + str(n)  + " " + str(sig) + " " + str(sig+1)+"\n")
		sig += 2
	fp.write(".end\n.pin\n")
	sig = 0
	for n in range(0,len(net_list)):
		#0 net0 0 1
		fp.write(str(sig) + " 0 0 " + str(n) + " "  + net_list[n].cpu_coor.x + " " + net_list[n].cpu_coor.y + "\n")
		fp.write(str(sig+1) + " 0 0 " + str(n) + " "  + net_list[n].ddr_coor.x + " " + net_list[n].ddr_coor.y  + "\n")
		sig += 2
	fp.write(".end\n")
	# pgr
	fpgr = open(output_name + "/" + arr[-1] + ".pgr", "wt")
	fpgr.write("1 1\n")
	fpgr.write(str(max_x) + " " + str(max_y) + "\n")
	for n in range(0,len(net_list)):
		#0 net0 0 1
		fpgr.write(".net " + str(n) + " " + str(NET_DRC_DICT[net_list[n].net_name]) + "\n")
		fpgr.write("0 0 0\n")
	
	fplg = open(output_name + "/" + arr[-1] + ".length", "wt")
	for n in range(0, len(net_list)):
		fplg.write( net_list[n].net_name + " " + net_list[n].pinpair + " " + net_list[n].group_name + " " + str(net_list[n].length) + "\n")

	frule = open(output_name + "/" + arr[-1] + ".rule", "wt")
	for keys,values in DRC_DICT.items():
		frule.write(str(values) + " " + str(keys.split(":")[0]) + " " + str(keys.split(":")[1]) + "\n")
	
	fsmk = open(output_name + "/" + arr[-1] + ".smk", "wt")
	fsmk.close()
		

	# for idx,i in enumerate(netlist):
	#	print(idx)
	#	#source = netlist[1]
	#	print("*******************"+i[1]+" "+i[3]+"**********************")

	#	if i[1] not in global_dict or i[3] not in global_dict:
	#		print(i[0]+" "+i[1])
	#		print(i[2]+" "+i[3])
	#		continue

	#	global target
	#	target = i[3]
	#	already = set()
	#	mypath = nextpath(i[1],already)
		
	#	withline1 = []
	#	withline2 = []

	#	for z in mypath:

	#		oldzz = ""
	#		for idz,zz in enumerate(z[3]):
	#			if idz == 0:
	#				oldzz = zz
	#			else:
	#				ttt = cross(zz+" "+oldzz,line1)
	#				if ttt:
	#					withline1.append(ttt)

	#				ttt = cross(zz+" "+oldzz,line2)
	#				if ttt:
	#					withline2.append(ttt)
	#				oldzz = zz

	#	if len(withline1) > 0:
	#		print(random.choice(withline1))
	#	#print(withline2)
	#	if len(withline2) > 0:
	#		print(random.choice(withline2))
	#	print("\n\n")
	
def read_fanout_line(line_name, line1, line2):
	with open(line_name, 'r', errors='ignore',encoding="utf-8") as file:
		line = file.readline()
		line = line.encode('utf-8').decode('utf-8-sig')
		while line:
			side = int(line.split(" ")[0])
			sx = line.split(" ")[1]
			sy = line.split(" ")[2]
			tx = line.split(" ")[3]
			ty = line.split(" ")[4]
			if side == 1:
				line1s = sx + " " + sy + " " + tx + " " + ty
				line1.append(line1s)
			if side == 2:
				line2s = sx + " " + sy + " " + tx + " " + ty
				line2.append(line2s)
			line = file.readline()	


######################## main ########################
if __name__ == '__main__': 
	routing_dir = 0#int(sys.argv[7])
	output_name = sys.argv[6]
	drc_name = sys.argv[5]
	target_layer = sys.argv[4]
	line_name = sys.argv[3]
	path_name = sys.argv[2]
	netlist_name = sys.argv[1]
	# python3 tt.py ../output/out2/see2 ../output/out2/path2 ../benchmarks/2_2.line TOP ../output/out2/2.drc ../output/out2/2.TOP
	# python3 tt.py see2 path2 2_2.line TOP 2.drc 2.TOP
	#line1 = input('please input fanout line1 2 point xy')
	line1 = []
	#print(line1)
	# line1 = line1.split()
	# print(line1)
	#line2 = input('please input fanout line2 2 point xy')
	line2 = []
	#print(line2)
	# line2 = line2.split()
	# print(line2)

	read_fanout_line(line_name, line1, line2)

	grouplist, pathlist= readfiles(netlist_name,path_name)
	# print(grouplist)
	#print(len(grouplist))
	# print("group ex")
	# print(grouplist[0])
	# print("path ex")
	# print(pathlist[0])
	#print(len(pathlist))

	#cross(line2,line1)

	findpath(grouplist,pathlist,line1,line2, target_layer, output_name, drc_name,routing_dir)
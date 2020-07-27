#CLP Path Parser
import string
import os
import sys
import re

clp_name = sys.argv[1]
#output_name = sys.argv[2]

file=open(clp_name,'r')
#group_file=open(output_name+'.matchGroup','wb')
line=file.readline()
while line:
    if line.find('(_clpPathStart')!=-1:
        point = line.split('_clpAdjustPt ')[1].split(' _clp_cinfo')[0]
        x = point.split(':')[0]
        y = point.split(':')[1]
        

        line=file.readline()
        width = line.split('_clpMKSConvert ')[1].split(' _clp_cinfo')[0]
        if width == '0.000000':

	        #print("Path BEGIN\n\tWidth " + str(width))
	        #print("\t" + str(x) + " " + str(y) )
	        while(True):
	        	#print(line)
	        	if line.find('_clpPathLine')!=-1:
	        		line=file.readline()
	        		point = line.split('_clpAdjustPt ')[1].split(' _clp_cinfo')[0]
	        		x = point.split(':')[0]
	        		y = point.split(':')[1]
	        		#print("\t" + str(x) + " " + str(y))
	        	elif line.find('"ETCH/')!=-1:
	        		layer = line.split('"ETCH/')[1].split('"')[0]
	        		#print("\tLayer " + str(layer))
	        		line=file.readline()
	        	elif line.find("_clpPl = nil")!=-1 or line.find("_clpDBCreateCloseShape")!=-1:
	        		#print("Path END")
	        		break
	        	elif line.find('(_clpPathStart')!=-1:
	        		break
	        	elif not line:
	        		break
	        	else:
	        		line=file.readline()

        else :
        	print("Path BEGIN\n\tWidth " + str(width))
	        print("\t" + str(x) + " " + str(y) )
	        while(True):
	        	#print(line)
	        	if line.find('_clpPathLine')!=-1:
	        		line=file.readline()
	        		point = line.split('_clpAdjustPt ')[1].split(' _clp_cinfo')[0]
	        		x = point.split(':')[0]
	        		y = point.split(':')[1]
	        		print("\t" + str(x) + " " + str(y))
	        	elif line.find('"ETCH/')!=-1:
	        		layer = line.split('"ETCH/')[1].split('"')[0]
	        		print("\tLayer " + str(layer))
	        		line=file.readline()
	        	elif line.find("_clpPl = nil")!=-1 or line.find("_clpDBCreateCloseShape")!=-1:
	        		print("Path END")
	        		break
	        	else:
	        		line=file.readline()
    if line.find('(_clpPathStart')!=-1:
        continue
    line=file.readline()
file.close()
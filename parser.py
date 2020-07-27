#parser
import string
import os
import sys
import re

test = True

casenumber = sys.argv[1]

outputdir = "../output/out" + casenumber + "/"
inputdir = "../benchmarks/"

os.system("rm -r "+outputdir)
os.system("mkdir " + outputdir )
os.system("python3 DCF_parser.py "+ inputdir + casenumber+".clp "+ inputdir + casenumber+".txt "+ inputdir + casenumber+".dcf "+ outputdir + casenumber+" > " + outputdir +"see"+casenumber)
os.system("python3 CLP_Path_Parser.py "+inputdir +casenumber+".clp > " + outputdir + "path"+casenumber)

if test == True:
	layerlist = []
	with open(outputdir+casenumber+".layer", 'r', errors='ignore',encoding="utf-8") as file:
		line = file.readline()
		for i in range(int(line)):
			line = file.readline()
			layerlist.append(line.split()[0])
			# arr = file.readline().split()
			# strr = ""
			# for i in arr[0:-1]:
			# 	strr = strr + i + " "
			# strr.strip()
			# print(strr)
			# layerlist.append(strr)

	#print(layerlist)

	for i in layerlist:
		#print("==="+i+"===")
		#os.system("rm -r "+"../output/out" + casenumber + "/" + casenumber + "." + i)
		#os.system("mkdir "+"../output/out" + casenumber + "/" + casenumber + "." + i)
		os.system("python3 tt_1.py " + "../output/out" + casenumber + "/see" + casenumber + " ../output/out" + casenumber + "/path" + casenumber + " ../benchmarks/" + casenumber + ".line " + i + " ../output/out" + casenumber + "/" + casenumber + ".drc ../output/out" + casenumber + "/" + casenumber + "." + i)
		print("python3 tt_1.py " + "../output/out" + casenumber + "/see" + casenumber + " ../output/out" + casenumber + "/path" + casenumber + " ../benchmarks/" + casenumber + ".line " + i + " ../output/out" + casenumber + "/" + casenumber + ".drc ../output/out" + casenumber + "/" + casenumber + "." + i)
		#print("==="+i+" fin"+"===")
		#print("python3 tt.py " + "../output/out" + casenumber + "/see" + casenumber + " ../output/out" + casenumber + "/path" + casenumber + " ../benchmarks/" + casenumber + ".line " + i + " ../output/out" + casenumber + "/" + casenumber + ".drc ../output/out" + casenumber + "/" + casenumber + "." + i)
# python3 tt.py ../output/out2/see2 ../output/out2/path2 ../benchmarks/2.line TOP ../output/out2/2.drc ../output/out2/2.TOP
# python3 tt.py ../output/out2/see2 ../output/out2/path2 ../benchmarks/2.line TOP ../output/out2/2.drc .../output/out2/2.TOP

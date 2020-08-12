#run
import string
import os
import sys
import re


os.system("mkdir ../output/")
for i in range(7):
	print("case" + str(i+1))
	os.system("python3 parser.py " + str(i+1))

# for i in range(20):
# 	print("caseb_" + str(i+1))
# 	if i < 9 :
# 		os.system("python3 parser.py b_0" + str(i+1))
# 	else:
# 		os.system("python3 parser.py b_" + str(i+1))
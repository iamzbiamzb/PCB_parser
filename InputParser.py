import string
import  os
import sys
import re

#python InputParser.py [.clp] [net] [.dcf] [out]

clpname = sys.argv[1]
file = open(clpname, 'r')

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

# Parse Pin info

while line:
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
        #print(line.split('"')[5])
        
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
file = open(sys.argv[2],'r')

file3 = open(sys.argv[3],'wb')
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
                buf =buf+' '+line.replace(',', '').replace('\n','').replace('   ','')
            line=file.readline()
        if netChangeLine==1:
            netChangeLine=0
            buf=buf+' '+line.replace(',','').replace('\n','').replace('    ','')
        for i in buf.split():
            if chipDict.get(i,'noExist')!='noExist':
                pinToNetDict[i]=netName
                if netMem=='':
                    netMem=i
                else:
                    netMem=netMem+':'+i
                pin_type = i.split('.')[0]
                #print(i)
                type = ID_TypeDict[pin_type]
                chipDict[i] = chipDict[i] + ' ' + type
                netData=netData+i+' '+chipDict[i]+'\n'
                pinCount=pinCount+1
        if pinCount>=2:
            #file2.write(netName+'\n'+netData)
            file3.write("NetName " + netName.strip("\'") + '\n')
            pin_list = netData.split('\n')
            file3.write("PIN START\n")
            for p in range(0,len(pin_list) - 1):
                file3.write("\t" + str(pin_list[p]) + '\n')
            file3.write("PIN END\n")
            netDict[netName]=netData
    elif netF==1 and line.find('EBI')!=-1:
        pinCount = 0
        netData = ""
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
                buf = buf + ' ' + line.replace(',', '').replace('\n', '').replace('   ', '')
            line = file.readline()
        if netChangeLine == 1:
            netChangeLine = 0
            buf = buf + ' ' + line.replace(',', '').replace('\n', '').replace('    ', '')
        for i in buf.split():
            if chipDict.get(i, 'noExist') != 'noExist':
                pinToNetDict[i] = netName
                if netMem == '':
                    netMem = i
                else:
                    netMem = netMem + ':' + i
                netData = netData + i + ' ' + chipDict[i] + '\n'
                pinCount = pinCount + 1
        if pinCount >= 2:
            #file2.write(netName + '\n' + netData)
            file3.write("NetName " + netName.strip("\'") + '\n')
            pin_list = netData.split('\n')
            file3.write("PIN START\n")
            for p in range(0,len(pin_list)- 1):
                file3.write("\t" + str(pin_list[p]) + '\n')
            file3.write("PIN END\n")
            netDict[netName] = netData
    elif netF==1 and line.find('DRAM')!=-1:
        pinCount = 0
        netData = ""
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
                buf = buf + ' ' + line.replace(',', '').replace('\n', '').replace('   ', '')
            line = file.readline()
        if netChangeLine == 1:
            netChangeLine = 0
            buf = buf + ' ' + line.replace(',', '').replace('\n', '').replace('    ', '')
        for i in buf.split():
            if chipDict.get(i, 'noExist') != 'noExist':
                pinToNetDict[i] = netName
                if netMem == '':
                    netMem = i
                else:
                    netMem = netMem + ':' + i
                netData = netData + i + ' ' + chipDict[i] + '\n'
                pinCount = pinCount + 1
        if pinCount >= 2:
            file3.write("NetName " + netName.strip("\'") + '\n')
            pin_list = netData.split('\n')
            file3.write("PIN START\n")
            for p in range(0,len(pin_list)- 1):
                file3.write("\t" + str(pin_list[p]) + '\n')
            file3.write("PIN END\n")
            netDict[netName] = netData
    elif netF==1 and line.find('$')!=-1:
        netF=0
    line=file.readline()
file.close()
file3.close()
#print('Parsing Net information completed')









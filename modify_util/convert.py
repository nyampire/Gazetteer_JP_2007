#!/usr/bin/env python3

import re
import unicodedata
import csv
def dm2dec(dmstr):
    dmstr = dmstr[:-2]
    dm = dmstr.split(" ゚ ")
    #print(dm)   
    dms = int(dm[0]) + float(dm[1])*1.0/60
    return (dms)

def join_diacritic(text, mode="NFC"):
    """
    基底文字と濁点・半濁点を結合
    """
    # str -> bytes
    bytes_text = text.encode()

    # 濁点Unicode結合文字置換
    bytes_text = re.sub(b"\xe3\x82\x9b", b'\xe3\x82\x99', bytes_text)
    bytes_text = re.sub(b"\xef\xbe\x9e", b'\xe3\x82\x99', bytes_text)

    # 半濁点Unicode結合文字置換
    bytes_text = re.sub(b"\xe3\x82\x9c", b'\xe3\x82\x9a', bytes_text)
    bytes_text = re.sub(b"\xef\xbe\x9f", b'\xe3\x82\x9a', bytes_text)

    # bytet -> str
    text = bytes_text.decode()

    # 正規化
    text = unicodedata.normalize(mode, text)

    return text
#
alllist = {}
with open("GAZETTEER_OF_JAPAN_2007.csv") as f:
    reader = csv.reader(f)
    header = next( reader )
    for line in reader:
        "row =(line[:-1]).split(",")"
        alllist[line[0]+line[3]] = line
        #print(join_diacritic(row[3]))
difflist = []
with open("modify_2018.csv") as f:
    reader = csv.reader(f)
    for line in reader:
        #row =(line[:-1]).split(",")
        #print(line[2])
        pos =  line[2][:-1]+line[5][:-1]
        pos2 =  line[8]+line[5][:-1]
        if pos in alllist:
            #print(alllist[line[2][:-1]])
            if len(alllist[pos]) == 8:
                
                alllist[pos].append( line[0])
            else:
                alllist[pos][8] =  line[0]
            if line[6][:-1] != alllist[pos][4] :
                print([line, alllist[pos]])
            if alllist[pos][1] != line[3][:-1]:
                alllist[pos][8] +=  " "+alllist[pos][1]+"から読み変更"
            if alllist[pos][2] != line[4][:-1]:
                alllist[pos][8] +=  " "+alllist[pos][2]+"から英語名変更"
            alllist[pos][1] =  line[3][:-1]
            alllist[pos][2] =  line[4][:-1]
        elif  pos2 in alllist:
            alllist[pos2][0] =  line[2][:-1]
            alllist[pos2][1] =  line[3][:-1]
            alllist[pos2][2] =  line[4][:-1]
            alllist[pos2].append( line[0]+ " "+line[8]+"から名称変更")
            if alllist[pos2][1] != line[3][:-1]:
                alllist[pos2][8] +=  " "+alllist[pos2][1]+"から読み変更"
            if alllist[pos2][2] != line[4][:-1]:
                alllist[pos2][8] +=  " "+alllist[pos2][2]+"から英語名変更"
            #print(alllist[pos2])
        else:
            #print(pos2)
            difflist.append([ line[2][:-1] ,line[3][:-1] ,line[4][:-1] ,line[5][:-1] ,line[6][:-1], "Abolished Municipality", dm2dec(line[5] ),dm2dec(line[6]),line[0] ])
        #print(join_diacritic(row[3]))

header.append("change_information")
with open('GAZETTEER_OF_JAPAN_2007_new.csv','w',newline='') as f:
    writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(header)
    for row in alllist.values():
        row[6] = float(row[6])
        row[7] = float(row[7])
        if len(row) == 8:
            row.append("")
        writer.writerow(row)
    for row in difflist:
        writer.writerow(row)

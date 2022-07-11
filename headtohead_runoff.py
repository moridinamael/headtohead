# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 12:24:30 2021

@author: Matt
"""

import math
import random

fh = open("C:\\Users\\Matt\\Documents\\GitHub\\headtohead\\BooksList.txt","r")
fpast = open("matches01.csv","r")
pastcontents = fpast.readlines()
fpast.close()



fo = open("matches01.csv","a")

contents = fh.readlines()

books = []

for line in contents:
    books.append(line.strip())

print(books)

bookranks = {}

for book in books:
    bookranks[book] = 400
    
def headtohead(pr1,pr2,answer):
    K = 32
    
    R1 = math.pow(10,(pr1/400.))
    R2 = math.pow(10,(pr2/400.))
    
    E1 = R1/(R1+R2)
    E2 = R2/(R1+R2)
    
    S1 = 0
    S2 = 0
    
    if(answer=="1"):
        S1 = 1
    elif(answer=="2"):
        S2 = 1
    else:
        print("Invalid input")
    
    RO1 = pr1 + K * (S1 - E1)
    RO2 = pr2 + K * (S2 - E2)
    
    return RO1,RO2

round_number = 0

for line in pastcontents:
    r,b1,b2,c = line.split(",")
    r = int(r.strip())
    b1 = b1.strip()
    b2 = b2.strip()
    c = c.strip()
    bookranks[b1],bookranks[b2] = headtohead(bookranks[b1],bookranks[b2],c)

round_number = r
for i in range(0,200):
    round_number += 1
    pick1 = random.choice(books)
    pick2 = random.choice(books)
    if(pick1 == pick2):
        pick2 = random.choice(books)
        if(pick1 == pick2):
            pick2 = random.choice(books)
    print(pick1,pick2)
    
    print("Choose:")
    print("1.",pick1)
    print("2.",pick2)
    answer = input()
    
    bookranks[pick1],bookranks[pick2] = headtohead(bookranks[pick1],bookranks[pick2],answer)
    
    print(str(round_number)+","+str(pick1)+","+str(pick2)+","+str(answer),file=fo)
    
    for k in books:
        print(k,":",bookranks[k])
        
    fo.flush()
    
#print(headtohead(500,400,"A","B"))






import matplotlib.pyplot as plt
import numpy as np

def neighbours(y,x):
    return (y-1,x),(y,x-1)

def find(label, links):
    j = label
    while links[j] !=0:
        j = links[j]
    return j 

def union(label1,label2,links):
    j = find(label1,links)
    k = find(label2,links)
    if j != k:
        links[k] = j

def label(binary):
    labeled = binary * -1
    links = np.zeros(labeled.size//2 +1, dtype ='int32')
    label = 0
    for y in range(1,binary.shape[0]-[1]):
        for x in range(1,binary.shape[1]-[1]):
            if labeled[y,x] ==-1:
                n=neighbours(y,x)
                n1 = labeled[n[0]]
                n2 == labeled[n[1]]
                if n1 ==0 and n2 ==0:
                    label +=1
                    lb = label
                elif n1 ==0 or n2 ==0:
                    lb =max([n1,n2])
                else: 
                    lb = min([n1,n2])
                labeled[y,x] = lb
                union(n1,lb,links)
                union(n1,lb,links)
    print(links[:10])
    return labeled
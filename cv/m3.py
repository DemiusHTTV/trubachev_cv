import matplotlib.pyplot as plt
import numpy as np

def neighbours(y,x):
    return (y-1,x),(y,x-1)
def label(binary):
    labeled = binary * -1
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
                    lh =max([n1,n2])
                else: 
                    lb = min([n1,n2])

    return labeled
import matplotlib.pyplot as plt
import numpy as np

def read_file(file):
    file1 = open(file, 'r')
    Lines = file1.readlines()
    arr=[]
    for line in Lines:
        temp=[]
        for word in line.split():
            temp.append(word)
        arr.append(temp)
    return arr

file = "log.txt"
file2 = "traffic.txt"
arr = read_file(file)
arr2 = read_file(file2)

first = 0
final = 0
arr3 = np.zeros((len(arr2)),dtype=np.uint8)
arr4 = np.zeros((len(arr2)),dtype=np.uint8)
for i in range(len(arr2)):
    row=arr2[i]
    src=row[1]
    dest=row[2]
    packet=row[3]
    for j in range(len(arr)):
        if (int(arr[j][1]) == int(arr2[i][0])-1) and arr[j][5] == "Pe"+src and arr[j][7] == src and int(arr[j][3]) == 1:
            first = arr[j][10]
        elif (int(arr[j][1]) == int(arr2[i][0])-1) and arr[j][7] == dest and int(arr[j][3]) == 3:
            final = arr[j][10]
    latency = int(final) - int(first)
    print("Latency for packet "+str(i+1)+" is "+str(latency))
    arr3[i] = latency
    arr4[i] = i+1

plt.bar(arr4,arr3)
plt.xlabel('Packet number')
plt.ylabel('Latency (in cycles)')
plt.title('Latency as a function of packets sent from PE to Detination')
plt.show()


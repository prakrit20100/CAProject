import matplotlib.pyplot as plt

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
arr = read_file(file)

peatoa,pebtob,pectoc,pedtod,atob,btoc,ctod,dtoa = 0,0,0,0,0,0,0,0
for i in range(len(arr)):
    if(arr[i][5]=="PeA" and arr[i][7]=="A"):
        peatoa+=1
    if(arr[i][5]=="PeB" and arr[i][7]=="B"):
        pebtob+=1
    if(arr[i][5]=="PeC" and arr[i][7]=="C"):
        pectoc+=1
    if(arr[i][5]=="PeD" and arr[i][7]=="D"):
        pedtod+=1
    if(arr[i][5]=="A" and arr[i][7]=="B"):
        atob+=1
    if(arr[i][5]=="B" and arr[i][7]=="C"):
        btoc+=1
    if(arr[i][5]=="C" and arr[i][7]=="D"):
        ctod+=1
    if(arr[i][5]=="D" and arr[i][7]=="A"):
        dtoa+=1

plt.bar(['PeA->A','PeB->B','PeC->C','PeD->D','A->B','B->C','C->D','D->A'],[peatoa,pebtob,pectoc,pedtod,atob,btoc,ctod,dtoa])
plt.xlabel('Connections')
plt.ylabel('Number of flits transferred')
plt.title('Flits transferred over different connections')
plt.show()
import numpy as np
import csv


#will get 5000rs
log=open("log.txt","w")

class Router:
    def __init__(self):
        '''self.portN = None
        self.portW = None
        self.portE = None
        self.portS = None
        self.pe = None
        
        self.switchallocator = None
        self.crossbar = None
        self.carryingData = False
        

        '''
        self.buffer = [] # max size is 5
    ''''
    def assignNorthRouter(self, nr):
        self.portN.assignConnection(self,nr)

    def assignSouthRouter(self, sr):
        self.portS.assignConnection(self,sr)

    def assignWestRouter(self, wr):
        self.portW.assignConnection(self,wr)

    def assignEastRouter(self, er):
        self.portE.assignConnection(self,er)

    def assignLocalPE(self,Pe):
        self.pe = Pe
    '''

class Flit:
    def __init__(self,bit,cnt,d,s):
        self.bits=bit
        self.src=s
        self.count=cnt
        self.dest=d

    

'''class PE:
    def __init__(self):
        self.router = None
        self.flits_storage=[]

    def assignRouter(self, r):
        self.router = r

class SwitchAllocator:
    def __init__(self):
        self.router = None

    def assignRouter(self, r):
        self.router = r

class Crossbar:
    def __init__(self):
        self.router = None

    def assignRouter(self, r):
        self.router = r
'''

'''class Port:
    def __init__(self):
        self.x = None
        self.y = None
    def assignConnection(self, X, Y):
        self.x = X
        self.y = Y
    '''

'''class Mesh:
    def __init__(self):
        self.A = Router()
        self.B = Router()
        self.C = Router()
        self.D = Router()
        self.A.assignEastRouter(self.B)
        self.A.assignSouthRouter(self.D)
        self.B.assignWestRouter(self.A)
        self.B.assignSouthRouter(self.C)
        self.C.assignNorthRouter(self.B)
        self.C.assignWestRouter(self.D)
        self.D.assignNorthRouter(self.A)
        self.D.assignEastRouter(self.C)
    '''


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
            

   



    
def transferPackets(traffic_file):
    in_arr=read_file(traffic_file)
    
    cycle_max=int(in_arr[len(in_arr)-1][0])
    i=0
    counter=0
    print(cycle_max)
    while cycle_max>0 or len(A.buffer)>0 or len(B.buffer)>0 or len(C.buffer)>0 or len(D.buffer)>0:
        # if cycle_max>0:
        #print(cycle_max,len(A.buffer),len(B.buffer),len(C.buffer),len(D.buffer))
        if cycle_max>0:
            counter+=1
            row=in_arr[i]
            print(row)
            src=row[1]
            # print(src)
            dest=row[2]
            # print(dest)
            packet=row[3]
            # print(packet)

            f1=Flit(packet[:32],counter,dest,src)
            f2=Flit(packet[32:64],-1,dest,src)
            f3=Flit(packet[64:96],-1,dest,src)

            if src=="A":
                print("`paclket at A",counter)
                A.buffer.append(f1)
                A.buffer.append(f2)
                A.buffer.append(f3)
                

            elif src=="B":
                print("`paclket at b",counter)
                B.buffer.append(f1)
                B.buffer.append(f2)
                B.buffer.append(f3)
            

            elif src=="C":
                print("`paclket at c",counter)
                C.buffer.append(f1)
                C.buffer.append(f2)
                C.buffer.append(f3)

            elif src=="D":
                print("`paclket at d",counter)
                D.buffer.append(f1)
                D.buffer.append(f2)
                D.buffer.append(f3)

        #transfering flits
        #A
        if len(A.buffer)>0:
            print("leaving from a",counter)
            
            flit=A.buffer[0]
            

            if flit.dest=="B":
                print("going to b",counter)
                if flit.count!=-1:
                    log.write("Packet "+str(flit.count)+" from "+ flit.src+ " to "+ flit.dest +" at cycle "+str(i+1)+"\n")
                
                A.buffer.pop(0)

            if flit.dest=="D":
                print("going to d",counter)
                if flit.count!=-1:
                    log.write("Packet "+str(flit.count)+" from "+ flit.src+ " to "+ flit.dest +" at cycle "+str(i+1)+"\n")
                
                A.buffer.pop(0)

            if flit.dest=="C":

                print("going to c",counter)
                B.buffer.append(flit)
                A.buffer.pop(0)



        if len(B.buffer)>0:
            print("leaving from b",counter)
            
            flit=B.buffer[0]
            

            if flit.dest=="A":
                print("going to a",counter)
                if flit.count!=-1:
                    log.write("Packet "+str(flit.count)+" from "+ flit.src+ " to "+ flit.dest +" at cycle "+str(i+1)+"\n")
                
                B.buffer.pop(0)

            if flit.dest=="C":
                
                print("going to c",counter)
                if flit.count!=-1:
                    log.write("Packet "+str(flit.count)+" from "+ flit.src+ " to "+ flit.dest +" at cycle "+str(i+1)+"\n")
                
                B.buffer.pop(0)

            if flit.dest=="D":
                print("going to d",counter)
                C.buffer.append(flit)
                B.buffer.pop(0)


        if len(C.buffer)>0:
            print("leaving from c",counter)
            
            flit=C.buffer[0]
            

            if flit.dest=="B":
                print("going to b",counter)
                if flit.count!=-1:
                    log.write("Packet "+str(flit.count)+" from "+ flit.src+ " to "+ flit.dest +" at cycle "+str(i+1)+"\n")
                
                C.buffer.pop(0)

            if flit.dest=="D":
                print("going to d",counter)
                if flit.count!=-1:
                    log.write("Packet "+str(flit.count)+" from "+ flit.src+ " to "+ flit.dest +" at cycle "+str(i+1)+"\n")
                
                C.buffer.pop(0)

            if flit.dest=="A":
                print("going to a",counter)
                D.buffer.append(flit)
                C.buffer.pop(0)


        if len(D.buffer)>0:
            print("leaving from d")
            flit=D.buffer[0]
            #print(flit.dest)

            if flit.dest=="C":
                print("going to c",counter)
                if flit.count!=-1:
                    log.write("Packet "+str(flit.count)+" from "+ flit.src+ " to "+ flit.dest +" at cycle "+str(i+1)+"\n")
               
                D.buffer.pop(0)


            if flit.dest=="A":
                print("going to a",counter)
                if flit.count!=-1:
                    log.write("Packet "+str(flit.count)+" from "+ flit.src+ " to "+ flit.dest +" at cycle "+str(i+1)+"\n")
                
                D.buffer.pop(0)


            if flit.dest=="B":
                print("going to b",counter)
                A.buffer.append(flit)
                D.buffer.pop(0)


        cycle_max-=1
        i+=1



A=Router()
B=Router()
C=Router()
D=Router()

transferPackets("traffic.txt")

            


            
                    

                


            

            









        


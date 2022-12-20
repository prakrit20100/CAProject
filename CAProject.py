log=open("log.txt","w")

class Port:
    def __init__(self):
        self.x = None
        self.y = None
    def assignConnection(self, X, Y):
        self.x = X
        self.y = Y

class SwitchAllocator:
    def __init__(self,id):
        self.router = id

    def assignRouter(self, r):
        self.router = r
        
    def assignNorthRouter(self, nr):
        self.router.portNinput.assignConnection(self, nr)
        self.router.portNoutput.assignConnection(self, nr)

    def assignSouthRouter(self, sr):
        self.router.portSinput.assignConnection(self, sr)
        self.router.portSoutput.assignConnection(self, sr)

    def assignWestRouter(self, wr):
        self.router.portWinput.assignConnection(self, wr)
        self.router.portWoutput.assignConnection(self, wr)

    def assignEastRouter(self, er):
        self.router.portEinput.assignConnection(self, er)
        self.router.portEoutput.assignConnection(self, er)

    def assignLocalPE(self,Pe):
        self.router.peinput = Pe
        self.router.peoutput = Pe

class Crossbar:
    def __init__(self):
        self.router = None 

    def assignRouter(self, r):
        self.router = r

class Flit:
    def __init__(self,bit,cnt,d,s,n):
        self.bits=bit
        self.src=s
        self.count=cnt
        self.dest=d
        self.number=n

class Router:
    def __init__(self,id):
        self.id = id
        self.portNinput = Port()
        self.portWinput = Port()
        self.portEinput = Port()
        self.portSinput = Port()
        self.peinput = PE()
        self.portNoutput = Port()
        self.portWoutput = Port()
        self.portEoutput = Port()
        self.portSoutput = Port()
        self.peoutput = PE()
        
        self.switchallocator = SwitchAllocator(self)
        self.crossbar = Crossbar()
        self.carryingData = False
        
        self.buffer = [] 

class PE:
    def __init__(self):
        self.router = None
        self.flits_storage=[]

    def assignRouter(self, r):
        self.router = r
    
    def storeFlit(self,flit):
        self.flits_storage.append(flit)

    def popFlit(self):
        return self.flits_storage.pop(0)

class Mesh:
    def __init__(self,A,B,C,D):
        self.pea = PE()
        self.peb = PE()
        self.pec = PE()
        self.ped = PE()
        self.pea.assignRouter(A)
        self.peb.assignRouter(B)
        self.pec.assignRouter(C)
        self.ped.assignRouter(D)
        A.switchallocator.assignRouter(A)
        B.switchallocator.assignRouter(B)
        C.switchallocator.assignRouter(C)
        D.switchallocator.assignRouter(D)
        A.switchallocator.assignEastRouter(B)
        A.switchallocator.assignSouthRouter(D)
        B.switchallocator.assignWestRouter(A)
        B.switchallocator.assignSouthRouter(C)
        C.switchallocator.assignNorthRouter(B)
        C.switchallocator.assignWestRouter(D)
        D.switchallocator.assignNorthRouter(A)
        D.switchallocator.assignEastRouter(C)
        A.switchallocator.assignLocalPE(self.pea)
        B.switchallocator.assignLocalPE(self.peb)
        C.switchallocator.assignLocalPE(self.pec)
        D.switchallocator.assignLocalPE(self.ped)

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

def storeinpe(file,mesh):
    in_arr=read_file(file)
    for i in range(len(in_arr)):
        row=in_arr[i]
        src=row[1]
        dest=row[2]
        packet=row[3]

        f1=Flit(packet[:32],i,dest,src,1)
        f2=Flit(packet[32:64],i,dest,src,2)
        f3=Flit(packet[64:96],i,dest,src,3)
        if src=="A":
            mesh.pea.storeFlit(f1)
            mesh.pea.storeFlit(f2)
            mesh.pea.storeFlit(f3)
        elif src=="B":
            mesh.peb.storeFlit(f1)
            mesh.peb.storeFlit(f2)
            mesh.peb.storeFlit(f3)
        elif src=="C":
            mesh.pec.storeFlit(f1)
            mesh.pec.storeFlit(f2)
            mesh.pec.storeFlit(f3)
        elif src=="D":
            mesh.ped.storeFlit(f1)
            mesh.ped.storeFlit(f2)
            mesh.ped.storeFlit(f3)
    return int(in_arr[len(in_arr)-1][0])
  
def transferPackets(file,routingalgorithm,mesh,A,B,C,D):
    cycle_max=3*storeinpe(file,mesh)
    i=0
    if routingalgorithm == 1:
        while cycle_max>0 or len(mesh.pea.flits_storage)>0 or len(mesh.peb.flits_storage)>0 or len(mesh.pec.flits_storage)>0 or len(mesh.ped.flits_storage)>0:
            if len(mesh.pea.flits_storage)>0 and len(A.buffer)<5:
                A.buffer.append(mesh.pea.flits_storage[0])
                log.write("Packet "+str(mesh.pea.flits_storage[0].count)+" flit "+str(mesh.pea.flits_storage[0].number)+" from PeA to A at cycle "+str(i+1)+"\n")
                mesh.pea.flits_storage.pop(0)
                i+=1
                continue
            if len(mesh.peb.flits_storage)>0 and len(B.buffer)<5:
                B.buffer.append(mesh.peb.flits_storage[0])
                log.write("Packet "+str(mesh.peb.flits_storage[0].count)+" flit "+str(mesh.peb.flits_storage[0].number)+" from PeB to B at cycle "+str(i+1)+"\n")
                mesh.peb.flits_storage.pop(0)
                i+=1
                continue
            if len(mesh.pec.flits_storage)>0 and len(C.buffer)<5:
                C.buffer.append(mesh.pec.flits_storage[0])
                log.write("Packet "+str(mesh.pec.flits_storage[0].count)+" flit "+str(mesh.pec.flits_storage[0].number)+" from PeC to C at cycle "+str(i+1)+"\n")
                mesh.pec.flits_storage.pop(0)
                i+=1
                continue
            if len(mesh.ped.flits_storage)>0 and len(D.buffer)<5:
                D.buffer.append(mesh.ped.flits_storage[0])
                log.write("Packet "+str(mesh.ped.flits_storage[0].count)+" flit "+str(mesh.ped.flits_storage[0].number)+" from PeD to D at cycle "+str(i+1)+"\n")
                mesh.ped.flits_storage.pop(0)
                i+=1
                continue
            if len(A.buffer)>0:
                
                flit=A.buffer[0]
                if flit.dest=="B":
                    
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from A to B at cycle "+str(i+1)+"\n")
                    A.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="D":
                    
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from A to D at cycle "+str(i+1)+"\n")
                    A.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="C":
                    B.buffer.append(flit)
                    A.buffer.pop(0)
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from A to B at cycle "+str(i+1)+"\n")
                    i+=1
                    continue

            if len(B.buffer)>0:
                flit=B.buffer[0]
                if flit.dest=="A":     
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from B to A at cycle "+str(i+1)+"\n")    
                    B.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue 

                if flit.dest=="C":             
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from B to C at cycle "+str(i+1)+"\n")
                    B.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="D":
                    A.buffer.append(flit)
                    B.buffer.pop(0)
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from B to A at cycle "+str(i+1)+"\n")
                    i+=1
                    continue

            if len(C.buffer)>0:                
                flit=C.buffer[0]
                if flit.dest=="B":                  
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from C to B at cycle "+str(i+1)+"\n")
                    C.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="D":    
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from C to D at cycle "+str(i+1)+"\n")
                    C.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="A":
                    D.buffer.append(flit)
                    C.buffer.pop(0)
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from C to D at cycle "+str(i+1)+"\n")
                    i+=1
                    continue

            if len(D.buffer)>0:               
                flit=D.buffer[0]
                if flit.dest=="C":                   
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from D to C at cycle "+str(i+1)+"\n")
                    D.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="A":                   
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from D to A at cycle "+str(i+1)+"\n") 
                    D.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="B":
                    C.buffer.append(flit)
                    D.buffer.pop(0)
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from D to C at cycle "+str(i+1)+"\n")
                    i+=1
                    continue

    if routingalgorithm == 2:
        while cycle_max>0 or len(mesh.pea.flits_storage)>0 or len(mesh.peb.flits_storage)>0 or len(mesh.pec.flits_storage)>0 or len(mesh.ped.flits_storage)>0:
            if len(mesh.pea.flits_storage)>0 and len(A.buffer)<5:
                A.buffer.append(mesh.pea.flits_storage[0])
                log.write("Packet "+str(mesh.pea.flits_storage[0].count)+" flit "+str(mesh.pea.flits_storage[0].number)+" from PeA to A at cycle "+str(i+1)+"\n")
                mesh.pea.flits_storage.pop(0)
                i+=1
                continue
            if len(mesh.peb.flits_storage)>0 and len(B.buffer)<5:
                B.buffer.append(mesh.peb.flits_storage[0])
                log.write("Packet "+str(mesh.peb.flits_storage[0].count)+" flit "+str(mesh.peb.flits_storage[0].number)+" from PeB to B at cycle "+str(i+1)+"\n")
                mesh.peb.flits_storage.pop(0)
                i+=1
                continue
            if len(mesh.pec.flits_storage)>0 and len(C.buffer)<5:
                C.buffer.append(mesh.pec.flits_storage[0])
                log.write("Packet "+str(mesh.pec.flits_storage[0].count)+" flit "+str(mesh.pec.flits_storage[0].number)+" from PeC to C at cycle "+str(i+1)+"\n")
                mesh.pec.flits_storage.pop(0)
                i+=1
                continue
            if len(mesh.ped.flits_storage)>0 and len(D.buffer)<5:
                D.buffer.append(mesh.ped.flits_storage[0])
                log.write("Packet "+str(mesh.ped.flits_storage[0].count)+" flit "+str(mesh.ped.flits_storage[0].number)+" from PeD to D at cycle "+str(i+1)+"\n")
                mesh.ped.flits_storage.pop(0)
                i+=1
                continue
            if len(A.buffer)>0:               
                flit=A.buffer[0]
                if flit.dest=="B":                   
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from A to B at cycle "+str(i+1)+"\n")
                    A.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="D":                   
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from A to D at cycle "+str(i+1)+"\n")
                    A.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="C":                      
                    D.buffer.append(flit)
                    A.buffer.pop(0)
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from A to D at cycle "+str(i+1)+"\n")
                    i+=1
                    continue

            if len(B.buffer)>0:               
                flit=B.buffer[0]
                if flit.dest=="A":                   
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from B to A at cycle "+str(i+1)+"\n")    
                    B.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue 

                if flit.dest=="C":             
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from B to C at cycle "+str(i+1)+"\n")
                    B.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="D":                       
                    C.buffer.append(flit)
                    B.buffer.pop(0)
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from B to C at cycle "+str(i+1)+"\n")
                    i+=1
                    continue

            if len(C.buffer)>0:                
                flit=C.buffer[0]
                if flit.dest=="B":                   
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from C to B at cycle "+str(i+1)+"\n")
                    C.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="D":                   
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from C to D at cycle "+str(i+1)+"\n")
                    C.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="A":     
                    B.buffer.append(flit)
                    C.buffer.pop(0)
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from C to B at cycle "+str(i+1)+"\n")
                    i+=1
                    continue
                    
            if len(D.buffer)>0:                
                flit=D.buffer[0]
                if flit.dest=="C":                   
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from D to C at cycle "+str(i+1)+"\n")
                    D.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="A":                    
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from D to A at cycle "+str(i+1)+"\n") 
                    D.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="B":                   
                    A.buffer.append(flit)
                    D.buffer.pop(0)
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from D to A at cycle "+str(i+1)+"\n")
                    i+=1
                    continue

    if routingalgorithm == 3:
        while cycle_max>0 or len(mesh.pea.flits_storage)>0 or len(mesh.peb.flits_storage)>0 or len(mesh.pec.flits_storage)>0 or len(mesh.ped.flits_storage)>0:
            if len(mesh.pea.flits_storage)>0 and len(A.buffer)<5:
                A.buffer.append(mesh.pea.flits_storage[0])
                log.write("Packet "+str(mesh.pea.flits_storage[0].count)+" flit "+str(mesh.pea.flits_storage[0].number)+" from PeA to A at cycle "+str(i+1)+"\n")
                mesh.pea.flits_storage.pop(0)
                i+=1
                continue
            if len(mesh.peb.flits_storage)>0 and len(B.buffer)<5:
                B.buffer.append(mesh.peb.flits_storage[0])
                log.write("Packet "+str(mesh.peb.flits_storage[0].count)+" flit "+str(mesh.peb.flits_storage[0].number)+" from PeB to B at cycle "+str(i+1)+"\n")
                mesh.peb.flits_storage.pop(0)
                i+=1
                continue
            if len(mesh.pec.flits_storage)>0 and len(C.buffer)<5:
                C.buffer.append(mesh.pec.flits_storage[0])
                log.write("Packet "+str(mesh.pec.flits_storage[0].count)+" flit "+str(mesh.pec.flits_storage[0].number)+" from PeC to C at cycle "+str(i+1)+"\n")
                mesh.pec.flits_storage.pop(0)
                i+=1
                continue
            if len(mesh.ped.flits_storage)>0 and len(D.buffer)<5:
                D.buffer.append(mesh.ped.flits_storage[0])
                log.write("Packet "+str(mesh.ped.flits_storage[0].count)+" flit "+str(mesh.ped.flits_storage[0].number)+" from PeD to D at cycle "+str(i+1)+"\n")
                mesh.ped.flits_storage.pop(0)
                i+=1
                continue
            if len(A.buffer)>0:               
                flit=A.buffer[0]
                if flit.dest=="B":                   
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from A to B at cycle "+str(i+1)+"\n")
                    A.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="D":                   
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from A to D at cycle "+str(i+1)+"\n")
                    A.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="C":
                    if(len(B.buffer)==5):                        
                        D.buffer.append(flit)
                        A.buffer.pop(0)
                        log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from A to D at cycle "+str(i+1)+"\n")
                        i+=1
                        continue
                    else:                       
                        B.buffer.append(flit)
                        A.buffer.pop(0)
                        log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from A to B at cycle "+str(i+1)+"\n")
                        i+=1
                        continue

            if len(B.buffer)>0:                
                flit=B.buffer[0]
                if flit.dest=="A":                    
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from B to A at cycle "+str(i+1)+"\n")    
                    B.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue 

                if flit.dest=="C":                   
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from B to C at cycle "+str(i+1)+"\n")
                    B.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="D":
                    if(len(A.buffer)==5):                        
                        C.buffer.append(flit)
                        B.buffer.pop(0)
                        log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from B to C at cycle "+str(i+1)+"\n")
                        i+=1
                        continue
                    else:                       
                        A.buffer.append(flit)
                        B.buffer.pop(0)
                        log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from B to A at cycle "+str(i+1)+"\n")
                        i+=1
                        continue

            if len(C.buffer)>0:                
                flit=C.buffer[0]
                if flit.dest=="B":                    
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from C to B at cycle "+str(i+1)+"\n")
                    C.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="D":                    
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from C to D at cycle "+str(i+1)+"\n")
                    C.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="A":
                    if(len(D.buffer)==5):                        
                        B.buffer.append(flit)
                        C.buffer.pop(0)
                        log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from C to B at cycle "+str(i+1)+"\n")
                        i+=1
                        continue
                    else:                        
                        D.buffer.append(flit)
                        C.buffer.pop(0)
                        log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from C to D at cycle "+str(i+1)+"\n")
                        i+=1
                        continue

            if len(D.buffer)>0:              
                flit=D.buffer[0]
                if flit.dest=="C":                    
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from D to C at cycle "+str(i+1)+"\n")
                    D.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="A":                   
                    log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from D to A at cycle "+str(i+1)+"\n") 
                    D.buffer.pop(0)
                    cycle_max-=1
                    i+=1
                    continue

                if flit.dest=="B":
                    if(len(C.buffer)==5):       
                        A.buffer.append(flit)
                        D.buffer.pop(0)
                        log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from D to A at cycle "+str(i+1)+"\n")
                        i+=1
                        continue
                    else:
                        C.buffer.append(flit)
                        D.buffer.pop(0)
                        log.write("Packet "+str(flit.count)+" flit "+str(flit.number)+" from D to C at cycle "+str(i+1)+"\n")
                        i+=1
                        continue

def main():
    A = Router('A')
    B = Router('B')
    C = Router('C')
    D = Router('D')
    print("Enter routing type: ")
    print("Enter 1 for XY routing")
    print("Enter 2 for YX routing")
    print("Enter 3 for Combination of XY and YX routing(utilising both XY and YX routing algorithms in a greedy way)")
    routingtype = int(input())
    mesh = Mesh(A,B,C,D)
    transferPackets("traffic.txt",routingtype,mesh,A,B,C,D)

if __name__ == "__main__":
  main()
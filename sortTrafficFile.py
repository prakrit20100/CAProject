
def SortTrafficFile(src):
    MyDict = dict()
    infile = open(src,'r')
    while True:
        line = infile.readline()
        
        if not line:
            break
        details = dict()


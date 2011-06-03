#python

def makeRList(file):
    a = open(file,'rb')
    rlist = []
    for eachline in a:
        b = eachline.strip().split('@')
        c = tuple(b)
        rlist.append(c)
    a.close()
    return rlist

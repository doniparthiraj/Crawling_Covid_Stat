import sys
filename = sys.argv[1]



months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
# print(filename)
y = filename.split("/")[3]
print(y)
try:
    fp = open(filename,'r')
    data = fp.read()
    data = data.split("\n")
    for i in data:
        i=i.strip()
        # print(i)
        if(len(i)>0 and len(i)<20):
            # print(i)
            i= i.strip("...")
            # print(i.split(" ")[1])
            if(" " in i):
                m = str(months.index(i.split(" ")[1])+1)
                m = m.rjust(2,"0")
                d = str(i.split(" ")[0])
                d = d.rjust(2,"0")
                print("..."+d+"-"+m+"-"+str(y)+"...")
        else:
            print(i)
    
    fp.close()

except  IOError as e:
    pass
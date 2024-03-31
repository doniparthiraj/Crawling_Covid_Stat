import sys

attribues=['Totalcases','Activecases','Totaldeaths','Totalrecovered','Totaltests','DeathsPer1M','TestsPer1M','Newcases','Newdeaths','Newrecovered']
country_data=[]
world_data=[]
for line in sys.stdin:
    line=line.strip()
    line=line.split('-')
    if line[0]=='World':
        for i in line:
            world_data.append(i)
    else:
        for i in line:
            country_data.append(i)

for i in range(len(attribues)):
    print(f"{attribues[i]}---{country_data[i+1]}")

print('\n\n\n')
print('percent in change w.r.t world cases:\n')


for i in range(len(attribues)):
    if world_data[i+1]=='N/A':
        a=0
    else:
        val=world_data[i+1].replace(',','')
        a=float(val)
    
    if country_data[i+1]=='N/A':
        b=0
    else:
        val=country_data[i+1].replace(',','')
        b=float(val)
    
    c=b/a if a !=0 else 0
    print(f"{attribues[i]}---{c*100}")
     













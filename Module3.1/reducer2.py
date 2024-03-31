import sys

min=float('inf')
i=0
countrydata=[]
tempdata=[]
for line in sys.stdin:
    if i==0:
        line=line.strip()
        line=line.split('-')
        last_four_values = line[-4:]

        for value in last_four_values:
            countrydata.append(float(value))
        

        print(line[0])
        closest_country=line[0]
        print('change in active cases in %',countrydata[0])
        print('change in daily deaths in %',countrydata[1])
        print('change in new recovered in %',countrydata[2])
        print('change in new cases in %',countrydata[3])
        i=1

    else:
        line=line.strip()
        line=line.split('-')
        last_four_values = line[-4:]
        for value in last_four_values:
            tempdata.append(float(value))

        for i in range(4):
            val=abs(tempdata[i]-countrydata[i])
            if val==0:
                closest_country=line[0]
                print('Closest country similar to any query is')
                print(f"{closest_country} for Query {i+1}")
                exit()
            
            elif val<min:
                min=val
                closest_country=line[0]
        tempdata.clear()
    
print('Closest country similar to any query is')
print(closest_country,i)     

            




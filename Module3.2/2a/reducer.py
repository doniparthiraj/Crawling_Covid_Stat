import sys
from datetime import datetime


start_date = sys.argv[1]
end_date = sys.argv[2]



def is_date_in_range(start_date_str, end_date_str, check_date_str):
    # print(start_date_str, end_date_str, check_date_str)
    start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
    end_date = datetime.strptime(end_date_str, "%d-%m-%Y")
    check_date = datetime.strptime(check_date_str, "%d-%m-%Y")

    return start_date <= check_date <= end_date

for line in sys.stdin:
    line=line.strip()
    flag=0
    i = line
    # print(i)
    date1 = i.strip("...")
    date1 = date1.strip()
    if(i.startswith("...") and i.endswith("...") and "Background" not in i):    
        if(is_date_in_range( start_date, end_date,date1)):
            # print(i)
            flag=1
                        
            for line in sys.stdin:
                line=line.strip()
                flag=0
                i = line
                # print(i)
                date1 = i.strip("...")
                date1 = date1.strip()
                if(i.startswith("...") and i.endswith("...") and "Background" not in i):    
                    if(is_date_in_range( start_date, end_date,date1)):
                        print(i)
                        continue
                    else:
                        break
                print(i)
    # else:
    #     print(i)
    # else:
    #     print(i)
    #     # print(i)
    #     date1 = i.strip("...")
    #     date1 = date1.strip()
    #     if(is_date_in_range( start_date, end_date,date1)):
    #         print(i)
    #         flag=1
    # elif(flag==1):
    #     print(i)
    #     flag=0
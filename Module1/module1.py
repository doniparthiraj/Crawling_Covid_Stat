import ply.lex as lex
import ply.yacc as yacc
from urllib.request import Request, urlopen
import html
import re
from module1_sub import Extract_data
id = 0
query = None
countries_url = {}
def extract_countries(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()     
    countries = []
    continents = []
    for line in lines:
        line = line.strip()
        if line.endswith(':'):
            continents.append(line[:-1])
        elif line and not line.startswith('-'):
            countries.append(line)
    
    return continents,countries

file_path = 'countrylist.txt'
continents, countries = extract_countries(file_path)


total_data = {}
for country in countries:
    total_data[country] = {i: None for i in range(1, 23)}
for cont in continents:
    total_data[cont] = {i: None for i in range(1, 23)}
total_data['World'] = {i: None for i in range(1, 23)}

# print(list(total_data.keys()))

###DEFINING TOKENS###
tokens = ('OPENTABLE', 'CLOSETABLE', 'OPENROW', 'CLOSEROW',
          'OPENHEAD','CLOSEHEAD','OPENHEADER', 'CLOSEHEADER', 
          'OPENHREF', 'CLOSEHREF','CONTENT', 'OPENDATA', 'CLOSEDATA' ,
          'OPENBODY','CLOSEBODY','OPENDIV','CLOSEDIV', 'BEGINTABLE')

def t_BEGINTABLE(t):
    r'<table.id="main_table_countries_yesterday".class="table.table-bordered.table-hover.main_table_countries".style="width:100%;margin-top:.0px.!important;display:none;">'
    return t

def t_OPENTABLE(t):
    r'<table[^>]*>'
    return t

def t_CLOSETABLE(t):
    r'</table[^>]*>'
    return t

def t_OPENDIV(t):
    r'<div[^>]*>'
    return t

def t_CLOSEDIV(t):
    r'</div[^>]*>'
    return t

def t_OPENHEAD(t):
    r'<thead[^>]*>'
    return t

def t_CLOSEHEAD(t):
    r'</thead[^>]*>'
    return t

def t_OPENBODY(t):
    r'<tbody[^>]*>'
    return t

def t_CLOSEBODY(t):
    r'</tbody[^>]*>'
    return t

def t_OPENROW(t):
    r'<tr[^>]*>'
    return t

def t_CLOSEROW(t):
    r'</tr[^>]*>'
    return t

def t_OPENHEADER(t):
    r'<th[^>]*>'
    return t

def t_CLOSEHEADER(t):
    r'</th[^>]*>'
    return t

def t_OPENHREF(t):
    r'<a[^>]*>'
    return t

def t_CLOSEHREF(t):
    r'</a[^>]*>'
    return t

def t_OPENDATA(t):
    r'<td[^>]*>'
    return t

def t_CLOSEDATA(t):
    r'</td[^>]*>'
    return t

def t_CONTENT(t):
    r'[A-Za-z0-9, ()\/#;\.\-–]+'
    return t

def t_error(t):
    t.lexer.skip(1)

#GRAMMAR
def p_start(p):
    '''
    start : st
    '''

def p_skipcontent(p):
    '''
    skipcontent : CONTENT skipcontent
                | '''

def p_handledata(p):
    '''
    handledata : OPENDATA CLOSEDATA skipcontent
               | OPENDATA CONTENT CLOSEDATA skipcontent
               | OPENDATA CONTENT CONTENT CLOSEDATA skipcontent
               | OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA skipcontent
               | OPENDATA OPENHREF CONTENT CONTENT CLOSEHREF CLOSEDATA skipcontent
    '''

    global id
    global query
    id += 1
    if id == 23:
        id = 1
        query = None
        # print(end = '\n')
    if id == 2:
        # print(len(p))
        if len(p) == 7:
            x = p[3]
            # print(x)
            if x in list(total_data.keys()):
                link = p[2]
                pattern = r'href="([^"]*)"'
                match = re.search(pattern, link)
                url = "https://www.worldometers.info/coronavirus/"
                if match:
                    href_value = match.group(1)
                    extract_url = url + href_value
                    # print("Extracted href value:", extract_url)
                global countries_url
                countries_url[x] = extract_url
                query = x
        if len(p) == 5:
            x = p[2]
            if x in list(total_data.keys()):
                query = x

    if len(p) == 5 and (3 <= id <= 9 or 12 <= id <= 14):
        if query is not None:
            total_data[query][id] = p[2]
        # else:
        #     print(p[2],end = "\t")
    # elif len(p) == 6:
    #     print(p[2],p[3],end = "\t")
    # elif len(p) == 8:
    #     print(p[3],p[4],end = "\t")


def p_skipheaders(p):
    '''
    skipheaders : OPENHEADER CONTENT CLOSEHEADER skipheaders
                | OPENHEADER CONTENT CONTENT CLOSEHEADER skipheaders
                | '''


def p_printhandledata(p):
    '''
    printhandledata : handledata printhandledata
                    | '''

def p_handlerow(p):
    '''
    handlerow : OPENROW printhandledata CLOSEROW skipcontent handlerow
              | '''

def p_st(p):
    '''
    st : BEGINTABLE OPENHEAD OPENROW skipheaders CLOSEROW CLOSEHEAD OPENBODY handlerow CLOSEBODY
       | '''

def p_error(p):
    print(p.lineno,p.value)

def page_download(url,name):
    req = Request(url,headers = {'User-Agent':'Mozilla/5.0'})
    page = urlopen(req).read()
    data = page.decode("utf-8")
    f = open(name,'w',encoding = "utf-8")
    f.write(data)
    f.close
    return data

def t_OPENSPAN(t):
    r'<span[^>]*>'
    return t
 
def t_CLOSESPAN(t):
    r'</span[^>]*>'
    return t

def clean_page_data(data):
    data = re.sub(r'\s{2,}', '', data)
    data = re.sub(r'\n\s*\n', '\n', data)
    data = re.sub(r'<br\s?\/?>','',data)
    data = re.sub(r'<nobr[^>]*>','',data)
    data = re.sub(r'</nobr[^>]*>','',data)
    data = re.sub(r'<span[^>]*>','',data)
    data = re.sub(r'</span[^>]*>','',data)
    data = re.sub(r'<sup[^>]*>','',data)
    data = re.sub(r'</sup[^>]*>','',data)
    return data

def main():
    base_url = 'https://www.worldometers.info/coronavirus/'
    name = "webpage.html"
    x_data = page_download(base_url,name)
    data = clean_page_data(x_data)
    lexer = lex.lex()
    lexer.input(data)
    # with open("tokens.txt", "w") as output_file:
    #     while True:
    #         token = lexer.token()
    #         if not token:
    #             break
    #         output_file.write(str(token) + "\n")
    parser = yacc.yacc()
    parser.parse(data)
    index = {'no':1,'name':2,'Totalcases':3,'Newcases':4,'Totaldeaths':5,'Newdeaths':6,'Totalrecovered':7,'Newrecovered':8,
    'Activecases':9,'seriouscritical':10,'TotCasesPer1M':11,'DeathsPer1M':12,'Totaltests':13,'TestsPer1M':14,'Population':15}

    all_query = ['Totalcases','Activecases','Totaldeaths','Totalrecovered','Totaltests','DeathsPer1M','TestsPer1M',
    'Newcases','Newdeaths','Newrecovered']

    country_query = ['Activecases','Newdeaths','Newrecovered','Newcases']

    global total_data
    # Writing to all_info.txt
    with open('all_info.txt', 'w') as all_info_file:
        all_info_file.write('Name\t')
        for x in all_query:
            all_info_file.write(x + '\t')
        all_info_file.write('\n')

        for x in list(total_data.keys()):
            all_info_file.write(x + '\t')
            for q in all_query:
                val = total_data[x][index[q]]
                if val is None:
                    all_info_file.write('N/A\t')
                else:
                    all_info_file.write("{:<12}".format(str(val)) + '\t')
            all_info_file.write('\n')

    # Writing to countries_info.txt
    # with open('countries_info.txt', 'w') as countries_info_file:
    #     countries_info_file.write('Name\t')
    #     for x in country_query:
    #         countries_info_file.write(x + '\t')
    #     countries_info_file.write('\n')

    #     for x in countries:
    #         countries_info_file.write(x + '\t')
    #         for q in country_query:
    #             val = total_data[x][index[q]]
    #             if val is None:
    #                 countries_info_file.write('N/A\t')
    #             else:
    #                 countries_info_file.write("{:<12}".format(str(val)) + '\t')
    #         countries_info_file.write('\n')

    Extract_data(countries_url)

if __name__ == '__main__':
	main()


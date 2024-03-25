import ply.lex as lex
import ply.yacc as yacc
from urllib.request import Request, urlopen
import html
import re
import os

dates = []
active = []
deaths = []
newcases = []
recover = []

###DEFINING TOKENS###
tokens = ('OPENTABLE', 'CLOSETABLE', 'OPENROW', 'CLOSEROW',
          'OPENHEAD','CLOSEHEAD','OPENHEADER', 'CLOSEHEADER', 
          'OPENHREF', 'CLOSEHREF','CONTENT', 'OPENDATA', 'CLOSEDATA' ,
          'OPENBODY','CLOSEBODY','OPENDIV','CLOSEDIV', 'ACTIVE','CATEGOR',
          'DEATHS', 'NEWCASES','RECOVERED','LINE')

def t_ACTIVE(t):
    r'text:.\'Active.Cases\''
    return t

def t_CATEGOR(t):
    r'categories:'
    return t

def t_DEATHS(t):
    r'text:.\'Daily.Deaths\''
    return t

def t_NEWCASES(t):
    r'text:.\'Daily.New.Cases\''
    return t

def t_RECOVERED(t):
    r"name:.'New.Recoveries',"
    return t

def t_LINE(t):
    r',lineWidth:.(\d+),'
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
    r'[A-Za-z0-9, \[\]()/;.:\-"]+'
    return t

def t_error(t):
    #print(t)
    t.lexer.skip(1)


def p_start(p):
    ''' 
    start : active
          | deaths
          | newcases
          | recover
    '''

def p_skipcontent(p):
    '''
    skipcontent : CONTENT skipcontent
                | CONTENT '''

def p_active(p):
    '''
    active : ACTIVE skipcontent CATEGOR CONTENT skipcontent LINE CONTENT
    '''
    global dates
    global active
    if len(dates) == 0:
        x=p[4]
        pattern = r'"([^"]+)"'
        dates = re.findall(pattern, x)
    values = r'-?\d+'
    active = re.findall(values, p[7])
    # active = [int(num) for num in numbers]

def p_deaths(p):
    '''
    deaths : DEATHS skipcontent CATEGOR CONTENT skipcontent LINE CONTENT
    '''
    global dates
    global deaths
    if len(dates) == 0:
        x=p[4]
        pattern = r'"([^"]+)"'
        dates = re.findall(pattern, x)
    values = r'-?\d+'
    deaths = re.findall(values, p[7])
    # deaths = [int(num) for num in numbers]
    

def p_newcases(p):
    '''
    newcases : NEWCASES skipcontent CATEGOR CONTENT skipcontent LINE CONTENT
    '''
    global dates
    global newcases
    if len(dates) == 0:
        x=p[4]
        pattern = r'"([^"]+)"'
        dates = re.findall(pattern, x)
    values = r'-?\d+'
    newcases = re.findall(values, p[7])
    # newcases = [int(num) for num in numbers]

def p_recover(p):
    '''
    recover : RECOVERED skipcontent LINE CONTENT
    '''
    global recover
    values = r'-?\d+'
    recover = re.findall(values, p[4])
    # recover = [int(num) for num in numbers]


def p_error(p):
    pass  


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

def page_download(url,name,dr):
    req = Request(url,headers = {'User-Agent':'Mozilla/5.0'})
    page = urlopen(req).read()
    data = page.decode("utf-8")
    f = open(f'country_info/{dr}/{name}','w',encoding = "utf-8")
    f.write(data)
    f.close
    return data

def Extract_data(countries_url):
    if not os.path.exists('country_info'):
        os.makedirs('country_info')
    while(True):
        c = input('Enter Country name or Exit to quit\n')
        if c == 'Exit':
            break
        if c not in list(countries_url.keys()):
            print("Incorrect country nme enter valid name ")
            continue
        mp = {c : countries_url[c]}
        for cname, base_url in mp.items():
            if not os.path.exists(f'country_info/{cname}'):
                os.makedirs(f'country_info/{cname}')
            name = f"{cname}.html"
            x_data = page_download(base_url, name, cname)
            data = clean_page_data(x_data)

            # Tokenize manually
            lexer = lex.lex()
            lexer.input(data)
            # with open(f"{cname}/{cname}_tokens.txt", "w") as output_file:
            #     for token in lexer:
            #         output_file.write(str(token) + "\n")
            parser = yacc.yacc()
            parser.parse(data)
            global dates
            global active
            global deaths
            global newcases
            global recover
            with open(f'country_info/{cname}/{cname}.txt','w') as f:
                f.write('Dates\tActive\tDeaths\tNewcases\trecover\n')
                max_len = len(dates)
                for i in range(0,max_len):
                    date = dates[i] if i < len(dates) else 'NA'
                    act = active[i] if i < len(active) else 'NA'
                    death = deaths[i] if i < len(deaths) else 'NA'
                    new = newcases[i] if i < len(newcases) else 'NA'
                    rec = recover[i] if i < len(recover) else 'NA'
                    f.write(f'{date}\t{act}\t{death}\t{new}\t{rec}\n')


import ply.lex as lex
import ply.yacc as yacc
from urllib.request import Request, urlopen  
###DEFINING TOKENS###
tokens = ('BEGINTABLE','ENDTABLE', 'OPENLI','CLOSELI','OPENHREF','CLOSEHREF',
'CONTENT','GARBAGE')

t_ignore = ' \t\n'
# lis to store all the values
lis = []
filep = open("timeline_links.txt","w")
###############Tokenizer Rules################
def t_BEGINTABLE(t):
     r'<span.class="mw-headline".id="Worldwide_timelines_by_month_and_year">Worldwide.timelines.by.month.and.year'
     return t

def t_ENDTABLE(t):
     r'<dt>Responses</dt>'
     return t
def t_OPENLI(t):
    r'<li[^>]*>'
    return t
 
def t_CLOSELI(t):
    r'</li>'
    return t

def t_OPENHREF(t):
    r'<a[^>]*>'
    return t
 
def t_CLOSEHREF(t):
    r'</a>'
    return t

def t_GARBAGE(t):
    r"(<[^>]*> | &nbsp; | &\#160;)"
    # print(t.value,len(t.value))
    t.lexer.skip(0)

def t_CONTENT(t):
    r'[A-Za-z0-9 \.\–\/]+'
    return t



def t_error(t):
    t.lexer.skip(1)
####################################################################################################################################################################################################
                                            #GRAMMAR RULES
def p_start(p):
    '''start : table'''
    p[0] = p[1]

def p_skiptag(p):
    '''skiptag : content skiptag
               | GARBAGE skiptag
               | OPENLI skiptag
               | CLOSELI skiptag
               | OPENHREF skiptag
               | CLOSEHREF skiptag
               | empty 

      '''

def p_handlehref(p):
    '''handlehref : OPENHREF content CLOSEHREF handlehref
                  
                  |

    '''
    if(len(p)>1):
        p[0] = p[1]
def p_skiphref(p):
    '''skiphref : OPENHREF content CLOSEHREF skiphref
                  | content skiphref
                  |
    '''
    # if(len(p)==5):
    #     print("Ads",p[1])

def p_handlelist(p):
    '''handlelist : OPENLI handlehref CLOSELI handlelist
                  | OPENLI handlelist CLOSELI handlelist
                  | OPENLI content handlelist CLOSELI handlelist
                  | content handlelist
                  |
    '''
    if(len(p)== 5):
        # print(p[2])
        filep.write(str(p[2])+"\n")
    # print(len(p))



def p_table(p):
    '''table : skiptag BEGINTABLE skiphref handlelist ENDTABLE skiptag '''

 
def p_empty(p):
    '''empty :'''
    pass
 
def p_content(p):
    '''content : CONTENT content
               | empty'''
    if(len(p)==3):
        p[0] = str(p[1])+str(p[2])
    else:
        p[0] = ""
 
def p_error(p):
    print("\n\n\n\n\nerror....",p)
    pass
 
#########DRIVER FUNCTION#######
def main():
    link = f"https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic"
    req = Request(link,headers ={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(req).read()
    mydata = webpage.decode("utf8")
    f=open('webpage.html','w',encoding="utf-8")
    f.write(mydata)
    f.close 

    print("fetching data.... Please wait....")
    file_obj= open('webpage.html','r',encoding="utf-8")
    data=file_obj.read()
    fp = open("lextokens.txt","w")
    lexer = lex.lex()
    lexer.input(data)
    for tok in lexer:
        try:
            fp.write(str(tok)+"\n")
        except:
            pass
    fp.close()
    parser = yacc.yacc()
    parser.parse(data)
    file_obj.close()
if __name__ == '__main__':
    main()
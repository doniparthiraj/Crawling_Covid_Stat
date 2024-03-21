import ply.lex as lex
import ply.yacc as yacc
from urllib.request import Request, urlopen  
import os 





###DEFINING TOKENS###
tokens = ('BEGINTABLE', 'H3SPAN','H2SPAN',
'CONTENT','GARBAGE','ENDTABLE')

t_ignore = ' \t\n'

# lis to store all the values
dic = {}

global filep
filep = None
# filep = open(path+"2023.txt","w")
###############Tokenizer Rules################
def t_BEGINTABLE(t):
    r'<h1.id="firstHeading".class="firstHeading.mw-first-heading'
    return t

def t_ENDTABLE(t):
     r'<span.class="mw-headline".id="See_also">'
     return t

def t_H2SPAN(t):
    r'<h2><span.class="mw-headline"[^>]*>'
    return t

# def t_CLOSESPAN(t):
#     r'</span>'
#     return t

def t_H3SPAN(t):
    r'<span.class="mw-headline".id="[^>]*>'
    return t

# def t_OPENUL(t):
#     r'<ul>'
#     return t 
# def t_CLOSEUL(t):
#     r'</ul>'
#     return t

def t_GARBAGE(t):
    r"(<[^>]*> | /\[[a-z0-9A-Z]*] | &nbsp; | &\#160;| edit)"
    # print(t.value,len(t.value))
    t.lexer.skip(0)

def t_CONTENT(t):
    r'[A-Za-z0-9 \,\.\–]+'
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
               | H2SPAN skiptag
               | H3SPAN skiptag
               | empty 

      '''


    

def p_handleh2span(p):
    '''handleh2span : H2SPAN CONTENT content 
                    | H2SPAN content
                '''
    
    # print(f"....{p[2]}....")
    if(len(p)==4):
        filep.write(f"....{p[2]}....\n")
        filep.write(f"....{p[3]}....\n")
        # print(p[2])
        # print(p[3])
    if(len(p)==3):
        # print(p[2])
        filep.write(f"....{p[2]}....\n")
    # global filep
   
  
    # filep = open(path+f"{p[2]}.txt","w")

def p_handleh4span(p):
    '''handleh4span : H3SPAN CONTENT content'''
    
    # print(f"....{p[2]}....")
    # print(p[3])
    global filep
    filep.write(p[2]+"\n")
    filep.write(p[3]+"\n")

def p_handledata(p):
    '''handledata : handleh2span handleh4span 
                | handleh2span 
                | handleh4span
                        
    '''
    # print()
    filep.write("\n")
    

def p_handlehead(p):
    '''handlehead :  handledata handlehead
                  
                  |
    '''
    



def p_table(p):
    '''table : skiptag  BEGINTABLE content handlehead ENDTABLE skiptag'''

 
def p_empty(p):
    '''empty :'''
    pass
 
def p_content(p):
    '''content : CONTENT content
               | empty'''
    if(len(p)==3):
        p[0] = str(p[1])+str(p[2])
    else:
       
        p[0]=""
    
 
def p_error(p):
    # print("\n\n\n\n\nerror....",p)
    pass
 
#########DRIVER FUNCTION#######
def main(link,path1):
    print(link)
    # # Check if the directory already exists
    # if not os.path.exists(path1):
    #     # If not, create the directory
    #     os.makedirs(path1)
    global filep
    # path = path1+"/"
    filep = open(path1+".txt","w")
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


# main("https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_India_(January%E2%80%93May_2020)","india")
# main("https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Australia_(2022)","australia")
import ply.lex as lex
import ply.yacc as yacc
from urllib.request import Request, urlopen  
import os
# import get_data_2023
import get_data_2020_response




###DEFINING TOKENS###
tokens = ('BEGINTABLE', 'OPENPARA','CLOSEPARA','OPENHEAD','CLOSEHEAD',
'CONTENT','GARBAGE','ENDTABLE')

t_ignore = ' \t\n'
# lis to store all the values
lis = []


filep = open("2019.txt","w")
###############Tokenizer Rules################
def t_BEGINTABLE(t):
    r'<span.class="mw-headline".id="Unconfirmed_reports_of_early_cases">Unconfirmed.reports.of.early.cases</span>'
    return t

def t_ENDTABLE(t):
     r'<span.class="mw-headline".id="See_also">See.also'
     return t
def t_OPENPARA(t):
    r'<p[^>]*>'
    return t
 
def t_CLOSEPARA(t):
    r'</p>'
    return t

def t_OPENHEAD(t):
    r'<h2[^>]*>'
    return t
 
def t_CLOSEHEAD(t):
    r'</h2>'
    return t

def t_GARBAGE(t):
    r"(<[^>]*> | &nbsp; | &\#160;)"
    # print(t.value,len(t.value))
    t.lexer.skip(0)

def t_CONTENT(t):
    r'[A-Za-z0-9 \,\.\–\/]+'
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
               | OPENPARA skiptag
               | CLOSEPARA skiptag
               | OPENHEAD skiptag
               | CLOSEHEAD skiptag
               | empty 

      '''

def p_skiptag1(p):
    '''skiptag1 : content skiptag1
               | GARBAGE skiptag1
               | OPENPARA skiptag1
               | CLOSEPARA skiptag1
               
               | CLOSEHEAD skiptag1
               | empty 

      '''
def p_printpara(p):
    '''printpara : OPENPARA content CLOSEPARA'''
    # print(p[2])
    filep.write(f"{p[2]}\n")
    
def p_handlepara(p):
    '''handlepara :  printpara handlepara
                  
                  |

    '''
    if(len(p)==3):
        p[0]=p[1]

def p_printhead(p):
    '''printhead : OPENHEAD content CLOSEHEAD'''
    if(p[2]):
        # print(f"....{p[2]}....")
        filep.write(f"....{p[2]}....\n")

def p_handlehead(p):
    '''handlehead : printhead content printpara handlehead
                  | printpara handlehead
                  | content printpara handlehead
                  | OPENHEAD ENDTABLE skiptag
                  |
    '''
    if(len(p)== 6):
        # print(f"{p[4]}\n")
        filep.write(f"{p[4]}\n")
    elif(len(p)==4):
        # print(f"{p[2]}\n")
        filep.write(str(p[2])+"\n")
    # print(len(p))



def p_table(p):
    '''table : skiptag  BEGINTABLE skiptag1  handlehead '''

 
def p_empty(p):
    '''empty :'''
    pass
 
def p_content(p):
    '''content : CONTENT content
               | empty'''
    if(len(p)==3):
        if(p[1]!="edit"):
            
            
            p[0] = str(p[1])+str(p[2])
            
        
        else:
            p[0] = ""
        
    
 
def p_error(p):
    # print("\n\n\n\n\nerror....",p)
    pass
 
#########DRIVER FUNCTION#######
def main(link):
    
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
    
    fp1 = open("response_links.txt","r")
    data = fp1.read()
    base = "https://en.wikipedia.org"
    # print(data)
    for link in data.split("\n"):
        link = link.strip('">')
        attr = link.split(" ")
        
        # print(len(attr))
        # print(attr[-1])
        
        # if(attr[-1]=="201"):
        #     print(base+attr[1].split("=")[1].strip('"'))
        #     main(base+attr[1].split("=")[1].strip('"'))

        # elif(attr[-1]=="2023"):
        # #     print(base+attr[1].split("=")[1].strip('"'))
        #     get_data_2023.main(base+attr[1].split("=")[1].strip('"'),"2023")
        # elif(attr[-1]=="2024"):
        # #     print(base+attr[1].split("=")[1].strip('"'))
        #     get_data_2023.main(base+attr[1].split("=")[1].strip('"'),"2024")
        if(attr[-1]=="2020"):
            print(base+attr[1].split("=")[1].strip('"'))
            get_data_2020_response.main(base+attr[1].split("=")[1].strip('"'),"response_2020",attr[-2])
        elif(attr[-1]=="2021"):
            print(base+attr[1].split("=")[1].strip('"'))
            get_data_2020_response.main(base+attr[1].split("=")[1].strip('"'),"response_2021",attr[-2])
        elif(attr[-1]=="2022"):
            print(base+attr[1].split("=")[1].strip('"'))
            get_data_2020_response.main(base+attr[1].split("=")[1].strip('"'),"response_2022",attr[-2])
    fp1.close()




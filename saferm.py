#!/usr/bin/python3
import time ,os , sys
import psutil , datetime  , argparse , urllib3

if(os.name=='nt'):
    exit(10) ; 

commandstring = '' ;  

for arg in sys.argv:
    if ' ' in arg:
        commandstring+= '"{}" '.format(arg) ;
    else:
        commandstring+="{} ".format(arg) ; 

if(os.getpid()!=os.getpgid(0)):
    print('passing it to system rm') ; 
    os.system('rm ' + commandstring) ; 
    exit(0) ; 



def argument_parser():
    parser = argparse.ArgumentParser() ; 

    parser.add_argument('files' , nargs='+' ,  help="The files which need to be removed ")  ; 

    parser.add_argument('-f' , '--force' ,action="store_true" , required=False ,help="ignore nonexistent files and arguments, never prompt")

    parser.add_argument('-i' , action="store_true" , help="prompt before every removal " , required=False) ; 
    
    parser.add_argument('-I' , action="store_true" , help="prompt once before removing more than three files, or when  removing  recursively;  less intrusive than -i, while still giving protection against most mistakes" , required=False)

    parser.add_argument('--interactive' , action="store_true" , help="prompt according to WHEN: never, once (-I), or always (-i); without WHEN, prompt always" , required=False) 

    parser.add_argument('-r' ,'-R', '--recursive' ,  action="store_true" ,help="remove directories and their contents recursively" , required=False)

    parser.add_argument('-d' , help='remove empty directories',  action="store_true" ,required=False) ; 

    parser.add_argument('-v' , help="explain what is being done" ,  action="store_true" ,required=False) ; 

    
    args = parser.parse_args() ; 
    return args ; 



# t = time.localtime() ; 
# timeString = "{}-{:0>2}-{:0>2}T{:0>2}:{:0>2}:{:0>2}".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
# pathString = 




# trashpath = "~/.local/share/Trash"
# trashinfoString = '''
# [Trash Info]
# Path=/home/natesh/Documents/Smart%20India%20Hackathon.docx
# DeletionDate={}
# '''


args = argument_parser() ; 

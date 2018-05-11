#!/usr/bin/python3
import time ,os , sys
import psutil , datetime  , argparse

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

parser = argparse.ArgumentParser() ;
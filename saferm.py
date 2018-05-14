#!/usr/bin/python3
import time ,os , sys
import psutil , datetime  , argparse , urllib3 , shutil
import glob , re , errno , subprocess
from pwd import getpwuid

def find_owner(filename):
    return getpwuid(os.stat(filename).st_uid).pw_name

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

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


def is_dir_empty(path):
    for dirpath, dirnames, files in os.walk(dir):
        if files:
            return False; 
        else:
            return True


def argument_parser():
    parser = argparse.ArgumentParser() ; 
    parser.add_help  = '''
    
    This is custom custom script to remove files safely without the risk of losing them permanently as what happens when we use rm in linux. 
    The script puts the deleted files safely in the trash like if you were deleting your file in your file manager.
    
    '''

    parser.add_argument('files' , nargs='+' ,  help="The files which need to be removed ")  ; 

    parser.add_argument('-f' , '--force' ,action="store_true" , required=False ,help="ignore nonexistent files and arguments, never prompt")

    parser.add_argument('-i' , '--interactive' , action="store_true" , help="prompt before every removal " , required=False) ; 
    
    parser.add_argument('-I' , action="store_true" , help="prompt once before removing more than three files, or when  removing  recursively;  less intrusive than -i, while still giving protection against most mistakes" , required=False)

    # parser.add_argument('--interactive[=WHEN]' , action="store_true" , help="prompt according to WHEN: never, once (-I), or always (-i); without WHEN, prompt always" , required=False) 

    parser.add_argument('-r' ,'-R', '--recursive' ,  action="store_true" ,help="remove directories and their contents recursively" , required=False)

    parser.add_argument('-d' , '--dir', help='remove empty directories',  action="store_true" ,required=False) ; 

    parser.add_argument('-v' , '--verbose' , help="explain what is being done" ,  action="store_true" ,required=False) ; 

    parser.add_argument('--one-file-system' , help="explain what is being done" ,  action="store_true" ,required=False) ; 

    parser.add_argument('--no-preserve-root' , help="explain what is being done" ,  action="store_true" ,required=False) ; 

    parser.add_argument('--preserve-root' , help="when removing a hierarchy recursively, skip any directory that is on a file system different from that of the corresponding command line argument" ,  action="store_true" ,required=False) ; 
    
    args = parser.parse_args() ; 
    return args ; 


args = argument_parser() ;
rm_command_string_without_files = 'rm '

if(args.force):rm_command_string_without_files+=" -f "
if(args.dir):rm_command_string_without_files+=" -d "
if(args.I ):rm_command_string_without_files+=" -I "
if(args.interactive):rm_command_string_without_files+=" -i "
if(args.recursive):rm_command_string_without_files+=" -r "
if(args.no_preserve_root):rm_command_string_without_files+=" --no-preserve-root "
if(args.preserve_root):rm_command_string_without_files+=" --preserve-root "
if(args.one_file_system):rm_command_string_without_files+=" --one-file-system "

print(rm_command_string_without_files) ; 


trashfilespath = os.path.expanduser("~/.local/share/Trash/files") ; 
trashinfopath= os.path.expanduser("~/.local/share/Trash/info") ; 

t = time.localtime() ; 
timeString = "{}-{:0>2}-{:0>2}T{:0>2}:{:0>2}:{:0>2}".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)


#Uncomment if glob patterns don't resolve in args.files

#>>>>>>>>>>>>>>>>>>>>.

# fileslist = [] ; #Final list after resolving patterns 

# for i in range(len(args.files)):
#     fileslist.extend(glob.glob(args.files[i])) ; 

# print(">>>>>" , fileslist) ;

#<<<<<<<<<<<<<<<<<<<<<
    
fullpaths = {os.path.abspath(path) for path in args.files}


trashfiles = os.listdir(trashfilespath) ; 

for path in fullpaths:

    if not os.path.exists(path):
        print("rm: cannot remove '{}': No such file or directory".format(path)) ; 
        continue ; 

    file_to_delete = os.path.basename(path) ; 
    filename_no_extention , extention  = os.path.splitext(file_to_delete)

    newpath = os.path.join(trashfilespath , os.path.basename(path)) ; 
    match_dot_with_filename_RE = re.compile('{}\.(\d+)$'.format(filename_no_extention))


    #>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #Detect file name collisions and keep adding the required duplicate numbers to the duplicate_number list to find the max one later . 

    duplicate_number = set(); 
    match_flag = False ; 
    if(file_to_delete in trashfiles):
        duplicate_number.add(1) ; 
        match_flag = True ; 

    for trashfile in trashfiles:
        match = match_dot_with_filename_RE.match(trashfile) ; 

        if(match):
            match_flag = True ; 
            duplicate_number.add( int(match.groups()[0])+1 ) ; 

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<,
    
            
    #If duplicate exists , then new file name should be with dot followed by max(duplicate_number) followed by the original exten
    if(match_flag):
        newpath = os.path.join(os.path.split(trashfilespath)[0] , filename_no_extention+'.'+str(max(duplicate_number))) ; 
        if(file_to_delete.endswith(extention)):
            newpath+=extention

        print("newpath after handling duplicates = " , newpath) ; 

 
    print("newpath = " , newpath) ; 



    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #Copy the current file to newpath 

    dummpy_new_path =  '/home/natesh/Trashtesting/files/'+file_to_delete
    print(path , dummpy_new_path) ;
    try:
        if(os.path.isdir(path)):
            if(not args.recursive):
                print("rm: cannot remove '{}': Is a directory".format(file_to_delete)) ; 
                continue

        copyanything(path , dummpy_new_path)  ;            


    except(PermissionError) as E:

        print(E , "trying to directly move the file or folder if -r is set ") ;
        
        try:
            shutil.move(path, dummpy_new_path ) ; 
        except PermissionError as E1:
            print(E1 , 'cant move the file doesnt have both read and write perm ') ; 
            continue ;

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    #os.system returns 0 if no error else returns int 
    if(os.system(rm_command_string_without_files+path)):
        print("Error in removing {}".format(path)) ; 
        continue ; 


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Save the deleted file information in the trashinfopath 

    trashinfoString = '''
    [Trash Info]
    Path={0}/home/natesh/Documents/Smart%20India%20Hackathon.docx
    DeletionDate={1}
    '''.format(path.replace(' ' , '%20') , timeString)


print("fullpaths = " , fullpaths) ;

pathString = ''''''


# safe-rm
safe "rm" puts the files you delete in a shell into the Trash (Recycle bin). The script is meant to be used in place of rm system command in linux . This script will safely delete your files and put them in the trash.

This solves accidental removals. The script is meant to be used as an alias with rm directly and unlike other such scripts , it can handle duplicate files in the trash and works for recursive arguments also . 

### Features :
+ meant to be used in place of rm
+ handles all arguments that rm can take
+ handles the file name collisions with the files already in trash
+ handles some permission issues automatically
+ if rm is called from any other script or indirectly then the system 'rm' command is used automatically
+ shows the appropriate error messages like those which arise in `rm` 


## Installation :

**Put the file in the /usr/local/bin directory and rename it to rm**

```
mv saferm.py /usr/local/bin/rm
```

## Usage :

Usage is just like we use the rm command normally

```
rm filename
```

Now it shows your filename in the Trash which can then be easily restored to any desired location.
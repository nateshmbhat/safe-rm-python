#!/usr/bin/python3
import os; 
print(os.getpid.__name__, os.getpid());
print(os.getpgid.__name__, os.getpgid(0));
print(os.getsid.__name__, os.getsid(0))

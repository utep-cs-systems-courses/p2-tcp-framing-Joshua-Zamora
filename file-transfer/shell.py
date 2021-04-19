import os
import sys
import re

from myreadline import myreadline
from fileClient import send_file, recieve_file

while True:
    if 'PS1' in os.environ:
        os.write(2, (os.environ['PS1']).encode())
    else:
        os.write(2, "$ ".encode())

    args = myreadline().strip().split(" ")
    
    if args[0] == "exit":
        os.write(2, "exiting shell...\n".encode())
        sys.exit(0)
    
    elif args[0] == "scp":
        if ":" in args[2]:
            local_file = args[1]
            remote_file = args[2][args[2].index(":") + 1:]
            host = args[2][:args[2].index(":")]
            send_file(local_file, remote_file, host)
        else:
            local_file = args[2]
            remote_file = args[1][args[1].index(":") + 1:]
            host = args[1][:args[1].index(":")]
            recieve_file(local_file, remote_file, host)

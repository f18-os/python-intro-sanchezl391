import os, re, sys

# Get Parent Process Id, for printing purposes
parentProcessId = os.getpid()

# Parent Process Prompts: Writes to stdout
os.write(1, "\nEnter a command: ".encode())

# Create Shell Subprocess to handle execution of command
processId = os.fork()
if processId < 0:  
    os.write(2, ("fork failed, returning %d\n" % processId).encode())
    sys.exit(1)

elif processId == 0:    # Child 
    os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
                 (os.getpid(), parentProcessId)).encode())
    # Read string from stdin
    user_input = input().split()    


    for dir in re.split(":", os.environ['PATH']): # try each directory in path
            # print(dir)
            program = "%s/%s" % (dir, user_input[0])
            try:
                os.execve(program, user_input, os.environ) # try to exec command
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly 
    sys.exit(1)
# Fork was successful, wait for child to terminate
else: 
    childPidCode = os.wait()
    os.write(1, ("Child Shell Process Terminated with exit code %d\n\n" % childPidCode).encode())




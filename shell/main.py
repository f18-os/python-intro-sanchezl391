import os, re, sys

def execute_cmd(cmd):
    for dir in re.split(":", os.environ['PATH']): # try each directory in path
        program = "%s/%s" % (dir, cmd[0])
        try:
            os.execve(program, cmd, os.environ) # try to exec command
            os.close(sys.stdout)
        except OSError:             # ...expected
            pass  

# Create SubProcess to emulate shell
parentProcessId = os.fork() 

if parentProcessId == 0: # Child Shell
    os.write(1, "\nEnter a command: ".encode())
    user_input = input().split() 

    hasPipe = "|" in user_input
    if(hasPipe):
        pipeIndex = user_input.index('|') # Has Pipe
        firstCmd = user_input[0 : pipeIndex]
        secondCmd = user_input[pipeIndex + 1: len(user_input)]

        r,w = os.pipe()
        # Fork another process to connect pipe to       
        childProcessId = os.fork()
        

        if(childProcessId == 0): # setting up child to read from pipe
            os.dup2(r, sys.stdin.fileno())
            os.close(r)
            os.close(w)
            execute_cmd(secondCmd)
        else: # writing side of pipe
            os.close(r)
            os.dup2(w, sys.stdout.fileno())
            execute_cmd(firstCmd)
    else: # No Pipe
        for dir in re.split(":", os.environ['PATH']): # try each directory in path
            program = "%s/%s" % (dir, user_input[0])
            try:
                os.execve(program, user_input, os.environ) # try to exec command
                os.close(sys.stdout)
            except OSError:             # ...expected
                pass                              # ...fail quietly 
else: # Parent Shell
    os.wait()

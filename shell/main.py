#!/usr/bin/env python3

import os, re, sys

def execute_cmd(cmd):
    for dir in re.split(":", os.environ['PATH']): # try each directory in path
        program = "%s/%s" % (dir, cmd[0])
        try:
            os.execve(program, cmd, os.environ) # try to exec command
            # os.close(sys.stdout)
        except OSError:             # ...expected
            pass  

# Create SubProcess to emulate shell
parentProcessId = os.fork() 

import fileinput

if parentProcessId == 0: # Child Shell
    os.write(1, "\nEnter a command: ".encode())
    user_input = input().split() 

    hasPipe = "|" in user_input
    if(hasPipe):
        pipeIndex = user_input.index('|') # Has Pipe
        firstCmd = user_input[0 : pipeIndex]
        secondCmd = user_input[pipeIndex + 1: len(user_input)]

        r,w = os.pipe()
        for f in (r, w):
            os.set_inheritable(f, True)
        # Fork another process to connect pipe to       
        childProcessId = os.fork()

        if(childProcessId == 0): # setting up child to read from pipe
            # os.dup2(r, 1)
            # os.close(0)
            # os.dup(r)
            os.dup2(r, 0)
            # for fd in (r, w):
            #     os.close(fd)
            readStr = ''
            for line in fileinput.input():
                readStr+=line
            secondCmd.insert(0, readStr)
            execute_cmd(secondCmd)
        else: # writing side of pipe
            os.dup2(w, r)
            # os.close(r)
            # print("1")
            # os.close(1)
            # print("2")
            # os.dup(w)
            # for fd in (r, w):
            #     os.close(fd)
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

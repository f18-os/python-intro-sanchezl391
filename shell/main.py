#!/usr/bin/env python3

import os, re, sys
import subprocess

def execute_cmd(cmd):
    for dir in re.split(":", os.environ['PATH']): # try each directory in path
        program = "%s/%s" % (dir, cmd[0])
        try:
            # subprocess.call(["ls > random.txt"])
            os.execve(program, cmd, os.environ) # try to exec command
            # os.close(sys.stdout)
        except OSError:             # ...expected
            pass
            # print("Error")  
def handle_pipe():
    pipeIndex = user_input.index('|') # Has Pipe          

    firstCmd = user_input[0 : pipeIndex]
    secondCmd = user_input[pipeIndex + 1: len(user_input)]

    r,w = os.pipe()
    for f in (r, w):
        os.set_inheritable(f, True)
            
    childProcessId = os.fork() # Fork another process to connect pipe to 

    if(childProcessId == 0): # setting up child to read from pipe
        os.dup2(r, 0)
        os.close(w)
        execute_cmd(secondCmd)
        os.close(1)
    else: # set up child writing to pipe
        os.close(r)
        os.dup2(w, 1)
        execute_cmd(firstCmd)
        os.close(w) # done writing data

def handle_right_redirection():
    redirectIndex  = user_input.index('>')

    firstCmd = user_input[0 : redirectIndex]
    secondCmd = user_input[redirectIndex + 1: len(user_input)]

    


# Create SubProcess to emulate shell
parentProcessId = os.fork() 

import fileinput


if parentProcessId == 0: # Child Shell
    os.write(1, "\nEnter a command: ".encode())
    user_input = input().split() 

    hasPipe = "|" in user_input
    hasRedirection = ">" in user_input


    if(hasPipe):
        handle_pipe()
    elif(hasRedirection):
        handle_right_redirection
            
    else: # No pipe, redirection
        if(user_input[0] == "cd"):
            os.chdir(user_input[1])
        else:
            execute_cmd(user_input)
else: # Parent Shell
    os.wait()



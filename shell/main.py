#!/usr/bin/env python3

import os, re, sys
import subprocess

# Executes a list of commands
def execute_cmd(cmd):
    for dir in re.split(":", os.environ['PATH']): # try each directory in path
        program = "%s/%s" % (dir, cmd[0])
        try:
            os.execve(program, cmd, os.environ) # try to exec command
        except OSError:             # ...expected
            pass
# Handles creating a pipe, setting up file descriptors, 
#   reading and writing to/from pipe, and executing commands
def handle_pipe():
    pipeIndex = user_input.index('|') # Has Pipe          

    # Split Commands into two sections
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
    elif(parentProcessId < 0):
        print("fork failed, returning %d\n" % parentProcessId, file=sys.stderr)
        sys.exit(1)
    else: # set up child writing to pipe
        os.close(r)
        os.dup2(w, 1)
        execute_cmd(firstCmd)
        os.close(w) # done writing data

import fileinput

# Loop to emulate shell
# Creates a process on each iteration
while True:
    # Create SubProcess to emulate shell
    parentProcessId = os.fork() 

    execute_cmd(["export", "PS1", "=" , ""])

    if parentProcessId == 0: # Child Shell
        os.write(1, "\n$ ".encode())
        user_input = input().split() 

        hasPipe = "|" in user_input

        if(hasPipe):
            handle_pipe()
                
        else: # No pipe
            if(user_input[0] == "cd"):
                os.chdir(user_input[1])
            else:
                execute_cmd(user_input)
    elif parentProcessId < 0:
        print("fork failed, returning %d\n" % parentProcessId, file=sys.stderr)
        sys.exit(1)
    else: # Parent Shell
        os.wait()




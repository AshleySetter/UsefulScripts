#!/usr/bin/python
import subprocess
import sys

def ssh_tunnel(localHost, remoteHost):
    bashCommand = "ssh -N -f -L localhost:{}:localhost:{} ash@ash-seahorse.clients.soton.ac.uk &".format(localHost, remoteHost)
    print("running command: {}".format(bashCommand))
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    #output, error = process.communicate()

if len(sys.argv) == 3:
    localHost = int(sys.argv[1])
    remoteHost = int(sys.argv[2])
    ssh_tunnel(localHost, remoteHost)
else:
    raise ValueError("Must enter localHost and remoteHost ports")

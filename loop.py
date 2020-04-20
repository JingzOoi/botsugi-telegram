import subprocess
import os
import sys


while True:
    if os.path.isfile('quit.txt'):
        kill = open('quit.txt').read()
        os.remove('quit.txt')
        break
    params = [sys.executable, 'main.py']
    params.extend(sys.argv[1:])
    subprocess.call(params)

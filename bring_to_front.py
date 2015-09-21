__author__ = 'churley'
import os
import subprocess

def showNav():
        subprocess.Popen('wmctrl -a "LEFTNAV"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

if __name__=='__main__':
    showNav()

from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
from commands import start, update
import argparse
import json
import os
import argparse

my_parser = argparse.ArgumentParser(prog='skool', description='Let SkoolOS control your system', epilog="Try again")
my_parser.add_argument('--init', action="store_true") #returns true if run argument
args = my_parser.parse_args()

update()
outputs = vars(args)
if(outputs['init']):
    start()







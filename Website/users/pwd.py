import os

pwd = "heyyy"
path = os.getcwd()
p = os.path.join(path, '../../', 'pwd.txt')
open(p, 'w')
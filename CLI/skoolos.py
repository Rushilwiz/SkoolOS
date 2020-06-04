import sys
import click
from selenium import webdriver;

PATH = "C:\Program Files (x86)\chromedriver.exe"

print("")
print(" SSSSS   CCCCC  HH   HH  OOOOO   OOOOO  LL        OOOOO   SSSSS ")
print("SS      CC    C HH   HH OO   OO OO   OO LL       OO   OO SS     ")
print(" SSSSS  CC      HHHHHHH OO   OO OO   OO LL       OO   OO  SSSSS ")
print("     SS CC    C HH   HH OO   OO OO   OO LL       OO   OO      SS")
print(" SSSSS   CCCCC  HH   HH  OOOO0   OOOO0  LLLLLLL   OOOO0   SSSSS ")
print("")

driver = webdriver.Chrome(PATH)

driver.get("")
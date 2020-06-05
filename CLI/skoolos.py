import sys
import click
from selenium import webdriver;
import os.path


def main():
    print("")
    print(" SSSSS   CCCCC  HH   HH  OOOOO   OOOOO  LL        OOOOO   SSSSS ")
    print("SS      CC    C HH   HH OO   OO OO   OO LL       OO   OO SS     ")
    print(" SSSSS  CC      HHHHHHH OO   OO OO   OO LL       OO   OO  SSSSS ")
    print("     SS CC    C HH   HH OO   OO OO   OO LL       OO   OO      SS")
    print(" SSSSS   CCCCC  HH   HH  OOOO0   OOOO0  LLLLLLL   OOOO0   SSSSS ")
    print("")

    if not os.path.exists(".profile"):
        authenticate()
    else:
        print("welcome back")



def authenticate():
    file = open(".profile", "w")
    file.write("Your Username")
    file.close()


if __name__ == "__main__":
    main()

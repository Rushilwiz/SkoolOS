from bgservice import SkoolOSDaemon as sod
import threading

logger = sod()


if __name__ == "__main__":
    line=1
    print(line)
    line+=1
    logger.start()
    print(line)
    line+=1
    input("Enter any key when you are done modifyng the /tmp/ directory")
    print(line)
    line+=1
    logger.stop()
    print(line)
    line+=1

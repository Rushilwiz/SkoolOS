import os, sys
import time
import pyinotify

start_time = None
edit_times = []
end_time = None


def write_pid_file():
  pid = str(os.getpid())
  f = open('/tmp/skoolos_work_logger', 'w')
  f.write(pid)
  f.close()


def readable_time(input_time):
    return time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime(input_time))


def start_service(dir_to_watch):
    start_time = time.time()



def Main():
    print("This does nothing right now...")


if __name__ == "__main__":
    Main()

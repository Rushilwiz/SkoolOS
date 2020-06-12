import os
import sys
import signal
import time
import event_processor


class SkoolOSDaemmon:
    """Constructor"""
    def __init__(self, work_dir):
        self.work_dir = work_dir
        self.start_time = None
        self.end_time = None
    """Stores the pid of the program to be terminated externally"""
    def write_pid_file(self):
        pid = str(os.getpid())
        file_ = open('/tmp/skoolosdaemonpid', 'w')
        file_.write(pid)
        file_.close()
    def readable_time(self, input_time):
        return time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime(input_time))
    def start_service(self):
        start_time = time.time()
        log_file = open('/tmp/skooloslog-' + start_time, 'w')
        log_file.write("Started work: " + self.readable_time(start_time))
        sys.stdout = log_file
        event_processor.watch_dir(self.work_dir)


def Main():
    print("This does nothing right now...")


if __name__ == "__main__":
    Main()

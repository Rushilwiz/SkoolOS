import os
import sys
import signal
import time
import event_processor


class SkoolOSDaemon:
    """Constructor"""
    def __init__(self, work_dir):
        self.work_dir = work_dir
        self.start_time = None
        self.end_time = None
        self.log_file = None
    def __write_pid_file(self):
        pid = str(os.getpid())
        file_ = open('/tmp/skoolosdaemonpid', 'w')
        file_.write(pid)
        file_.close()
    def readable_time(self, input_time):
        return time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime(input_time))
    def start(self):
        __write_pid_file()
        self.start_time = time.time()
        self.log_file = open('/tmp/skooloslogs/' + str(self.start_time), 'w')
        self.log_file.write("Started work: \n" + self.readable_time(self.start_time))
        sys.stdout = self.log_file
        event_processor.watch_dir(self.work_dir)
    def stop(self):
        self.end_time = time.time()
        self.log_file.write("Stop time: \n" + self.readable_time(self.end_time))
        self.log_file.write("Total work time: " + 
                            time.strftime("%H:%M:%S", time.gmtime(self.end_time - self.start_time)))


logger = None


def Main():
    logger = SkoolOSDaemon("/tmp")
    logger.start()


if __name__ == "__main__":
    Main()

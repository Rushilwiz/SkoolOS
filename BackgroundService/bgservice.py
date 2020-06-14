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
        try:
            dirName = "/tmp/skooloslogs"
            # Create log Directory
            os.mkdir(dirName)
        except FileExistsError:
            pass
        pid = str(os.getpid())
        file_ = open('/tmp/skoolosdaemonpid', 'w')
        file_.write(pid)
        file_.close()
    def readable_time(self, input_time):
        return time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime(input_time))
    def start(self):
        self.__write_pid_file()
        self.start_time = time.time()
        self.log_file = open('/tmp/skooloslogs/' + str(self.start_time), 'w')
        self.log_file.write("Start time: " + self.readable_time(self.start_time) + "\n")
        sys.stdout = self.log_file
        event_processor.watch_dir(self.work_dir)
    def stop(self):
        event_processor.stop_watching()
        self.end_time = time.time()
        self.log_file.write("Stop time: \n" + self.readable_time(self.end_time))
        self.log_file.write("Total work time: " + 
                            time.strftime("%H:%M:%S", time.gmtime(self.end_time - self.start_time)))




logger = None

def Main():
    def signal_handler(signum, frame):
        logger.stop()
    signal.signal(signal.SIGINT, signal_handler)
    global logger
    logger = SkoolOSDaemon("/tmp")
    logger.start()


if __name__ == "__main__":
    Main()

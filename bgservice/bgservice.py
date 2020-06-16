import time
import sys
import os
import pyinotify
import checker


class EventHandler(pyinotify.ProcessEvent):
    _methods = [
        "IN_CREATE",
        "IN_CLOSE_WRITE",
        "IN_DELETE",
        "IN_MOVED_TO",
        "IN_MOVED_FROM",
        "IN_OPEN",
    ]

    def process_IN_CREATE(self, event):
        description = \
            "Event: Created file\n" \
            "Event Path: {}\n" \
            "Timestamp: {}\n".format(
                event.pathname,
                time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime())
                )
        print(description)

    def process_IN_CLOSE_WRITE(self, event):
        description = \
            "Event: Wrote to a file\n" \
            "Event Path: {}\n" \
            "Timestamp: {}\n".format(
                event.pathname,
                time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime())
                )
        print(description)

    def process_IN_DELETE(self, event):
        description = \
            "Event: Deleted file\n" \
            "Event Path: {}\n" \
            "Timestamp: {}\n".format(
                event.pathname,
                time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime())
                )
        print(description)

    def process_IN_MOVED_TO(self, event):
        description = \
            "Event: Moved a file in\n" \
            "Event Path: {}\n" \
            "Timestamp: {}\n".format(
                event.pathname,
                time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime())
                )
        print(description)

    def process_IN_MOVED_FROM(self, event):
        description = \
            "Event: Moved a file out\n" \
            "Event Path: {}\n" \
            "Timestamp: {}\n".format(
                event.pathname,
                time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime())
                )
        print(description)

    def process_IN_OPEN(self, event):
        description = \
            "Event: Opened file\n" \
            "Event Path: {}\n" \
            "Timestamp: {}\n".format(
                event.pathname,
                time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime())
                )
        print(description)


NOTIFIER = None
STDOUT = sys.stdout
DIR = None
START_TIME = None


def watch_dir(watched_dir="/tmp", logdir="/tmp/skooloslogs"):
    global DIR
    global START_TIME
    global NOTIFIER
    DIR = watched_dir
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    logfile = open(
        logdir + "/skoolos_" +
        time.strftime("%m%d%Y-%H%M%S", time.localtime()), 'w')
    START_TIME = time.time()
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_CREATE | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_DELETE | \
        pyinotify.IN_MOVED_TO | pyinotify.IN_MOVED_FROM | pyinotify.IN_OPEN
    NOTIFIER = pyinotify.ThreadedNotifier(wm, EventHandler())
    NOTIFIER.start()
    sys.stdout = open("/dev/null", 'w')
    wm.add_watch(watched_dir, mask, rec=True)
    sys.stdout = logfile
    print("Start time: " +
          time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime()) + "\n")


def stop_watching():
    NOTIFIER.stop()
    now = time.time()
    print("End time: " +
          time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime()))
    print("\nTotal work time: " +
          time.strftime("%H:%M:%S", time.gmtime(now - START_TIME)))
    print("\n" + checker.shell_check())
    suspicious_files = checker.file_check(DIR)
    if suspicious_files != []:
        print(
            "\n\n--------------------------------------------------\n\n\n" +
            "WARNING: One or more file did not have file extensions that are acceptable.\n"
            + "The paths to these files are listed below:\n")
        print(*suspicious_files, sep='\n')
    sys.stdout = STDOUT
    print("Done watching.\n")

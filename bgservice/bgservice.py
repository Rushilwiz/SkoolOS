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
        """
        Generates an output to record for IN_CREATE events
        :param event: event automatically passed to function
        :return: none
        """
        description = \
            "Event: Created file\n" \
            "Event Path: {}\n" \
            "Timestamp: {}\n".format(
                event.pathname,
                time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime())
                )
        print(description)

    def process_IN_CLOSE_WRITE(self, event):
        """
        Generates an output to record for IN_CLOSE_WRITE events
        :param event: event automatically passed to function
        :return: none
        """
        description = \
            "Event: Wrote to a file\n" \
            "Event Path: {}\n" \
            "Timestamp: {}\n".format(
                event.pathname,
                time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime())
                )
        print(description)

    def process_IN_DELETE(self, event):
        """
        Generates an output to record for IN_DELETE events
        :param event: event automatically passed to function
        :return: none
        """
        description = \
            "Event: Deleted file\n" \
            "Event Path: {}\n" \
            "Timestamp: {}\n".format(
                event.pathname,
                time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime())
                )
        print(description)

    def process_IN_MOVED_TO(self, event):
        """
        Generates an output to record for IN_MOVED_TO events
        :param event: event automatically passed to function
        :return: none
        """
        description = \
            "Event: Moved a file in\n" \
            "Event Path: {}\n" \
            "Timestamp: {}\n".format(
                event.pathname,
                time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime())
                )
        print(description)

    def process_IN_MOVED_FROM(self, event):
        """
        Generates an output to record for IN_MOVED_FROM events
        :param event: event automatically passed to function
        :return: none
        """
        description = \
            "Event: Moved a file out\n" \
            "Event Path: {}\n" \
            "Timestamp: {}\n".format(
                event.pathname,
                time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime())
                )
        print(description)

    def process_IN_OPEN(self, event):
        """
        Generates an output to record for IN_OPEN events
        :param event: event automatically passed to function
        :return: none
        """
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


def watch_dir(watched_dir="/tmp", log_dir="/tmp/skooloslogs"):
    """
    Watches the specified directory for changes and outputs it in
    human readable format to a log file in the specified log directory.
    :param watched_dir: directory to watch for changes
    :param log_dir: directory to store log files
    :return: none
    """
    global DIR
    global START_TIME
    global NOTIFIER
    DIR = watched_dir
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logfile = open(
        log_dir + "/skoolos_" +
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
    """
    Stops the watch started by watch_dir()
    :return: none
    """
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

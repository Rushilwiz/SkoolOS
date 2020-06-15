import time
import sys
import os
import pyinotify


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


def watch_dir(watched_dir="/tmp", logdir="/tmp/skooloslogs"):
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    logfile = open(
        logdir + "/skoolos_" +
        time.strftime("%m%d%Y-%H%M%S", time.localtime()), 'w')
    sys.stdout = logfile
    print("Start time: " +
          time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime()) + "\n\n")
    global NOTIFIER
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_CREATE | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_DELETE | \
        pyinotify.IN_MOVED_TO | pyinotify.IN_MOVED_FROM | pyinotify.IN_OPEN
    NOTIFIER = pyinotify.ThreadedNotifier(wm, EventHandler())
    NOTIFIER.start()
    wm.add_watch(watched_dir, mask, rec=True)


def stop_watching():
    NOTIFIER.stop()
    print("End time: " +
          time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime()))
    sys.stdout = STDOUT
    print("Done watching.\n")

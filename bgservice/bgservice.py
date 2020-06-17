"""
A simple background service to log events in a directory,
check for git commands in bash/zsh history,
and check for non-whitelisted files in the watched directory.
"""
import time
import sys
import os
import pyinotify
from pathlib import Path
from glob import glob


NOTIFIER = None
STDOUT = sys.stdout
DIR = None
START_TIME = None


def watch_dir(watched_dir=str(Path.home()), log_dir="SkoolOS/logs"):
    """
    Watches the specified directory for changes and outputs it in
    human readable format to a log file in the specified log directory.
    param watched_dir: directory to watch for changes
    param log_dir: directory to store log files
    return: none
    """
    global DIR
    global START_TIME
    global NOTIFIER
    DIR = watched_dir
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logfile_ = log_dir + "/skooloslog"
    if os.path.isfile(logfile_):
        os.remove(logfile_)
    logfile = open(logfile_, 'w')
    START_TIME = time.time()
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_CREATE | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_DELETE | \
        pyinotify.IN_MOVED_TO | pyinotify.IN_MOVED_FROM | pyinotify.IN_OPEN
    NOTIFIER = pyinotify.ThreadedNotifier(wm, EventHandler())
    NOTIFIER.start()
    sys.stdout = open("/dev/null", 'w')
    wm.add_watch(watched_dir, mask, rec=True)
    time.sleep(1)
    sys.stdout = logfile
    print("Start time: " +
          time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime()) + "\n")


def stop_watching():
    """
    Stops the watch started by watch_dir()
    return: none
    """
    NOTIFIER.stop()
    now = time.time()
    print("End time: " +
          time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime()))
    print("\nTotal work time: " +
          time.strftime("%H:%M:%S", time.gmtime(now - START_TIME)))
    print("\n" + shell_check())
    suspicious_files = file_check(DIR)
    if suspicious_files != []:
        print(
            "\n\n--------------------------------------------------\n\n\n" +
            "WARNING: One or more file did not have file extensions that are acceptable.\n"
            + "The paths to these files are listed below:\n")
        print(*suspicious_files, sep='\n')
    sys.stdout = STDOUT

file_whitelist = [
    # text and document files
    ".doc",
    ".docx",
    ".odt",
    ".pdf",
    ".rtf",
    ".tex",
    ".txt",
    ".wpd",
    # video files
    ".3g2",
    ".3gp",
    ".avi",
    ".flv",
    ".h264",
    ".m4v",
    ".mkv",
    ".mov",
    ".mp4",
    ".mpg",
    ".mpeg",
    ".rm",
    ".swf",
    ".vob",
    ".wmv",
    # spreadsheet files
    ".ods",
    ".xls",
    ".xlsm",
    ".xlsx",
    ".csv",
    # programming files
    ".c",
    ".class",
    ".cpp",
    ".cs",
    ".go",
    ".h",
    ".java",
    ".pl",
    ".sh",
    ".swift",
    ".vb",
    # presentation files
    ".key",
    ".odp",
    ".pps",
    ".ppt",
    ".pptx",
    # image files
    ".ai",
    ".bmp",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".png",
    ".ps",
    ".psd",
    ".svg",
    ".tif",
    ".tiff",
]


def shell_check():
    """
    Check .bash_history and .histfile for git commands that could interfere with SkoolOS
    return: results of the check
    """
    bash_history = [
        line.strip()
        for line in open(os.path.expanduser("~/.bash_history"), 'r')
    ]
    zsh_history = [
        line.strip() for line in open(os.path.expanduser("~/.histfile"), 'r')
    ]
    suspicious_commands = []
    for i in bash_history + zsh_history:
        if "git" in i:
            suspicious_commands.append(i)
    if suspicious_commands:
        return str(
            len(suspicious_commands)
        ) + " suspicious commands found:\n" + "\n".join(suspicious_commands)
    return "Nothing suspicious found in bash or zsh history."


def verify_file(file_):
    """
    Check if the file name has an extension in the list of whitelisted file exentsions
    param file_: path to file
    return: whether or not the file's extension is whitelisted
    """
    for ext in file_whitelist:
        if len(file_) > len(ext):
            if file_[len(file_) - len(ext):] == ext:
                return True
    return False


def file_check(dir_):
    """
    Checks specified dir_ for non-whitelisted files using verify_file()
    param dir_: directory to check
    return: list of suspicious files
    """
    files = glob(dir_ + "/**/*", recursive=True)
    suspicious_files = []
    for file_ in files:
        if not verify_file(file_):
            suspicious_files.append(file_)
    return suspicious_files

class EventHandler(pyinotify.ProcessEvent):
    """
    Custom event handler for watching a SkoolOS work directory
    """
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
        param event: event automatically passed to function
        return: none
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
        param event: event automatically passed to function
        return: none
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
        param event: event automatically passed to function
        return: none
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
        param event: event automatically passed to function
        return: none
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
        param event: event automatically passed to function
        return: none
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
        param event: event automatically passed to function
        return: none
        """
        description = \
            "Event: Opened file\n" \
            "Event Path: {}\n" \
            "Timestamp: {}\n".format(
                event.pathname,
                time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime())
                )
        print(description)

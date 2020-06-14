import time
import pyinotify


def readable_time(input_time):
    return time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime(input_time))


class EventProcessor(pyinotify.ProcessEvent):
    _methods = ["IN_ACCESS",
                "IN_CREATE",
                "IN_CLOSE_WRITE",
                "IN_DELETE",
                "IN_MOVED_TO",
                "IN_MOVED_FROM",
                ]


def __method_format(method):
    return {
        "IN_ACCESS":"Accessed a file",
        "IN_CREATE":"Created a file",
        "IN_CLOSE_WRITE":"Wrote to a file",
        "IN_DELETE":"Deleted a file",
        "IN_MOVED_TO":"Moved a file or directory in from elsewhere",
        "IN_MOVED_FROM":"Moved a file or directory elsewhere",
    }.get(method, "Unknown event")


def __process_generator(cls, method):
    def _method_name(self, event):
        description = "Event description: {}\n" \
            "Path name: {}\n" \
            "Event Name: {}\n" \
            "Timestamp: {}\n".format(__method_format(method),
                                     event.pathname,
                                     event.maskname,
                                     readable_time(time.time())
                                     )
        if "IN_DELETE" in description:
            description += "Warning: Unexpected file deletion\n"
        if "IN_MOVED_TO" in description:
            description += "Warning: Unexpected file add to work\n"
        if "IN_MOVED_FROM" in description:
            description += "Warning: Unexpected file moved out of directory\n"
        print(description)
    _method_name.__name__ = "process_{}".format(method)
    setattr(cls, _method_name.__name__, _method_name)


EVENT_NOTIFIER = None


def watch_dir(dir_to_watch):
    global EVENT_NOTIFIER
    for method in EventProcessor._methods:
        __process_generator(EventProcessor, method)
    watch_manager = pyinotify.WatchManager()
    EVENT_NOTIFIER = pyinotify.Notifier(watch_manager, EventProcessor())
    watch_manager.add_watch(dir_to_watch, pyinotify.ALL_EVENTS)
    EVENT_NOTIFIER.loop()#daemonize=True)


def stop_watching():
    EVENT_NOTIFIER.stop()

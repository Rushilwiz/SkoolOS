import time
import pyinotify


def readable_time(input_time):
    return time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime(input_time))


class EventProcessor(pyinotify.ProcessEvent):
    _methods = ["IN_ACCESS",
                "IN_CREATE",
                "IN_CLOSE_WRITE",
                "IN_DELETE"
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
    }[method]


def __process_generator(cls, method):
    def _method_name(self, event):
        print("Event description: {}\n"
              "Path name: {}\n"
              "Event Name: {}\n"
              "Timestamp: {}\n".format(__method_format(method),
                                       event.pathname,
                                       event.maskname,
                                       readable_time(time.time())
                                       )
              )
    _method_name.__name__ = "process_{}".format(method)
    setattr(cls, _method_name.__name__, _method_name)


def watch_dir(dir_to_watch):
    for method in EventProcessor._methods:
        __process_generator(EventProcessor, method)
    watch_manager = pyinotify.WatchManager()
    event_notifier = pyinotify.Notifier(watch_manager, EventProcessor())
    watch_manager.add_watch(dir_to_watch, pyinotify.ALL_EVENTS)
    event_notifier.loop()
